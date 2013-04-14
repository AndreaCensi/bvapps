from reprep import Report
 
def report_raw_display(processed):
    r = Report('raw_display')
    f = r.figure()

    xy = processed['raw_xy']
    centroid = processed['centroid']
    
    caption = "Raw trajectory and selected points"
    with f.plot('sparse_xy', caption=caption) as pylab:
        pylab.plot(xy[:, 0], xy[:, 1], 'k+')
#         pylab.plot(sparse_xy[:, 0], sparse_xy[:, 1], 'rs')
        pylab.plot(centroid[0], centroid[1], 'gs')
        plot_reference_points(pylab, processed)
        pylab.axis('equal')

    caption = "Selected points, drawn with poses"
    with f.plot('sparse_poses', caption=caption) as pylab:
        pylab.plot(xy[:, 0], xy[:, 1], 'k-')
        plot_reference_points_poses(pylab, processed)
        pylab.axis('equal')

    return r

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


def report_distances(processed):
    r = Report('distances')
    p_dist = processed['p_distance']
    y_dist = processed['y_distance']
    
    f = r.figure('distance_stats')
    #     with f.plot('p_dist_hist') as pylab:
    #         pylab.hist(p_dist)
    # 
    #     with f.plot('y_dist_hist') as pylab:
    #         pylab.hist(y_dist)

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
 
def report_servo1(processed):
    r = Report('servo1')
    f = r.figure()
     
    xy = processed['sparse_xy']
    bds = processed['sparse']
    
    with f.plot('u_raw_arrows') as pylab:
        plot_reference_points(pylab, processed)
        u_raw = get_extra_item(bds, 'u_raw')
        plot_servo_arrows(pylab, xy, u_raw)

    with f.plot('u_arrows') as pylab:
        plot_reference_points(pylab, processed)
        u = get_extra_item(bds, 'u')
        plot_servo_arrows(pylab, xy, u)

 
#     with f.plot('arrows_inverted') as pylab:
#         plot_reference_points(pylab, processed)
#         plot_servo_arrows_inverted(pylab, xy, commands)


    return r

import numpy as np

def plot_servo_arrows(pylab, ps, commands):
    """
        ps : list of 2D points
        commands: list of 2D commands
    """

    us = np.array(commands)[:, :2]
    print('norms: %s' % np.hypot(us[:, 0], us[:, 1]))
    u_max = np.max(np.hypot(us[:, 0], us[:, 1]))
    
    arrow_length = 0.1
    style = dict(head_width=0.01, head_length=0.01,
                 edgecolor='black')
    
    us = us / u_max * arrow_length
    print('u_max', u_max)
    for p, u in zip(ps, us):
        if np.hypot(u[0], u[1]) == 0:
            continue
        pylab.arrow(p[0], p[1], u[0], u[1], **style)




def plot_servo_arrows_inverted(pylab, ps, commands):
    us = np.array(commands)[:, :2]
    u_max = np.max(np.hypot(us[:, 0], us[:, 1]))
    
    arrow_length = 0.1
    style = dict(head_width=0.01, head_length=0.01,
                 edgecolor='black')
    
    us = us / u_max * arrow_length
    # print 'u_max', u_max
    for p, u in zip(ps, us):
        if np.hypot(u[0], u[1]) == 0:
            continue
        pylab.arrow(p[0], p[1], u[1], -u[0], **style)
