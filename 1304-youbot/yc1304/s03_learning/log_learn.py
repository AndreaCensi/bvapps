#     bom -d out-boot_root learn-log -a bdse1 -r uA_b1_tw_hlhr_sane_s4 -p 2000
#     bom -d out-boot_root learn-log -a bdse1 -r uA_b1_tw_hlhr_sane_s4 --once
from yc1304.campaign import campaign_sub, CampaignCmd
from bootstrapping_olympics.programs.manager.meat.log_learn import learn_log


@campaign_sub
class LearnLog(CampaignCmd):
    cmd = 'learn-log'
    usage = 'learn-log -a <AGENT> -r <ROBOT> [--reset] [--publish interval] [--once]'
     
    '''
        Runs the learning for a given agent and log. 
        
        
        Running a live plugin:
         
            bom  [agent/robot options] --reset --dontsave --plugin dummy
         
    '''
     
    def define_options(self, params):
        params.add_string("agent", help="Agent ID", compulsory=True)
        params.add_string("robot", help="Robot ID", compulsory=True)
        params.add_flag("reset", help="Do not use cached state.")
        params.add_float("interval_publish", help="Publish debug information every N cycles.")
        params.add_flag("once", help="Just plot the published information and exit.")
        params.add_int("interval_save", default=300,
                          help="Interval for saving state (seconds)")
        params.add_int("interval_print", default=5,
                          help="Interval for printing stats (seconds)")
        params.add_flag("dontsave", help="Do not save the state of the agent.")
     
        params.add_string_list("plugin", default=[],
                          help="Run the specified plugin model during "
                               "learning. (eg, visualization)")
 
 
    def define_jobs_context(self, context):
        options = self.get_options()
        if options.interval_publish is None and not options.once:
            msg = 'Not creating any report; pass -p <interval> or --once to do it.'
            self.info(msg)
 
        data_central = self.get_data_central()
         
        context.comp(learn_log, data_central=data_central,
                  id_agent=options.agent,
                  id_robot=options.robot,
                  reset=options.reset,
                  publish_interval=options.interval_publish,
                  publish_once=options.once,
                  interval_save=options.interval_save,
                  interval_print=options.interval_print,
                  save_state=not(options.dontsave),
                  live_plugins=options.plugin)
