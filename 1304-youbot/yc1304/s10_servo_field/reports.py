import numpy as np
from reprep import Report
from yc1304.s10_servo_field.plots import (plot_reference_points_poses,
    plot_reference_points, plot_scalar_field_sign,
    plot_style_sensels, plot_style_sensels_deriv)
from geometry.poses import SE2_from_SE3, translation_angle_from_SE2
import warnings
 
def report_raw_display(processed):
    r = Report('raw_display')
    f = r.figure()

    xy = processed['raw_xy']
    centroid = processed['centroid']
    
    caption = "Raw trajectories with commands"
    with f.plot('some', caption=caption) as pylab:
        pylab.plot(xy[:, 0], xy[:, 1], '-')
        plot_odom_commands(pylab, processed['raw'][::20])
        pylab.axis('equal')

    
    caption = "Raw trajectory and selected points"
    with f.plot('sparse_xy', caption=caption) as pylab:
        pylab.plot(xy[:, 0], xy[:, 1], 'k+')
        pylab.plot(centroid[0], centroid[1], 'gs')
        plot_reference_points(pylab, processed)
        pylab.axis('equal')

    caption = "Selected points, drawn with poses"
    with f.plot('sparse_poses', caption=caption) as pylab:
        pylab.plot(xy[:, 0], xy[:, 1], 'k-')
        plot_reference_points_poses(pylab, processed)
        pylab.axis('equal')

    caption = "Selected points, drawn with poses and commands"
    with f.plot('sparse_poses_commands', caption=caption) as pylab:
        pylab.plot(xy[:, 0], xy[:, 1], 'k-')
        
        plot_odom_commands(pylab, processed['sparse'])
        pylab.axis('equal')

    return r

def plot_odom_commands(pylab, bds):
    poses = [bd['extra'].item()['odom'] for bd in bds]    
    commands = [bd['commands'] for bd in  bds]
    plot_poses_commands(pylab, poses, commands)

def plot_poses_commands(pylab, poses, commands,
                        pose_arrow_length=0.03,
                        cmd_arrow_length=0.05):

    pose_style = dict(head_width=0.01, head_length=0.01,
                      edgecolor=[0.8, 0.8, 0.8])

    # scale to given arrow_length
    us = np.array(commands)[:, :2]
    u_max = np.max(np.hypot(us[:, 0], us[:, 1]))
    us = us / u_max * cmd_arrow_length
    
    cmd_style = dict(head_width=0.01, head_length=0.01, edgecolor='blue')
    
    for pose, u in zip(poses, us):        
        p, th = translation_angle_from_SE2(SE2_from_SE3(pose))
        
        a = np.cos(th) * pose_arrow_length        
        b = np.sin(th) * pose_arrow_length
        #  pylab.arrow(p[0], p[1], a, b, **pose_style)
        
        # u_w = np.dot(pose, [u[0], u[1], 0, 0])[:2]
        warnings.warn('This is probably only correct with this dataset')
        u_w = u[1], -u[0]
        
        pylab.arrow(p[0], p[1], u_w[0], u_w[1], **cmd_style)
        

def report_distances(processed):
    r = Report('distances')
    p_dist = processed['p_distance']
    y_dist = processed['y_distance']
    
    f = r.figure('distance_stats') 

    with f.plot('y_vs_p') as pylab:
        pylab.plot(y_dist, p_dist, 's')
        pylab.xlabel('d(y_0, y_1)')
        pylab.ylabel('d(p_0, p_1)')

    with f.plot('p_vs_y') as pylab:
        pylab.plot(p_dist, y_dist, 's')
        pylab.ylabel('d(y_0, y_1)')
        pylab.xlabel('d(p_0, p_1)')

    return r

def get_extra_item(bds, field):
    return [bd['extra'].item()[field] for bd in bds]
 
def repsec_servo1_u(r, processed):
    f = r.figure()
    
    bds = processed['sparse']
    u = np.array(get_extra_item(bds, 'u'))
    xy = processed['sparse_xy']
    
    poses = get_extra_item(bds, 'odom')
    has_theta = u.shape[1] == 3

    caption = 'First two components of "u".'
    with f.plot('u01_arrows', caption=caption) as pylab:
        plot_reference_points(pylab, processed)
        plot_poses_commands(pylab, poses, u)
        pylab.axis('equal')

    if has_theta:
        u_th = u[:, 2]
        caption = 'Third component of "u".'
        with f.plot('u_th_sign', caption=caption) as pylab:
            plot_reference_points(pylab, processed)
            plot_scalar_field_sign(pylab, xy, u_th)


def repsec_servo1_u_raw(r, processed):
    f = r.figure()
    
    bds = processed['sparse']
    u = np.array(get_extra_item(bds, 'u_raw'))
    xy = processed['sparse_xy']
    
    poses = get_extra_item(bds, 'odom')
    has_theta = u.shape[1] == 3

    caption = 'First two components of "u".'
    with f.plot('u01_arrows', caption=caption) as pylab:
        plot_reference_points(pylab, processed)
        plot_poses_commands(pylab, poses, u)
        pylab.axis('equal')

    if has_theta:
        u_th = u[:, 2]
        caption = 'Third component of "u".'
        with f.plot('u_th_sign', caption=caption) as pylab:
            plot_reference_points(pylab, processed)
            plot_scalar_field_sign(pylab, xy, u_th)
    
def report_servo1(processed):
    r = Report('servo1')

    with r.subsection('u', robust=True) as s:
        repsec_servo1_u(s, processed)
    
    with r.subsection('u_raw', robust=True) as s:
        repsec_servo1_u_raw(s, processed)
     
    return r

def report_servo_details(processed, nsamples=6):
    r = Report('servo_details')
    
    bds = processed['sparse']
    for i in range(nsamples):
        bd = bds[np.random.randint(len(bds))]
        name = 'sample%s' % i
        r_i = report_servo_details_one(name, processed, bd)
        r.add_child(r_i)
    return r

def report_servo_details_one(name, processed, bd):
    r = Report(name)
    f = r.figure(cols=4)
    
    y_goal = processed['bd_goal']['observations'].copy()
    y0 = bd['observations'].copy()
    e = y0 - y_goal
    
    extra = bd['extra'].item()
    p = extra['odom_xy']
    u = extra['u']
    
    bdse_model = processed['servo_agent'].bdse_model
    y_dot_pred = bdse_model.get_y_dot(y0, u)
    y_dot_pred = y_dot_pred / np.max(np.abs(y_dot_pred)) * 0.05
    r.data('u', u)
    r.data('y_dot_pred', y_dot_pred)
    dt = 1
    y1 = y0 + y_dot_pred * dt

    with f.plot('map') as pylab:
        plot_reference_points(pylab, processed) 
        pylab.plot(p[0], p[1], 'r+')
        pylab.arrow(p[0], p[1], u[0], u[1])

    with f.plot('y0_vs_y_goal') as pylab:
        pylab.plot(y0, label='y0')
        pylab.plot(y_goal, label='ygoal')
        plot_style_sensels(pylab)   
        pylab.legend()
    with f.plot('y_dot_pred') as pylab:
        pylab.plot(y_dot_pred, label='y_dot_pred')
        plot_style_sensels(pylab)
        pylab.legend()   
    
    with f.plot('y0_y1') as pylab:
        pylab.plot(y0, label='y0')
        pylab.plot(y_goal, label='ygoal')
        pylab.plot(y1, label='y1')
        plot_style_sensels(pylab)
        pylab.legend()   
    
    with f.plot('error') as pylab:
        pylab.plot(e, label='error')

    r.add_child(report_prediction_all_commands(bd, bdse_model))
        
    return r

def report_prediction_all_commands(bd, bdse_model):
    r = Report('report_prediction')
    try:
        commands = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        for c in commands:
            r.add_child(report_prediction_command(bd, bdse_model, np.array(c)))
    except Exception as e:
        r.text('error', str(e))
        print('failed')
        
    return r
        
def report_prediction_command(bd, bdse_model, u):
    r = Report('cmd%s-%s' % (u[0], u[1]))
    y0 = bd['observations'].copy()
    y_dot_pred = bdse_model.get_y_dot(y0, u)
    y_dot_pred = y_dot_pred / np.max(np.abs(y_dot_pred)) * 0.05
    r.data('u', u)
    r.data('y_dot_pred', y_dot_pred)
    
    caption = """ Prediction for command %s """ % str(u)
    f = r.figure(caption=caption)
    
    with f.plot('y_dot_pred') as pylab:
        pylab.plot(y_dot_pred, label='y_dot_pred')
        plot_style_sensels_deriv(pylab)
        pylab.legend()   
  
    return r
    

