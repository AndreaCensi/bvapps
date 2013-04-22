from procgraph import pg
from quickapp import QuickApp
from rosstream2boot.interfaces.ros_log import ExpLogFromYaml
from yc1304.campaign import CampaignCmd, campaign_sub
import os
from procgraph_mplayer.scripts.find_background import find_background
from procgraph_pil.imwrite import imwrite
from yc1304.exps.exp_utils import iterate_context_explogs


param_hints = {
    'unicornA_base1_2013-04-03-16-36-03': dict(frames=[400, 20, 100, 150], perc=98.75, every=300),
    'unicornA_base1_2013-04-02-20-37-43': dict(frames=[20, 80, 150], perc=97, every=600),
    'unicornA_base1_2013-04-03-12-58-11': dict(frames=[20, 80, 150], perc=96.5, every=600),
    'unicornA_base1_2013-04-03-13-16-53': dict(frames=[300, 80, 150], perc=96.5, every=600),
    'unicornA_base1_2013-04-03-13-30-28': dict(frames=[300, 80, 150], perc=96.5, every=600),
    'default': dict(frames=[300, 80, 150], perc=96.5, every=600),
}



@campaign_sub
class MakeVideoSFX(CampaignCmd, QuickApp):
    
    cmd = 'video-sfx'
    
    def define_options(self, params):
        params.add_string('id_explog', help='Which exp log to use', compulsory=True)

    def define_jobs_context(self, context):    
        id_explog = self.get_options().id_explog
        rs2b_config = self.get_rs2b_config()
        log = rs2b_config.explogs.instance(id_explog)
        if not isinstance(log, ExpLogFromYaml):
            self.info('Skipping log %r because not raw log.' % id_explog)
            return
        
        outside = log.get_outside_movie()
        if outside is None:
            msg = ('"outside" movie not available for log %r' % id_explog)
            raise Exception(msg)
        
        hints = param_hints.get(id_explog, param_hints['default'])
        
        self.info('Using hints: %s' % hints)
        perc = hints['perc']
        every = hints['every']
        frames = hints['frames']
        comp = context.comp
        
        dirname = context.get_output_dir()
        if not os.path.exists(dirname):
            os.makedirs(dirname)
            
        def vname(id_video, ext='mp4'):
            return os.path.join(dirname, '%s.%s.%s' % (id_explog, id_video, ext))
        
        tmp_path = os.path.join(dirname, '%s.bg_transp.details' % id_explog)
        static_bg = comp(pg_video_background, video=outside, frames=frames, tmp_path=tmp_path,
                         out=vname('bg', 'png'), job_id='video_background')
        
        out_prefix = os.path.join(dirname, id_explog)
        comp(pg_video_bg_depth, video=outside, background=static_bg, perc=perc, every=every,
             out=out_prefix, job_id='bg_transp')


def pg_video_background(video, out, frames, tmp_path):
    if os.path.exists(out): 
        return out
    result = find_background(video, frames, debug=True, tmp_path=tmp_path)
    rgb = result['background']
    imwrite(rgb, out)
    return out

def pg_video_bg_depth(video, background, perc, every, out):
    if os.path.exists(out): 
        return out
    pg('video_bg_depth', config=dict(video=video, bg=background,
                                     perc=perc, every=every, out=out))
    return out
     
     
    
@campaign_sub
class MakeVideoSFXAll(CampaignCmd, QuickApp):
    
    cmd = 'video-sfx-all'
    short = 'Creates SFX videos for all explogs available.'
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):    
        config = self.get_rs2b_config()
        explogs = list(config.explogs.keys())     
        
        for c, id_explog in iterate_context_explogs(context, explogs):
            explog = config.explogs.instance(id_explog)
            if not isinstance(explog, ExpLogFromYaml):
                continue  # XX
            if explog.get_outside_movie() is None:
                continue
        
            c.subtask(MakeVideoSFX, id_explog=id_explog, add_job_prefix='', add_outdir='')
                                
        
