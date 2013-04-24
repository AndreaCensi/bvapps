from . import CampaignCmd, campaign_sub
from bootstrapping_olympics.agent_states.learning_state import LearningState
from quickapp.library.app.quickapp_imp import QuickApp
from rosstream2boot.programs.rs2b_convert import RS2BConvertOne
from yc1304.exps import good_logs_cf
from yc1304.exps.exp_utils import (iterate_context_episodes,
    iterate_context_explogs)
from yc1304.s03_learning.log_learn import PublishLearningResult, LearnLogNoSave
from yc1304.s10_servo_field.apps import ServoField
from bootstrapping_olympics.interfaces.agent import AgentInterface
from contracts import contract
from bootstrapping_olympics.programs.manager.meat.data_central import DataCentral


def merge_agents(agent1, agent2):
    print('merging')
    agent1.merge(agent2)
    return agent1

@contract(data_central=DataCentral, id_agent='str', id_robot='str', agent=AgentInterface,
          id_episodes='list(str)')
def save_state(data_central, id_agent, id_robot, agent, id_episodes):
    state = LearningState(id_robot=id_robot, id_agent=id_agent)
    state.agent_state = agent.get_state()
    state.id_episodes = set(id_episodes)
    db = data_central.get_agent_state_db() 
    db.set_state(state=state, id_robot=id_robot, id_agent=id_agent)


# def jobs_parallel_convert
#       agent = None
#         for c, id_explog in iterate_context_explogs(context, explogs_convert):
#             episodes = c.subtask(RS2BConvertOne,
#                                    boot_root=self.get_boot_root(),
#                                    id_explog=id_explog,
#                                    id_adapter=id_adapter,
#                                    id_robot=id_robot)
#         
#             if id_explog in explogs_learn:
#                 agent_i = c.subtask(LearnLogNoSave, agent=id_agent, robot=id_robot,
#                                     episodes=episodes)
#                 if agent is None:
#                     agent = agent_i
#                 else:
#                     agent = context.comp(merge_agents, agent, agent_i) 
#             
#         id_episodes = explogs_learn
#         data_central = self.get_data_central()
#         context.comp(save_state, data_central, id_agent, id_robot, agent, id_episodes)
#  

@campaign_sub
class Exp12(CampaignCmd, QuickApp):
    
    cmd = 'exp12'
    short = """ Parallel learning """
    comment = """ 

    """
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):    
        id_agent = 'exp10_bdser1'
        
        id_robot = 'exp12_uA_b1_tw_cf'
        id_adapter = 'uA_b1_tw_cf'
        
        explogs_learn = good_logs_cf
        explogs_test = ['unicornA_tran1_2013-04-12-23-34-08']        
        explogs_convert = explogs_learn + explogs_test

        agent = None
        for c, id_explog in iterate_context_explogs(context, explogs_convert):
            episodes = c.subtask(RS2BConvertOne,
                                   boot_root=self.get_boot_root(),
                                   id_explog=id_explog,
                                   id_adapter=id_adapter,
                                   id_robot=id_robot)
        
            if id_explog in explogs_learn:
                agent_i = c.subtask(LearnLogNoSave, agent=id_agent, robot=id_robot,
                                    episodes=episodes)
                if agent is None:
                    agent = agent_i
                else:
                    agent = context.comp(merge_agents, agent, agent_i) 
            
        id_episodes = explogs_learn
        data_central = self.get_data_central()
        context.comp(save_state, data_central, id_agent, id_robot, agent, id_episodes)
            

        context.checkpoint('learning')
        
        context.subtask(PublishLearningResult, agent=id_agent, robot=id_robot)

         
        test_episodes = [
            'unicornA_tran1_2013-04-12-23-34-08'
        ]
         
        for c, id_episode in iterate_context_episodes(context, test_episodes):
            c.subtask(ServoField, id_robot=id_robot, id_agent=id_agent,
                                  variation='default', id_episode=id_episode)
 
