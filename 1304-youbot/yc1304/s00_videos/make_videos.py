from procgraph import pg
from quickapp import QuickApp
from rosstream2boot.interfaces import ExpLogFromYaml
from yc1304.campaign import CampaignCmd, campaign_sub
import os
from procgraph_mplayer import MPlayer
from yc1304.exps.exp_utils import iterate_context_explogs
from abc import abstractmethod
from yc1304.s00_videos.fcpx_index_dir import create_event_for_fcpx
from yc1304.s00_videos.fcpx_project import create_project_for_fcpx

scan1 = '/scan_hokuyo_H1204906'
scan2 = '/scan_hokuyo_H1205005'
cam1 = '/cam_eye_right/image_raw/compressed'
cam2 = '/cam_back/image_raw/compressed'

container = 'mp4'
# container = 'mkv'
# container = 'mov'

class CmdForLog(CampaignCmd, QuickApp):
    """ Commands that make something for one explog """
     
    def define_options(self, params):
        params.add_required_string('id_explog', help='Which exp log to use')        
    
    def define_jobs_context(self, context):
        self.context = context
        self.id_explog = self.get_options().id_explog
        self.explog = self.instance_explog(self.id_explog)
        
        self.define_jobs_video(context, self.id_explog, self.explog)
        
    @abstractmethod
    def define_jobs_video(self, context, id_explog, explog):
        raise NotImplementedError()
    
    def vname(self, id_video):
        """ Returns the filename for the video name. """    
        return os.path.join(self.context.get_output_dir(),
                            '%s.%s.%s' % (self.id_explog, id_video, container))
       
    def get_metadata(self):
        md = self.explog.get_metadata()
        # TODO: more stuff
        md['id_explog'] = self.id_explog
        return md
        
    
@campaign_sub
class MakeVideosCams(CmdForLog):
    
    short = 'Creates videos for cameras'
    cmd = 'make-videos2-cams'
    
    def define_jobs_video(self, context, id_explog, explog):  # @UnusedVariable
        bag = explog.get_bagfile() 
        video_cam_eye_right = self.vname('cam_eye_right')
        video_cam_back = self.vname('cam_back')
        
        md = self.get_metadata()
        md['sensor'] = cam1
        md['angle'] = 'cam_eye_right'
        context.comp(create_video_cam, bag, cam1, video_cam_eye_right, md=md, job_id='cam_eye_right')
        
        md = self.get_metadata()
        md['sensor'] = cam2
        md['angle'] = 'cam_back'
        context.comp(create_video_cam, bag, cam2, video_cam_back, md=md, job_id='cam_back')        

        context.checkpoint('creation')
        job_fcpx_index(context, self.context.get_output_dir(), id_explog) 
        
        
def job_fcpx_index(context, outdir, id_explog):
    """ Creates a job for index """
    event_name = id_explog + '-event'
    project_name = id_explog + '-project'
    event_filename = os.path.join(outdir, 'event.fcpxml')
    project_filename = os.path.join(outdir, 'project.fcpxml')
    pattern = '*.%s' % container
    context.comp(create_event_for_fcpx, dirname=outdir, pattern=pattern, event_filename=event_filename, event_name=event_name)
    context.comp(create_project_for_fcpx, dirname=outdir, pattern=pattern, project_filename=project_filename,
                 project_name=project_name, event_name=event_name)
    
    
@campaign_sub
class MakeVideosScans(CmdForLog):
    
    short = 'Creates videos for scans'
    cmd = 'make-videos2-scans'
    
    def define_jobs_video(self, context, id_explog, explog):  # @UnusedVariable
        bag = explog.get_bagfile() 
        video_scan1 = self.vname('scan1')
        video_scan2 = self.vname('scan2')
        md = self.get_metadata()
        md['sensor'] = scan1
        md['angle'] = 'scan1'
        context.comp(create_video_laser, bag, scan1, video_scan1, md=md, job_id='scan1')
        md['sensor'] = scan2
        md['angle'] = 'scan2'
        context.comp(create_video_laser, bag, scan2, video_scan2, md=md, job_id='scan2')

        context.checkpoint('creation')
        job_fcpx_index(context, self.context.get_output_dir(), id_explog) 


@campaign_sub
class MakeVideos2(CmdForLog):
    
    cmd = 'make-videos2'
    
    def define_options(self, params):
        params.add_required_string('id_explog', help='Which exp log to use')            

    def define_jobs_video(self, context, id_explog, explog):  # @UnusedVariable
        context.subtask(MakeVideosCams, id_explog=id_explog, add_job_prefix='cams', add_outdir='')
        context.subtask(MakeVideosScans, id_explog=id_explog, add_job_prefix='scans', add_outdir='')

        context.checkpoint('videos')
        video_cam_eye_right = self.vname('cam_eye_right')
        video_cam_back = self.vname('cam_back')
        video_scan1 = self.vname('scan1')
        video_scan2 = self.vname('scan2')
        video_all = self.vname('all')
        context.comp(join_four, video_cam_back, video_cam_eye_right,
                                video_scan1, video_scan2, video_all,
                     job_id='vall')
    
        context.checkpoint('creation')
        job_fcpx_index(context, self.context.get_output_dir(), id_explog) 


@campaign_sub
class MakeVideos2All(CampaignCmd, QuickApp):
    
    cmd = 'make-videos2-all'
    short = 'Creates a set of videos for all explogs available.'
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):    
        config = self.get_rs2b_config()
        explogs = list(config.explogs.keys())     
        
        for c, id_explog in iterate_context_explogs(context, explogs):
            c.subtask(MakeVideos2, id_explog=id_explog,
                      add_job_prefix='', add_outdir='')
            



@campaign_sub
class MakeVideos(CampaignCmd, QuickApp):
    
    cmd = 'make-videos-mix'
    
    def define_options(self, params):
        params.add_string('id_explog', help='Which exp log to use', compulsory=True)

    def define_jobs_context(self, context):    
        id_explog = self.get_options().id_explog
        rs2b_config = self.get_rs2b_config()
        log = rs2b_config.explogs.instance(id_explog)
        if not isinstance(log, ExpLogFromYaml):
            self.info('Skipping log %r because not raw log.' % id_explog)
            return
        
        bag = log.get_bagfile() 
        
        comp = context.comp
        
        def vname(id_video):
            return os.path.join(context.get_output_dir(),
                                '%s.%s.%s' % (id_explog, id_video, container))
        
        video_right = comp(create_video_cam, bag, cam1, vname('cam_eye_right'), job_id='cam_eye_right')
        video_back = comp(create_video_cam, bag, cam2, vname('cam_back'), job_id='cam_back')
        video_scan1 = comp(create_video_laser, bag, scan1, vname('scan1'), job_id='scan1')
        video_scan2 = comp(create_video_laser, bag, scan2, vname('scan2'), job_id='scan2')
    
        video_right_mean = comp(average, video_right, vname('cam_eye_right.mean'),
                                job_id='cam_eye_right-mean')
        video_back_mean = comp(average, video_back, vname('cam_back.mean'),
                               job_id='cam_back-mean')
    
        video_scan1_mean = comp(create_video_laser_mean, bag, scan1, vname('scan1.mean'),
                                job_id='scan1-mean')
        video_scan2_mean = comp(create_video_laser_mean, bag, scan2, vname('scan2.mean'),
                                job_id='scan2-mean')
        video_scan1_mean_n = comp(create_video_laser_mean_n, bag, scan1, vname('scan1.mean_n'),
                                  job_id='scan1-mean_n')
        video_scan2_mean_n = comp(create_video_laser_mean_n, bag, scan2, vname('scan2.mean_n'),
                                   job_id='scan2-mean_n')
    
        video_scan1_variance = comp(create_video_laser_variance, bag, scan1, vname('scan1.var'),
                                    job_id='scan1-var')
        video_scan2_variance = comp(create_video_laser_variance, bag, scan2, vname('scan2.var'),
                                    job_id='scan2-var')
    
        video_both = comp(join_two, video_back, video_right, vname('cams'),
                          job_id='cams')
        video_all = comp(join_four, video_back, video_right,
                         video_scan1, video_scan2, vname('all'),
                         job_id='all')
        video_all_mean = comp(join_four,
                                video_back_mean,
                                video_right_mean,
                                video_scan1_mean_n,
                                video_scan2_mean_n, vname('all.mean_n'),
                                job_id='all-mean_n')
        # video_all_mean = comp(average, video_all, vname('all.mean'))
        
        # TODO: check ok
        
        comp(create_video_servo_both, bag, vname('servo_both'),
                                job_id='servo_both')
        
        outside = log.get_outside_movie()
        if outside is not None:
            do_timestamps = comp(copy_first_timestamp, video_to=outside, video_from=video_all,
                                 job_id='outside_all_tosync_copy_first')
#             video_outside_all = comp(join_two_vert, outside, video_all, vname('outside_all'),
#                                      max_duration=6000000,
#                                      extra_dep=[do_timestamps],
#                                      job_id='outside_all')
            comp(join_two_vert, outside, video_all, vname('outside_all_tosync'),
                                     max_duration=60,
                                     extra_dep=[do_timestamps],
                                     job_id='outside_all_tosync')
            
            
        else:
            self.info('No outside found.')

    
@campaign_sub
class campaign_sub(CampaignCmd, QuickApp):
    
    cmd = 'make-videos-all'
    short = 'Creates a set of videos for all explogs available.'
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):    
        config = self.get_rs2b_config()
        explogs = list(config.explogs.keys())     
        
        for c, id_explog in iterate_context_explogs(context, explogs):
            c.subtask(MakeVideos, id_explog=id_explog)
            
            
            
            
def create_video_servo_both(bag, out):
    if os.path.exists(out):
        return out
     
    pg('video_servo_all', config=dict(bag=bag, out=out))
    
    return out


def copy_first_timestamp(video_to, video_from):
    """ Adds the timestamp of video2 to video1 """
    t1 = video_to + MPlayer.TIMESTAMPS_SUFFIX
    t2 = video_from + MPlayer.TIMESTAMPS_SUFFIX
    if os.path.exists(t1):
        print('Already created %r' % t1)
        return
    if not os.path.exists(t2):
        msg = 'Could not open reference timestamp %s' % t2
        raise Exception(msg)
    t2l1 = open(t2).readline()
    print('Read timestamp %r' % t2l1)
    assert not os.path.exists(t1)
    with open(t1, 'w') as f:
        f.write(t2l1)
    print('Written on %s' % t1)
    print()

def join_two_vert(video1, video2, out, max_duration):
    if not os.path.exists(out): 
        pg('join_two_vert', config=dict(video1=video1, video2=video2, max_duration=max_duration, out=out))
    return out

def create_video_laser_mean(bag, topic, out):
    if not os.path.exists(out): 
        pg('video_hokuyo_mean', config=dict(bag=bag, topic=topic, out=out))
    return out

def create_video_laser_mean_n(bag, topic, out):
    if not os.path.exists(out): 
        pg('video_hokuyo_mean_n', config=dict(bag=bag, topic=topic, out=out))
    return out


def create_video_laser_variance(bag, topic, out):
    if not os.path.exists(out): 
        pg('video_hokuyo_variance', config=dict(bag=bag, topic=topic, out=out))
    return out

def create_video_laser(bag, topic, out, md={}):
    if not os.path.exists(out): 
        pg('video_hokuyo', config=dict(bag=bag, topic=topic, out=out, md=md))
    return out

def join_two(video1, video2, out):
    if not os.path.exists(out): 
        pg('join_two', config=dict(video1=video1, video2=video2, out=out))
    return out


def join_four(video1, video2, video3, video4, out):
    print('video1: %s' % video1)
    print('video2: %s' % video2)
    print('video3: %s' % video3)
    print('video4: %s' % video4)
    if not os.path.exists(out): 
        config = dict(video1=video1, video2=video2,
                    video3=video3, video4=video4, out=out)
        pg('join_four', config=config)
    return out

def average(video, out):
    if not os.path.exists(out): 
        pg('video_average', config=dict(video=video, out=out))
    return out

def create_video_cam(bag, topic, out, md={}):
    if not os.path.exists(out): 
        import procgraph_ros  # @UnusedImport
        pg('video_cam', config=dict(bag=bag, topic=topic, out=out, md=md))
    return out
    
        
