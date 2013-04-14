from quickapp.library.app.quickapp_imp import QuickApp
from rosstream2boot.programs.rs2b import RS2B
from . import CampaignCmd, campaign_sub
from yc1304.s10_servo_field import CreateField
from yc1304.exps.exp_utils import iterate_context_episodes

@campaign_sub
class Exp01(CampaignCmd, QuickApp):
    
    cmd = 'exp01'
    short = 'Test create_field'
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):    
        
        id_adapter = 'unicornA_base1_tw_hlhr_sane_s4'
        id_robot = 'uA_tran'
        test_episodes = [
            'unicornA_tran1_2013-04-12-22-29-16',
            'unicornA_tran1_2013-04-12-22-40-02',
            'unicornA_tran1_2013-04-11-23-21-36',
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
        
            self.call_recursive(c, 'create_field',
                            CreateField, dict(id_robot=id_robot,
                                              id_episode=id_episode),
                            extra_dep=jobs_convert)
        
