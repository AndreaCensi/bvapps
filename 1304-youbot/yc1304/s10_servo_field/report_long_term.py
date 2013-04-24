from boot_agents.bdse.agent.servo.bdse_servo_long_term import (get_distance_map,
    BDSEServoLongTerm)
from reprep import Report
from yc1304.s10_servo_field.plots import (plot_reference_points,
    plot_style_sensels)
import numpy as np
 
 
def report_long_term(processed, nsamples=6):
    r = Report('servo_details')
    slt = processed['servo_agent']
    if not isinstance(slt, BDSEServoLongTerm):
        r.text('warn', 'The report servo_details is only done for BDSEServoLongTerm.')
#     bdse_model = processed['servo_agent'].bdse_model
#     slt = BDSEServoLongTerm()
#     slt.set_model(bdse_model)
#     
    bds = processed['sparse']
    for i in range(nsamples):
        bd = bds[np.random.randint(len(bds))]
        name = 'sample%s' % i
        r_i = report_long_term_one(name, processed, bd, slt)
        r.add_child(r_i)
    return r



def report_long_term_one(name, processed, bd, slt):
    r = Report(name)
    f = r.figure(cols=4)
    
    y_goal = processed['bd_goal']['observations'].copy()
    y0 = bd['observations'].copy()
    
    extra = bd['extra'].item()
    p = extra['odom_xy']
    u = extra['u']
    
    
    with f.plot('map') as pylab:
        plot_reference_points(pylab, processed) 
        pylab.plot(p[0], p[1], 'r+')
        pylab.arrow(p[0], p[1], u[0], u[1])

    with f.plot('y0_vs_y_goal') as pylab:
        pylab.plot(y0, 'b-', label='y0')
        pylab.plot(y_goal, 'g-', label='ygoal')
        plot_style_sensels(pylab)   
        pylab.legend()

    D = get_distance_map(y0, y_goal)
    
    f.data('D', D).display('scale').add_to(f, caption='Distance matrix')
    
    plans = slt.find_best(y0, y_goal, limit=4)
    for p in plans:
        motion = slt.plans[p]
        ygoal1, ygoal1u = motion.predict_inverse(y_goal)
        R = motion.get_R()
        
        DR = D.copy()
        DR[R > 0] = np.nan

        ff = r.figure()
        ff.data('DR', DR).display('scale').add_to(ff, caption='DR')
        
        # with ff.plot('prediction1') as pylab:
        #     # pylab.plot(y0, label='y0')
        #     pylab.plot(y_goal, 'g-', label='ygoal')
        #     pylab.plot(y1, 'r-', label='y1')
        #     plot_style_sensels(pylab)   
        #     pylab.legend()
        
        known = ygoal1u > 0
        unknown = np.logical_not(known)
        
        sensels = np.array(range(y0.size))
        
        with ff.plot('prediction2') as pylab:
            pylab.plot(y0, 'b-', label='y0')
            pylab.plot(sensels[known], ygoal1[known], 'rs', label='ygoal1')
            pylab.plot(sensels[unknown], ygoal1[unknown], 'rx', label='ygoal1u')
            
            plot_style_sensels(pylab)   
            pylab.legend()
    
    return r


