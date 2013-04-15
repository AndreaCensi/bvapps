from contracts import contract
from geometry.manifolds import R2
from geometry.manifolds.point_set import PointSet
from geometry.poses import translation_from_SE3, angle_from_SE2, SE2_from_SE3
import numpy as np
from bootstrapping_olympics.programs.manager.meat.load_agent_state import load_agent_state
from bootstrapping_olympics.configuration.master import set_boot_config
import warnings
from boot_agents.bdse.agent.bdse_servo import BDSEServo
from boot_agents.bdse.model.bdse_model import BDSEmodel
from boot_agents.bds.bds_agent import BDSAgent


def read_pose_observations(data_central, id_robot, id_episode):
    """ Returns a list of (timestamp, pose, observations) """
    data = []
    
    log_index = data_central.get_log_index()
    log_index.reindex()
    source = log_index.read_robot_episode(id_robot, id_episode, read_extra=True)
    for bd in source:
        extra = bd['extra'].item()
        extra['odom'] = np.array(extra['odom'])
        extra['odom_th'] = angle_from_SE2(SE2_from_SE3(extra['odom']))
        extra['odom_xy'] = translation_from_SE3(extra['odom'])[:2]
        
        data.append(bd)

    return data


def xy_from_data(data):
    # 2 x N translation array
    res = np.array([bd['extra'].item()['odom_xy'] for bd in data])
    assert res.shape[1] == 2
    return res

def process(data, min_dist):
    res = {}
    res['raw'] = data
    res['raw_xy'] = xy_from_data(res['raw']) 
         
    res['sparse'] = sparsify(data, min_dist)
    res['sparse_xy'] = xy_from_data(res['sparse'])
    res['points'] = PointSet(R2, points=res['sparse_xy'])
    
    index = res['points'].centroid_index()
    
    res['centroid'] = res['points'].points[index]
    
    res['bd_goal'] = res['sparse'][index]
    return res

def process_compute_distances(processed):
    processed['p_distance'] = [R2.distance(p, processed['centroid'])  # @UndefinedVariable
                               for p in processed['sparse_xy']]  # @UndefinedVariable
    
    # ... for observations
    y_dist = lambda y0, y1: np.linalg.norm(y0 - y1) 
    y_goal = get_y_goal(processed)
    processed['y_distance'] = [y_dist(bd['observations'], y_goal) for bd in processed['sparse']]
    return processed

def get_y_goal(processed):
    return processed['bd_goal']['observations'].copy()


@contract(y='array[N]', max_diff='float,>0', returns='array[N]')
def remove_array_discontinuity(y, max_diff):
    """ Removes discontinuities from an array """
    
    changed = True
    
    while changed:
        y, changed = change_far(y, max_diff)
        # print('changed: %s' % changed)
    
    return y
    
def change_far(y, max_diff):
    y = y.copy()
#     y_ok = find_ok(y, max_diff)
    ok = np.logical_and(y > 0.04, y < .9) 
    
    changed = []
    for i in range(y.size):
        val = y[i]
        
        if not ok[i]:
            for j in range(i, y.size):
                if ok[j]:
                    repl = y[j]
                    y[i] = repl
                    assert repl > 0
                    changed.append((i, j, val, repl))
                    break
            else:
                continue

#     for i in range(1, y.size - 1):
#         val = y[i]
#         if (not y_ok[i]) and y_ok[i + 1]:
#             repl = y[i + 1]
#             assert y_ok[i + 1]
#             assert repl > 0
#             y[i] = repl
#             changed.append((i, val, repl))
#         
#         
#         if (not y_ok[i]) and y_ok[i - 1]:
#             repl = y[i - 1]
#             assert y_ok[i - 1]
#             assert repl > 0
#             y[i] = repl
#             changed.append((i, val, repl))
#             
#         if (not y_ok[i]) and y_ok[i - 1] and y_ok[i - 2]:
#             repl = y[i - 1]
#             y[i] = repl
#             changed.append((i, val, repl))
#             
    return y, changed
    
def find_ok(y, max_diff):
    ok = np.zeros(y.size, 'bool')
    close_enough = lambda a, b: np.abs(a - b) < max_diff
    for i in range(y.size):
        left_ok = (i > 0) and close_enough(y[i], y[i - 1]) 
        right_ok = (i < y.size - 1) and close_enough(y[i], y[i + 1])
        ok[i] = left_ok and right_ok
    return ok    




def remove_discontinuities(processed, threshold=0.2):
    warnings.warn('Trimming discontinuities, using error threshold = %f' % threshold)
    max_diff = 0.1
    bd = processed['bd_goal'] 
    bd['observations'] = remove_array_discontinuity(bd['observations'], max_diff)
    
    
    for bd in processed['sparse']: 
        bd['observations'] = remove_array_discontinuity(bd['observations'], max_diff)
     
    if False:        
        y_goal = get_y_goal(processed) 
        for bd in processed['sparse']: 
            y = bd['observations']
            e = np.abs(y - y_goal)
            too_far = e > threshold
            y[too_far] = y_goal[too_far]
    return processed

def compute_servo_action(processed, data_central, id_agent, id_robot, variation):
    set_boot_config(data_central.get_bo_config())
    agent, state = load_agent_state(data_central, id_agent, id_robot,
                                    reset_state=False, raise_if_no_state=True)
    
    servo_agent = agent.get_servo()             

    if False:
        if False or not isinstance(agent, BDSAgent):
            servo_agent = agent.get_servo()             
        else:
            warnings.warn('using our own servo variation')
            
            T = agent.bdse_estimator.T.get_value()
            
            if True:
                warnings.warn('using M=0')
                T = T * 0
            U = agent.bdse_estimator.U.get_value()
            model = BDSEmodel(M=T, N=U)
            servo_agent = BDSEServo(model, agent.commands_spec,
                                    strategy='S1', gain=0.1, linpoint='current')
        
 
    bd_goal = processed['bd_goal']
    
    processed['id_agent'] = id_agent
    processed['agent'] = agent
    processed['servo_agent'] = servo_agent
    
    for i, bd in enumerate(processed['sparse']):
        extra = bd['extra'].item()
        res = compute_servo_commands(servo_agent, bd_goal, bd, variation)
        extra.update(res)
        
      
    return processed

def compute_servo_commands(servo_agent, bd_goal, bd, variation):
    servo_agent.set_goal_observations(bd_goal['observations'])
    servo_agent.process_observations(bd) 
    res = servo_agent.choose_commands2()

    u = res['u']
    
    y0 = bd['observations']
    y_goal = bd_goal['observations']
  
    if True:
        # checking descent direction
        y_dot_pred = servo_agent.bdse_model.get_y_dot(y0, u)
        dt = 0.1
        y1 = y0 + y_dot_pred * dt
        
        e0 = np.linalg.norm(y_goal - y0)
        e1 = np.linalg.norm(y_goal - y1)
        
        print('e0 %.3f  e1 %.3f e1 - e0 = %+.3f' % (e0, e1, e1 - e0))
        res['e0'] = e0
        res['e1'] = e1
        res['e_diff'] = e1 - e0
        
    return res


@contract(points='array[Nx2]', returns='int,>=0,<N')
def select_center(points):
    """ Returns the index of the selected center. """
    mean = np.mean(points, axis=0)
    assert len(mean) == 2 
    
    

class Sparsifier():
    def __init__(self, manifold, min_dist):
        self.min_dist = min_dist
        self.point_set = PointSet(manifold)
        
    def accept(self, p):
        """ Returns True or False """
        if self.point_set.__len__() == 0:
            self.point_set.add(p)
            return True
        
        accept = not self.point_set.is_closer_than(p, self.min_dist)
        if accept:
            self.point_set.add(p)
            return True
        else:
            return False
        
        
        
def sparsify(data, min_dist):
    print('Original data: %d' % len(data))
    result = list(sparse_sequence(data, min_dist))
    print(' cut to %d ' % len(result))
    return result

def sparse_sequence(data, min_dist):
    """ Yields a sequence """
    sp = Sparsifier(manifold=R2, min_dist=min_dist)
    for bd in data:
        p = bd['extra'].item()['odom_xy']        
        if sp.accept(p):
            yield bd

