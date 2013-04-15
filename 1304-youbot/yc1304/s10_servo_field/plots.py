'''
    Functions like plot_* take pylab as first instance
'''
from reprep.plot_utils.axes import x_axis_extra_space, y_axis_set
from contracts import contract

def plot_style_sensels(pylab):
    y_axis_set(pylab, -0.1, 1.1)
    x_axis_extra_space(pylab)

def plot_style_sensels_deriv(pylab):
    y_axis_set(pylab, -0.1, 0.1)
    x_axis_extra_space(pylab)

import numpy as np
# 
# def plot_servo_arrows(pylab, ps, commands):
#     """
#         ps : list of 2D points
#         commands: list of 2D commands
#     """
# 
#     us = np.array(commands)[:, :2]
#     u_max = np.max(np.hypot(us[:, 0], us[:, 1]))
#     
#     arrow_length = 0.1
#     style = dict(head_width=0.01, head_length=0.01,
#                  edgecolor='black')
#     
#     us = us / u_max * arrow_length
#     print('u_max', u_max)
#     for p, u in zip(ps, us):
#         if np.hypot(u[0], u[1]) == 0:
#             continue
#         pylab.arrow(p[0], p[1], u[0], u[1], **style)



@contract(ps='array[Nx2]', ss='array[N]')
def plot_scalar_field_sign(pylab, ps, ss):
    """
        ps : list of 2D points
       s: associated scalar field
    """
    
    style = {}
    for p, s in zip(ps, ss):
        if s > 0:
            style['markerfacecolor'] = 'red'
        else:
            style['markerfacecolor'] = 'blue'
        
        pylab.plot(p[0], p[1], 'o', markersize=5, **style)



def plot_reference_points(pylab, processed):
    centroid = processed['centroid']
    sparse_xy = processed['sparse_xy']
    pylab.plot(sparse_xy[:, 0], sparse_xy[:, 1], 'o', zorder=(-1200),  # markeredgecolor='none',
               markerfacecolor=[0.3, 0.3, 0.3], markersize=0.5)
    pylab.plot(centroid[0], centroid[1], 'o', zorder=(-1000))

def plot_reference_points_poses(pylab, processed):

    arrow_length = 0.05
    style = dict(head_width=0.01, head_length=0.01,
                 edgecolor='green')
    
    for bd in processed['sparse']:
        extra = bd['extra'].item()
        p = extra['odom_xy']
        th = extra['odom_th']
        a = np.cos(th) * arrow_length        
        b = np.sin(th) * arrow_length
        pylab.arrow(p[0], p[1], a, b, **style)
