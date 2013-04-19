from quickapp import QuickApp
from rosstream2boot.interfaces import ExpLogFromYaml
from yc1304.campaign import CampaignCmd, campaign_sub
import os
from procgraph.scripts.pgmain import pg


@campaign_sub
class MakeVideosServo(CampaignCmd, QuickApp):
    
    cmd = 'make-videos-servo'
    short = 'make-videos-servo --id_explog <log>'
    
    usage = """ Creates video for servo experiments """
    
    def define_options(self, params):
        params.add_string('id_explog', help='Which exp log to use', compulsory=True)

    def define_jobs_context(self, context):    
#         scan1 = '/scan_hokuyo_H1204906'
#         scan2 = '/scan_hokuyo_H1205005'
#         cam1 = '/cam_eye_right/image_raw/compressed'
#         cam2 = '/cam_back/image_raw/compressed'

        id_explog = self.get_options().id_explog
        rs2b_config = self.get_rs2b_config()
        log = rs2b_config.explogs.instance(id_explog)
        if not isinstance(log, ExpLogFromYaml):
            self.info('Skipping log %r because not raw log.' % id_explog)
            return
        
        
        bag = log.get_bagfile() 
        
        comp = context.comp
#         
#         def vname(id_video):
#             return os.path.join(context.get_output_dir(),
#                                 '%s.%s.mp4' % (id_explog, id_video))
        
        out_base = os.path.join(context.get_output_dir(), id_explog)
        comp(create_video_servo_multi, bag, out_base,
                                job_id='servo_multi')
        
        
#         comp(create_video_servo_error, bag, vname('servo_error'),
#              job_id='servo_error')
#         
        

def create_video_servo_multi(bag, out_base):
    if os.path.exists(out_base + '.fcpxml'):
        print('Already exists: %s' % out_base)
        return 
#         return out
#     out_base = os.path.splitext(out)[0]
    pg('video_servo_multi', config=dict(bag=bag, out_base=out_base))
    


def create_video_servo_error(bag, out):
    if os.path.exists(out):
        return out
    out_base = os.path.splitext(out)[0]
    pg('video_servo_error', config=dict(bag=bag, out_base=out_base))
    return out
