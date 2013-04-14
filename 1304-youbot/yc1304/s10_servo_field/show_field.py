from contracts import contract
from geometry.manifolds import R2
from geometry.manifolds.point_set import PointSet
from geometry.poses import translation_from_SE3, angle_from_SE2, SE2_from_SE3
import numpy as np
from bootstrapping_olympics.programs.manager.meat.load_agent_state import load_agent_state
from bootstrapping_olympics.configuration.master import set_boot_config


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
    res['y_goal'] = res['bd_goal']['observations']
    
    # distances to the goal
    # ... for positions
    res['p_distance'] = [R2.distance(p, res['centroid']) for p in res['sparse_xy']]  # @UndefinedVariable
    
    # ... for observations
    y_dist = lambda y0, y1: np.linalg.norm(y0 - y1) 
    res['y_distance'] = [y_dist(bd['observations'], res['y_goal']) for bd in res['sparse']]
    
    return res


def compute_servo_action(processed, data_central, id_agent, id_robot, variation):
    set_boot_config(data_central.get_bo_config())
    agent, state = load_agent_state(data_central, id_agent, id_robot,
                                    reset_state=False, raise_if_no_state=True)
    
    servo_agent = agent.get_servo()

#     y_goal = processed['y_goal'] 
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

