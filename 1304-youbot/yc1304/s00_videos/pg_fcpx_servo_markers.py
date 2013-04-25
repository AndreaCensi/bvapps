from procgraph import Block
import os

STATE_WAIT = 'wait'
STATE_SERVOING = 'servoing'


class FCPXServoMarkers(Block):
    """ 
        Creates Final Cut Pro X xml project for the servo videos
    """
    Block.alias('servo_fcpx_project')
    
    Block.config('out_base')
    
    Block.input('state')
    
    Block.output('rgb')
    
    def init(self):
        self.servo_state = STATE_WAIT
        self.first_timestamp = None
        
        self.servo_sequences = []
        self.timestamps = []
    
    def update(self):
        timestamp = self.get_input_timestamp(0)
        if timestamp is None:
            self.info('None timestamp?: %s' % timestamp)
            return
#         assert timestamp is not None
        
        if self.first_timestamp is None:
            self.info('first timestamp: %s' % timestamp)
            self.first_timestamp = timestamp
            
        state = self.input.state.data
        assert state in [STATE_WAIT, STATE_SERVOING]
        
        if self.servo_state == STATE_WAIT and state == STATE_SERVOING:
            # we started now
            self.timestamps = []
            # self.ys = []
            # self.info('%s: Started servoing' % self.time_since_start)
            
        if self.servo_state == STATE_SERVOING and state == STATE_WAIT:
            # self.info('%s: Stopped servoing' % self.time_since_start)
            self.servo_sequences.append(self.timestamps)
            self.timestamps = []
            
#             if self.first_timestamp is not None:
#                 xml = self.get_project_xml('myproj')
#                 print xml

        # only add values if we are servoing
        if state == STATE_SERVOING:
            self.timestamps.append(timestamp)
    
        self.servo_state = state
    

    def get_servo_sequences_xml(self):
        s = ""
        for i, timestamps in enumerate(self.servo_sequences):
            start = timestamps[0]
            end = timestamps[-1]
            duration = end - start
#             s += self.get_marker_xml(start=start, duration=duration, value='Servo %d' % i)
            s += self.get_marker_xml(start=start, duration=duration, value='Servo %d - start' % i)
            s += self.get_marker_xml(start=end, duration=None, value='Servo %d - end' % i)
        return s
    
    def get_marker_xml(self, start, duration, value):
        if duration is None:
            fc_duration = "1001/30000s"
        else:
            fc_duration = get_fc_time(duration) 
        
        fc_start = get_fc_time(start - self.first_timestamp)
        tm = '<marker start="%s" duration="%s" value=%r/>' % (fc_start, fc_duration, value)
        
        return tm + '\n'
    
    def finish(self):
        base = os.path.basename(self.config.out_base)
        proj_name = base
        xml = self.get_project_xml(proj_name)
        proj = self.config.out_base + '.fcpxml'
        with open(proj, 'w') as f:
            f.write(xml)
        self.info('writing to %s' % proj)
        print xml
        
    
    def get_clip_xml(self, name, duration):
        v = dict(name=name, duration=duration, markers=self.get_servo_sequences_xml())
        return """
          <clip name="{name}"  duration='{duration}' format="r1">
              <video ref="{name}"  duration='{duration}'>
              </video>
              {markers}
          </clip>
        """.format(**v)
        
    def get_asset_xml(self, name, filename):
        return  """ 
          <asset id="{name}" src="{filename}"/>
        """.format(name=name, filename=filename)

    def get_project_xml(self, name):
        duration = get_fc_time(self.get_input_timestamp(0) - self.first_timestamp) 
        out_base = self.config.out_base
        assets = ""
        clips = ""
        
        for video in ['servo_status', 'servo_error', 'servo_indicator']:
            filename = '%s.%s.mp4' % (out_base, video)
            # filename = os.path.realpath(filename)
            assets += self.get_asset_xml(video, filename)
            clips += self.get_clip_xml(video, duration)
        
        template = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.2">
<project name="{name}">
          
          <resources>
              <format id="r1" frameDuration="1001/30000s" width="320" height="240"/>
              {assets}
          </resources>
        
            {clips}
</project>
</fcpxml>
        """
        s = template.format(name=name, assets=assets, clips=clips)
        return s
    
    
    
     
def get_fc_time(t):
    units = 30000
    num = int(t * units)
    den = units
    return '%d/%ds' % (num, den)

