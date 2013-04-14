from . import process, read_pose_observations, report_raw_display
from yc1304.campaign import CampaignCmd, campaign_sub
from yc1304.s10_servo_field.show_field import compute_servo_action
from yc1304.s10_servo_field.reports import report_distances, report_servo1


@campaign_sub
class CreateField(CampaignCmd):
    cmd = 'create_field'
 
    def define_options(self, params):
        params.add_string('id_robot', help='', compulsory=True)
        params.add_string('id_episode', help='', compulsory=True)
        params.add_float('min_dist', help='Minimum distance for fake grid',
                         default=0.07)

    def define_jobs_context(self, context):
        options = self.get_options()

        id_robot = options.id_robot
        id_episode = options.id_episode
        min_dist = options.min_dist
        
        data_central = self.get_data_central()
        
        all_data = context.comp(read_pose_observations, data_central, id_robot, id_episode)
        processed = context.comp(process, all_data, min_dist)
        context.add_report(context.comp(report_raw_display, processed),
                           'raw_display', id_robot=id_robot, id_episode=id_episode)
        context.add_report(context.comp(report_distances, processed),
                           'distances', id_robot=id_robot, id_episode=id_episode)
    
        keys = dict(id_robot=id_robot, id_episode=id_episode)
        
        reports = {'distances': report_distances,
                   'raw_display': report_raw_display}
        
        for k, v in reports.items(): 
            context.add_report(context.comp(v, processed), k, **keys)
    


@campaign_sub
class ServoField(CampaignCmd):
    cmd = 'servo_field'
 
    def define_options(self, params):
        params.add_string('id_robot', help='', compulsory=True)
        params.add_string('id_episode', help='', compulsory=True)
        params.add_string('id_agent', help='', compulsory=True)
#         params.add_string('id_robot_learn', help='', compulsory=True)
        params.add_string('variation', help='', compulsory=True)
        params.add_float('min_dist', help='Minimum distance for fake grid',
                         default=0.07)

    def define_jobs_context(self, context):
        options = self.get_options()

        id_agent = options.id_agent
        variation = options.variation
        id_robot = options.id_robot
#         id_robot_learn = options.id_robot_learn
        
        id_episode = options.id_episode
        min_dist = options.min_dist
        
        data_central = self.get_data_central()
        
        all_data = context.comp(read_pose_observations, data_central, id_robot, id_episode)
        processed = context.comp(process, all_data, min_dist)
        processed2 = context.comp(compute_servo_action, processed, data_central,
                                  id_agent, id_robot, variation)
        
        keys = dict(id_robot=id_robot, id_episode=id_episode)
        
        reports = {'distances': report_distances,
                   'servo1': report_servo1,
                   'raw_display': report_raw_display}
        
        for k, v in reports.items(): 
            context.add_report(context.comp(v, processed2), k, **keys)
    



