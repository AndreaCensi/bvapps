from . import CampaignCmd, campaign_sub
from quickapp.library.app.quickapp_imp import QuickApp
from rosstream2boot.programs.rs2b import RS2B
from yc1304.exps.exp_utils import (iterate_context_episodes,
    iterate_context_agents)
from yc1304.s03_learning.log_learn import LearnLog, PublishLearningResult
from yc1304.s10_servo_field.apps import ServoField


@campaign_sub
class Exp09(CampaignCmd, QuickApp):
    
    cmd = 'exp09'
    short = """ Let's try the convergence ratio of the lyapunov function """
    comment = """ 

    """

    logs_to_learn = ['unicornA_base1_2013-04-11-20-14-27',
                    'unicornA_tran1_2013-04-11-23-21-36',
                    'unicornA_tran1_2013-04-12-22-29-16',
                    'unicornA_tran1_2013-04-12-22-40-02',
                    'unicornA_tran1_2013-04-12-23-34-08']

    agents = {}
    for i in range(1, 6):
        agents['exp09_bdser_%d' % i] = logs_to_learn[:i]
    
    id_robot = 'exp05_uA_xy'
    id_adapter = 'exp05_uA_xy'
         
    test_episodes = [
        'unicornA_tran1_2013-04-12-23-34-08'
    ]
        
        
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):            
        # let's convert all logs
        for id_explog in Exp09.logs_to_learn:
            self.call_recursive(context, 'convert',
                       RS2B, ['--config', self.get_config_dirs()[0],  # XXX
                              '--dummy',
                              'convert-one',
                              '--boot_root', self.get_boot_root(),
                              '--id_explog', id_explog,
                              '--id_adapter', Exp09.id_adapter,
                              '--id_robot', Exp09.id_robot,
                              ])
 
        # Everything before needs to be done before we do the rest
        context.checkpoint('conversion')
        
        for c, id_agent in iterate_context_agents(context, Exp09.agents):
            logs = Exp09.agents[id_agent]
            
            c.subtask(LearnLog, agent=id_agent, robot=Exp09.id_robot, episodes=logs,
                                interval_publish=5000)

            c.checkpoint('learning')
            
            c.subtask(PublishLearningResult, agent=id_agent, robot=Exp09.id_robot)
        
            for cc, id_episode in iterate_context_episodes(c, Exp09.test_episodes):
                cc.subtask(ServoField,
                           id_robot=Exp09.id_robot, id_agent=id_agent, id_episode=id_episode,
                           variation='default')
 
