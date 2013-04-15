from quickapp.library.app.quickapp_imp import QuickApp
from rosstream2boot.programs.rs2b import RS2B
from . import CampaignCmd, campaign_sub
from yc1304.s03_learning.log_learn import LearnLog
from yc1304.s10_servo_field.apps import ServoField
from yc1304.exps.exp_utils import iterate_context_episodes

@campaign_sub
class Exp07(CampaignCmd, QuickApp):
    
    cmd = 'exp07'
    short = """ Let's try robustified """
    comment = """  Works much better. Now let's try BDS. """

    #  bom -d out/boot-root -c yc1304  predict -r exp05_uA_xy -a exp07_bgdsr1
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):    
        id_agent = 'exp07_bgdsr1'
        
        id_robot = 'exp05_uA_xy'
        id_convert_job = 'exp05_uA_xy'
          
        jobs_convert = self.call_recursive(context, 'convert',
                       RS2B, ['--config', self.get_config_dirs()[0],  # XXX
                              '--dummy',
                              
                              'convert',
                              '--boot_root', self.get_boot_root(),
                              '--jobs', id_convert_job,
                              ])
 
        jobs_learn = context.subtask(LearnLog, agent=id_agent, robot=id_robot, interval_publish=500,
                                     extra_dep=jobs_convert.all_jobs())

        test_episodes = [
            'unicornA_tran1_2013-04-12-23-34-08'
        ]
        
        for c, id_episode in iterate_context_episodes(context, test_episodes):
            c.subtask(ServoField, id_robot=id_robot, id_agent=id_agent,
                                  variation='default',
                                  id_episode=id_episode,
                        extra_dep=jobs_learn.all_jobs())
 
