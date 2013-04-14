from quickapp.library.app.quickapp_imp import QuickApp
from rosstream2boot.programs.rs2b import RS2B
from . import CampaignCmd, campaign_sub
from yc1304.s03_learning.log_learn import LearnLog
from yc1304.s10_servo_field.apps import ServoField
from yc1304.exps.exp_utils import iterate_context_episodes

@campaign_sub
class Exp03(CampaignCmd, QuickApp):
    
    cmd = 'exp03'
    short = 'Testing with the good logs with clean laser data'
    
    comment = 'Strangely, I get 90deg error....'

    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):    
         
        id_agent = 'bdse1'
        id_robot = 'exp03_uA_tran'
        id_convert_job = 'exp03_uA_tran'
           
        jobs_convert = self.call_recursive(context, 'convert',
                       RS2B, ['--config', self.get_config_dirs()[0],  # XXX
                              '--dummy',
                              
                              'convert',
                              '--boot_root', self.get_boot_root(),
                              '--jobs', id_convert_job,
                              ])
 
        jobs_learn = context.subtask(LearnLog,
                                     agent=id_agent, robot=id_robot,
                                     interval_publish=5000,
                                     extra_dep=jobs_convert.all_jobs())

        test_episodes = [
            'unicornA_tran1_2013-04-12-23-34-08'
        ]
        
        for c, id_episode in iterate_context_episodes(context, test_episodes):
            c.subtask(ServoField, id_robot=id_robot, id_agent=id_agent,
                                  variation='default',
                                  id_episode=id_episode,
                        extra_dep=jobs_learn.all_jobs())
 
