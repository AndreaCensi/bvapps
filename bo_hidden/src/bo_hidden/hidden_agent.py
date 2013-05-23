from boot_agents.bds import BDSAgent
from boot_agents.bgds import BGDSAgent
from boot_agents.simple_stats.exp_switcher import ExpSwitcher


class Stage:
    def __init__(self, boot_spec):
        self.agent = BGDSAgent(beta=1)
        self.agent.init(boot_spec)
        self.commands = []
        self.cumulative_time = 0

    def process_observations(self, observations):
        self.cumulative_time += observations['dt'].item()

        self.agent.process_observations(observations)


class HiddenAgent(ExpSwitcher):

    def __init__(self, max_t=10):
        ExpSwitcher.__init__(self, beta=1)
        self.max_t = max_t

    def init(self, boot_spec):
        ExpSwitcher.init(self, boot_spec)

        self.boot_spec = boot_spec
        self.stages = []
        self.current_stage = Stage(self.boot_spec)

    def process_observations(self, observations):
        stage = self.current_stage

        stage.process_observations(observations)

        if stage.cumulative_time > self.max_t:
            self.info('Switching stage (%s)' % len(self.stages))
            self.stages.append(stage)
            self.current_stage = Stage(self.boot_spec)


    def publish(self, pub):

        for i, stage in enumerate(self.stages):
            bgds_estimator = stage.agent.bgds_estimator
            S = pub.section('s%s' % i)
            bgds_estimator.publish_compact(S) # XXX


