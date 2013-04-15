from procgraph import pg
from quickapp import QuickApp
from rosstream2boot.interfaces.ros_log import ExpLogFromYaml
from yc1304.campaign import CampaignCmd, campaign_sub
import os
from procgraph_mplayer.mplayer import MPlayer


@campaign_sub
class MakeVideos(CampaignCmd, QuickApp):
    
    cmd = 'make-videos'
    
    def define_options(self, params):
        params.add_string('id_explog', help='Which exp log to use', compulsory=True)

    def define_jobs_context(self, context):    
        scan1 = '/scan_hokuyo_H1204906'
        scan2 = '/scan_hokuyo_H1205005'
        cam1 = '/cam_eye_right/image_raw/compressed'
        cam2 = '/cam_back/image_raw/compressed'

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
                                '%s.%s.mp4' % (id_explog, id_video))
        
        video_right = comp(create_video_cam, bag, cam1, vname('cam_eye_right'))
        video_back = comp(create_video_cam, bag, cam2, vname('cam_back'))
        video_scan1 = comp(create_video_laser, bag, scan1, vname('scan1'))
        video_scan2 = comp(create_video_laser, bag, scan2, vname('scan2'))
    
        video_right_mean = comp(average, video_right, vname('cam_eye_right.mean'))
        video_back_mean = comp(average, video_back, vname('cam_back.mean'))
    
        video_scan1_mean = comp(create_video_laser_mean, bag, scan1, vname('scan1.mean'))
        video_scan2_mean = comp(create_video_laser_mean, bag, scan2, vname('scan2.mean'))
        video_scan1_mean_n = comp(create_video_laser_mean_n, bag, scan1, vname('scan1.mean_n'))
        video_scan2_mean_n = comp(create_video_laser_mean_n, bag, scan2, vname('scan2.mean_n'))
    
        video_scan1_variance = comp(create_video_laser_variance, bag, scan1, vname('scan1.var'))
        video_scan2_variance = comp(create_video_laser_variance, bag, scan2, vname('scan2.var'))
    
        video_both = comp(join_two, video_back, video_right, vname('cams'))
        video_all = comp(join_four, video_back, video_right,
                        video_scan1, video_scan2, vname('all'))
        video_all_mean = comp(join_four,
                            video_back_mean,
                            video_right_mean,
                            video_scan1_mean_n,
                            video_scan2_mean_n, vname('all.mean_n'))
        # video_all_mean = comp(average, video_all, vname('all.mean'))
        
        outside = log.get_outside_movie()
        if outside is not None:
            do_timestamps = comp(copy_first_timestamp, video_to=outside, video_from=video_all)
#             video_outside_all = comp(join_two_vert, outside, video_all, vname('outside_all'),
#                                      max_duration=6000000,
#                                      extra_dep=[do_timestamps],
#                                      job_id='outside_all')
            video_outside_all = comp(join_two_vert, outside, video_all, vname('outside_all_tosync'),
                                     max_duration=60,
                                     extra_dep=[do_timestamps],
                                     job_id='outside_all_tosync')
            
            
        else:
            self.info('No outside found.')

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

def create_video_laser(bag, topic, out):
    if not os.path.exists(out): 
        pg('video_hokuyo', config=dict(bag=bag, topic=topic, out=out))
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

def create_video_cam(bag, topic, out):
    if not os.path.exists(out): 
        import procgraph_ros
        pg('bag2mp4', config=dict(bag=bag, topic=topic, out=out))
    return out
    
    
@campaign_sub
class campaign_sub(CampaignCmd, QuickApp):
    
    cmd = 'make-videos-all'
    short = 'Creates a set of videos for all explogs available.'
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):    
        config = self.get_rs2b_config()
        explogs = list(config.explogs.keys())     
        
        for i, id_explog in enumerate(explogs):
            # TODO: user better names
            self.call_recursive(context, 'log%s' % i,
                                MakeVideos, dict(id_explog=id_explog))
        
