from quickapp.library.app.quickapp_imp import QuickApp
from . import CampaignCmd, campaign_sub
from yc1304.s03_learning.log_learn import PublishLearningResult, LearnLog
from yc1304.s10_servo_field.apps import ServoField
from yc1304.exps.exp_utils import iterate_context_episodes, \
    iterate_context_explogs
from yc1304.exps import good_logs_cf
from rosstream2boot.programs.rs2b_convert import RS2BConvertOne
from bootstrapping_olympics.configuration.master import set_boot_config
from bootstrapping_olympics.programs.manager.meat.load_agent_state import load_agent_state
from reprep import Report
import itertools
from boot_agents.bdse.agent.servo.bdse_servo_long_term import myexp, \
    BDSEServoLongTerm
import warnings

@campaign_sub
class Exp13(CampaignCmd, QuickApp):
    
    cmd = 'exp13'
    short = """ Let's try with luminance strip"""
    comment = """ 
        kind of works for learning
    """
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, cc):    
        id_agent = 'exp13_bdser1'
        id_robot = 'exp13_uA_b1_tw_cf'
        id_adapter = 'uA_b1_tw_cf_strip'
        explogs_learn = good_logs_cf
        explogs_test = ['unicornA_tran1_2013-04-12-23-34-08']
        
        explogs_convert = explogs_learn + explogs_test
        for c, id_explog in iterate_context_explogs(cc, explogs_convert):
            c.subtask(RS2BConvertOne,
                        boot_root=self.get_boot_root(),
                        id_explog=id_explog,
                        id_adapter=id_adapter,
                        id_robot=id_robot)
         
        cc.checkpoint('conversion')

        cc.subtask(LearnLog, agent=id_agent, robot=id_robot, interval_publish=5000)

        cc.checkpoint('learning')
        
        cc.subtask(PublishLearningResult, agent=id_agent, robot=id_robot)

         
        test_episodes = explogs_test
        for c, id_episode in iterate_context_episodes(cc, test_episodes):
            c.subtask(ServoField, id_robot=id_robot, id_agent=id_agent,
                                  variation='default', id_episode=id_episode)
 
        data_central = self.get_data_central()
        
        cc.add_report(cc.comp(report_prediction,
                              data_central=data_central,
                              id_agent=id_agent,
                              id_robot=id_robot),
                      'prediction', id_agent=id_agent, id_robot=id_robot)

        cc.add_report(cc.comp(report_prediction2,
                              data_central=data_central,
                              id_agent=id_agent,
                              id_robot=id_robot),
                      'prediction2', id_agent=id_agent, id_robot=id_robot)


import numpy as np

# expm(A, q = 7)
# Compute the matrix exponential using Pade approximation of order q.
# 
# expm2(A)
# Compute the matrix exponential using eigenvalue decomposition.
# 
# expm3(A, q = 20)
# Compute the matrix exponential using a Taylor series.of order q.


def report_prediction2(data_central, id_agent, id_robot, exp=myexp): 
    set_boot_config(data_central.get_bo_config())
    agent, state = load_agent_state(data_central, id_agent, id_robot,
                                    reset_state=False, raise_if_no_state=True)
    model = agent.estimator.get_model()
    warnings.warn('does not work anymore')
    slt = BDSEServoLongTerm()
    slt.set_model(model)
    return  slt.report()
    
    
def report_prediction(data_central, id_agent, id_robot, exp=myexp): 
    set_boot_config(data_central.get_bo_config())
    agent, state = load_agent_state(data_central, id_agent, id_robot,
                                    reset_state=False, raise_if_no_state=True)
    
    r = Report('report-pred')
    f = r.figure()
    model = agent.estimator.get_model()
#     R = agent.estimator.y_stats.get_correlation()
    M = model.M
    N, _, K = M.shape 

#     W = np.eye(N)
    W = np.zeros((N, N))
    for i, j in itertools.product(range(N), range(N)):
        if np.abs(i - j) == 1:
            W[i, j] = 1
#     W = R * R * R * R * R
    f.data('W', W).display('posneg').add_to(f, caption='W')

    times = [0.25, 0.5, 1, 2, 4, 8, 16]
    for k in  range(K):
        A = M[:, :, k]
#         AW = A * W
#         AW = (AW - AW.T) / 2
        report_exp(r, 'k=%d' % k, A, times, exp=exp)
        report_exp(r, 'k=%dneg' % k, -A, times, exp=exp)
        

    for k1, k2 in itertools.product(range(K), range(K)):
        A = M[:, :, k1] + M[:, :, k2] 
        report_exp(r, 'k1=%d,k2=%d' % (k1, k2), A, times, exp=exp)
        

        
#     D1 = np.zeros((N, N))
#     for i, j in itertools.product(range(N), range(N)):
#         if i == j + 2:
#             D1[i, j] = 1
#         if i == j + 1:
#             D1[i, j] = 2
#         if i == j - 1:
#             D1[i, j] = -2
#         if i == j - 2:
#             D1[i, j] = -1
# 
#     report_exp(r, 'D1', D1, times, exp=exp)
    
    return r

def report_exp(r, name, A, times, exp):
    f = r.figure(name)
    
    f.data('A', A).display('posneg').add_to(f, caption='A')
    
    for i, t in enumerate(times):
        expiA = exp(t * A) 
        f.data('exp%dA' % i, expiA).display('scale').add_to(f, caption='t=%f' % t)


        
        
        
        
        
        
