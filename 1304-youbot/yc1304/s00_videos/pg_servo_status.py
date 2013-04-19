import numpy as np
from procgraph import Block
from procgraph_mpl import PlotGeneric
from contracts import contract
from reprep.plot_utils.spines import turn_off_all_axes
from procgraph_mpl.plot_anim import PlotAnim
from procgraph.core.registrar_other import simple_block
from procgraph_images.solid import solid


STATE_WAIT = 'wait'
STATE_SERVOING = 'servoing'


class ServoStatus(Block):
    Block.alias('servo_status')

    Block.config('width', 'Image dimension', default=320)
    Block.config('height', 'Image dimension', default=240)
    
    Block.input('y')
    Block.input('y_goal')
    Block.input('state')
    
    Block.output('rgb')
    
    def init(self):
        self.plot_generic = PlotGeneric(width=self.config.width,
                                        height=self.config.height,
                                        transparent=False,
                                        tight=False,
                                        keep=True)
        self.first_timestamp = None
        self.plot_anim = PlotAnim()
        
    def update(self):
        if self.first_timestamp is None:
            self.first_timestamp = self.get_input_timestamp(0)
        self.time_since_start = self.get_input_timestamp(0) - self.first_timestamp
        
        self.output.rgb = self.plot_generic.get_rgb(self.plot)
        
        
    def plot(self, pylab):
        y = np.array(self.input.y.values)
        y_goal = np.array(self.input.y_goal.values)
        sensels = np.array(range(y.size))
        
        self.plot_anim.set_pylab(pylab)
        
        M = 0.1
        y_min = 0
        y_max = 1

        self.plot_anim.plot('y', sensels, y, 'k-')
        self.plot_anim.plot('y_goal', sensels, y_goal, 'g-')
        
        n = y.size
        pylab.axis((-1, n, y_min - M, y_max + M))
        turn_off_all_axes(pylab)
    
#         state = self.input.state.data

#         self.plot_anim.text('state', 1, 0.7, state)
        self.plot_anim.text('clock', 0, 1, '%5.2f' % self.time_since_start)

        
        # self.info('%10s %10s' % (self.time_since_start, self.servo_state))

@contract(y='array[N]', y_goal='array[N]')
def plot_servo_status(pylab, y, y_goal, y_min=0, y_max=1, M=0.1):
    pylab.plot(y_goal, 'k-')
    pylab.plot(y, 'g-')
    n = y.size
    pylab.axis((-1, n, y_min - M, y_max + M))
    
    turn_off_all_axes(pylab)



class ServoError(Block):
    """ 
        Captures the error since the start of the data.
    """
    Block.alias('servo_error')

    Block.config('width', 'Image dimension', default=320)
    Block.config('height', 'Image dimension', default=240)
    
    Block.input('y')
    Block.input('y_goal')
    Block.input('state')
    
    Block.output('rgb')
    
    def init(self):
        self.plot_generic = PlotGeneric(width=self.config.width,
                                        height=self.config.height,
                                        transparent=False,
                                        tight=False,
                                        keep=True)
        self.plot_anim = PlotAnim()
        self.timestamps = []
        self.ys = []
        self.y_goal = None
        self.servo_state = STATE_WAIT
        
        self.first_timestamp = None
        
        
        self.plot_line = None
        
    def update_values(self):
        if self.first_timestamp is None:
            self.first_timestamp = self.get_input_timestamp(0)
        self.time_since_start = self.get_input_timestamp(0) - self.first_timestamp

        
        state = self.input.state.data
        assert state in [STATE_WAIT, STATE_SERVOING]
        
        self.y_goal = np.array(self.input.y_goal.values)
        y = np.array(self.input.y.values)
        
        assert self.y_goal.shape == y.shape
        
        timestamp = self.get_input_timestamp(0)
        
        
        if self.servo_state == STATE_WAIT and state == STATE_SERVOING:
            # we started now
            self.timestamps = []
            self.ys = []
            self.info('%s: Started servoing' % self.time_since_start)
            
        if self.servo_state == STATE_SERVOING and state == STATE_WAIT:
            self.info('%s: Stopped servoing' % self.time_since_start)
            self.timestamps = []
            self.ys = []
        
        # only add values if we are servoing
        if state == STATE_SERVOING:
            self.timestamps.append(timestamp)
            self.ys.append(y)
    
        self.servo_state = state
        
    def get_relative_times(self):
        T = np.array(self.timestamps)
        if T.size > 0:
            T -= T[0]
        return T

    @contract(y0='array[N]', y1='array[N]')
    def metric(self, y0, y1):
        return np.linalg.norm(y0 - y1)
    
    def get_errors(self):
        es = [self.metric(self.y_goal, y) for y in self.ys]
        return np.array(es)
    
    def get_relative_errors(self):
        es = self.get_errors()
        if es.size > 0:
            es = es / es[0]
        return es
        
    def update(self):
        self.update_values()
        self.output.rgb = self.plot_generic.get_rgb(self.plot)
        
        
    def get_T(self, duration, chunk, min_time):
        duration = max(duration, min_time)
        T = np.ceil(duration / chunk) * chunk
        return T  
        
    def plot(self, pylab):
        ts = self.get_relative_times()
        es = self.get_relative_errors()
        assert ts.size == es.size
        
        self.plot_anim.set_pylab(pylab)
        
        if ts.size > 0:
            T = self.get_T(duration=(ts[-1] - ts[0]), chunk=5, min_time=15)
            assert T >= ts[-1]
        else:
            T = 10
        
        
        
        if self.plot_line is None:            
            ax1 = pylab.gca()
            ax1.axes.get_xaxis().set_visible(False)
            ax1.axes.get_yaxis().set_visible(False)
            self.plot_line = True
        
        border = 2
        pylab.axis((-1, T + border, -0.1, 1.3))

        self.plot_anim.text('clock', 0.7 * T, 1.2, '%5.2f' % self.time_since_start)
        self.plot_anim.plot('error', ts, es, 'k-')
        
        if es.size > 0:
            self.plot_anim.plot('error1', ts[0], es[0], 'rs')
            self.plot_anim.plot('error2', ts[-1], es[-1], 'rs')
        else:
            self.plot_anim.plot('error1', [], [], 'ro')
            self.plot_anim.plot('error2', [], [], 'ro')
        
        self.plot_anim.plot('zero', [0, T], [0, 0], 'k--')
            
        if self.servo_state == STATE_SERVOING:
            # self.info('Servoing')
            pass
        else:
            pass
            # self.info('Not servoing')
        
        # self.info('%10s %10s' % (self.time_since_start, self.servo_state))
        

@simple_block
def servo_state_indicator(state_msg, width=64, height=64):
    state = state_msg.data
    colors = {
              STATE_WAIT: [0, 0, 0],
              STATE_SERVOING: [255, 0, 0],
              None: [255, 255, 0]
              }
    
    color = colors.get(state, colors[None])
    
    return solid(width, height, color)
    
    



