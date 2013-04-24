from . import CampaignCmd, campaign_sub
from quickapp.library.app.quickapp_imp import QuickApp
from rosstream2boot.programs.rs2b_convert import RS2BConvertOne
from yc1304.exps import good_logs_cf
from yc1304.exps.exp12 import merge_agents, save_state
from yc1304.exps.exp_utils import (iterate_context_episodes,
    iterate_context_agents_and_episodes, iterate_context_agents)
from yc1304.s03_learning.log_learn import PublishLearningResult, LearnLogNoSave
from yc1304.s10_servo_field.apps import ServoField
import warnings
 

def jobs_parallel_learning(context, data_central, id_agent, id_robot, episodes):
    """
    
        Needs:
        
            "episode-ready", id_robot, id_episode 
    """    
    agent = None
    i = 0
    for c, id_episode in iterate_context_episodes(context, episodes):
        i += 1
        c.needs('episode-ready', id_robot=id_robot, id_episode=id_episode)
         
        agent_i = c.subtask(LearnLogNoSave, agent=id_agent, robot=id_robot,
                            episodes=[id_episode],
                            add_job_prefix='')
        
        if agent is None:
            agent = agent_i
        else:
            agent = context.comp(merge_agents, agent, agent_i,
                                 job_id='merge-%d' % i) 
             
    save = context.comp(save_state, data_central, id_agent, id_robot, agent, episodes)
    
    return save


@campaign_sub
class Exp14(CampaignCmd, QuickApp):
    
    cmd = 'exp14'
    short = """ Cleaning up servo interface """
    comment = """ 
        
    """
    
    id_robot = 'exp14_uA_b1_xy_cf_strip'
    id_adapter = 'uA_b1_xy_cf_strip'
    agents = ['exp14_bdser_s1', 'exp14_bdser_s2', 'exp14_bdser_s3']
    
    warnings.warn('only one log')
         
    explogs_learn = good_logs_cf
    explogs_test = ['unicornA_tran1_2013-04-12-23-34-08']
    
    def define_options(self, params):
        pass
    
    def setup_rp_convert(self, rm):
        boot_root = self.get_boot_root()
        
        def rp_convert(context, id_robot, id_episode):
            id_explog = id_episode
            return context.subtask(RS2BConvertOne,
                                   boot_root=boot_root,
                                   id_explog=id_explog,
                                   id_adapter=Exp14.id_adapter,
                                   id_robot=id_robot,
                                   add_job_prefix='')
            
        rm.set_resource_provider('episode-ready', rp_convert)
        
    def setup_rp_learn(self, rm):
        data_central = self.get_data_central()
        
        def rp_learn(context, id_agent):
            return jobs_parallel_learning(context, data_central,
                                          id_agent, Exp14.id_robot,
                                          Exp14.explogs_learn)
        rm.set_resource_provider('agent-learn', rp_learn)
        

    def setup_rp(self, context):
        rm = context.get_resource_manager()
        self.setup_rp_convert(rm)
        self.setup_rp_learn(rm)
    
    def define_jobs_context(self, context):
        self.setup_rp(context)
             
        for c, id_agent in iterate_context_agents(context, Exp14.agents):
            c.needs('agent-learn', id_agent=id_agent)        
            c.subtask(PublishLearningResult, agent=id_agent, robot=Exp14.id_robot)
        
        cases = iterate_context_agents_and_episodes(context, Exp14.agents, Exp14.explogs_test)
        for c, id_agent, id_episode in cases:
            c.needs('agent-learn', id_agent=id_agent)
            c.needs('episode-ready', id_robot=Exp14.id_robot, id_episode=id_episode)
            c.subtask(ServoField, id_robot=Exp14.id_robot,
                      id_agent=id_agent, id_episode=id_episode)
 
        
        
        
        
