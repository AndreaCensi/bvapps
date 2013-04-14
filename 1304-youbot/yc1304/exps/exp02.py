from quickapp.library.app.quickapp_imp import QuickApp
from rosstream2boot.programs.rs2b import RS2B
from . import CampaignCmd, campaign_sub
from yc1304.s10_servo_field.apps import ServoField
from yc1304.exps.exp_utils import iterate_context_episodes

@campaign_sub
class Exp02(CampaignCmd, QuickApp):
    
    cmd = 'exp02'
    short = 'Testing with servo agent'
    
    comment = """ This shows that there was something wrong with learning. """
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):    
        
        id_adapter = 'unicornA_base1_tw_hlhr_sane_s4'
        
        
        id_agent = 'bdse1'
        id_robot = 'uA_b1_tw_hlhr_s4'
            
        variation = 'default'
        
        test_episodes = [ 
            'unicornA_tran1_2013-04-12-23-34-08'
        ]
        
        for c, id_episode in iterate_context_episodes(context, test_episodes):               
            id_explog = id_episode
            jobs_convert = self.call_recursive(c, 'convert',
                                   RS2B, ['--config', self.get_config_dirs()[0],  # XXX
                                          '--dummy',
                                          
                                          'convert-one',
                                          '--boot_root', self.get_boot_root(),
                                          '--id_explog', id_explog,
                                          '--id_adapter', id_adapter,
                                          '--id_robot', id_robot])
        
            self.call_recursive(c, 'servo_field',
                            ServoField, dict(id_robot=id_robot,
                                            id_agent=id_agent,
                                             variation=variation,
                                             id_episode=id_episode),
                            extra_dep=jobs_convert)
        
