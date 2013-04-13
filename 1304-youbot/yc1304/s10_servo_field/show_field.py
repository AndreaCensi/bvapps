from geometry.poses import translation_from_SE3
from reprep import Report
from yc1304.campaign import CampaignCmd, campaign_sub
import numpy as np


@campaign_sub
class CreateField(CampaignCmd):
    cmd = 'create_field'
 
    def define_options(self, params):
        params.add_string('id_robot', help='', compulsory=True)
        params.add_string('id_episode', help='', compulsory=True)

    def define_jobs_context(self, context):
        options = self.get_options()

        id_robot = options.id_robot
        id_episode = options.id_episode
        
        data_central = self.get_data_central()
        
        all_data = context.comp(read_pose_observations, data_central, id_robot, id_episode)
        processed = context.comp(process, all_data)
        context.add_report(context.comp(report_raw_display, processed),
                           'raw_display', id_robot=id_robot, id_episode=id_episode)
    
def read_pose_observations(data_central, id_robot, id_episode):
    """ Returns a list of (timestamp, pose, observations) """
    data = []
    
    log_index = data_central.get_log_index()
    log_index.reindex()
    source = log_index.read_robot_episode(id_robot, id_episode, read_extra=True)
    for obs in source:
        timestamp = obs['timestamp']
        y = obs['observations']
        extra = obs['extra'].item()
        pose = np.array(extra['odom'])
        data.append((timestamp, pose, y))

    return data

def process(data):
    res = {}
    res['raw'] = data
    res['xy'] = [translation_from_SE3(pose)[:2] for _, pose, _ in data]    
    return res

def report_raw_display(processed):
    r = Report('raw_display')
    f = r.figure()
    xy = processed['xy']
    xy = np.array(xy).T  # 2 x N
    with f.plot('xy') as pylab:
        pylab.plot(xy[0, :], xy[1, :], '+')
        pylab.axis('equal')
    return r





