from bootstrapping_olympics import StreamSpec
from contracts import contract
from geometry import (SE3, se3, SE3_from_SE2, angle_from_SE2,
    SE2_from_translation_angle, SE2_from_SE3, ProductManifold)
from vehicles.library.dynamics import CircleVel, SE2Dynamics
import numpy as np
from vehicles import Dynamics


class BaseTopDynamics(Dynamics):

    last_turret_angle = 0.0

    @contract(base=Dynamics, top=Dynamics)
    def __init__(self, base, top):
        self.base = base
        self.top = top

        cmd1 = StreamSpec.from_yaml(self.base.get_commands_spec())
        cmd2 = StreamSpec.from_yaml(self.top.get_commands_spec())

        cmd_spec = StreamSpec.join(cmd1, cmd2).to_yaml()

        components = [self.base.get_state_space(),
                      self.top.get_state_space()]
        state_space = ProductManifold(components)
        Dynamics.__init__(self, commands_spec=cmd_spec,
                          state_space=state_space)

    @contract(pose='SE3')
    def pose2state(self, pose):
        ''' 
            Returns the state that best approximates 
            the given pose (in SE3).
        '''
        # random_angle = SO2.convert_to(SE3, SO2.sample_uniform()) # XXX
#        random_angle = SE3_from_SE2(SE2_from_SO2(SO2.sample_uniform()))

        # angle = BaseTopDynamics.last_turret_angle
        angle = np.random.rand() * np.pi * 2
        turret_pose = SE3_from_SE2(SE2_from_translation_angle([0, 0], angle))
        # print('Starting at %s deg ' % np.rad2deg(angle))
        return self.compose_state(base=self.base.pose2state(pose),
                                  top=self.top.pose2state(turret_pose))

    @contract(commands='array[4]')
    def _integrate(self, state, commands, dt):
        cmd1 = commands[:3]
        cmd2 = np.array([commands[3]])

        base_state = self.base_state_from_big_state(state)
        top_state = self.top_state_from_big_state(state)

        base_state2 = self.base.integrate(base_state, cmd1, dt)
        top_state2 = self.top.integrate(top_state, cmd2, dt)

        stateb = self.compose_state(base=base_state2, top=top_state2)

        # Save angle
        q, _ = self.top.joint_state(top_state2)
        BaseTopDynamics.last_turret_angle = angle_from_SE2(SE2_from_SE3(q))
        # print('angle: %s deg ' % np.rad2deg(Turret.last_turret_angle))
        # print('new state:\n%s' % self.print_state(stateb))
        return stateb

    def base_state_from_big_state(self, state):
        return state['base']

    def top_state_from_big_state(self, state):
        return state['top']

    def compose_state(self, base, top):
        return dict(base=base, top=top)

    def state_to_yaml(self, state):
        ''' Converts the state to a YAML representation.'''
        base_state = self.base_state_from_big_state(state)
        top_state = self.top_state_from_big_state(state)
        s = {}
        s['base'] = self.base.state_to_yaml(base_state)
        s['top'] = self.top.state_to_yaml(top_state)
        return s

    def num_joints(self):
        return 2

    @contract(returns='tuple(SE3, se3)')
    def joint_state(self, state, joint=0):
        base_state = self.base_state_from_big_state(state)
        top_state = self.top_state_from_big_state(state)
        conf = self.base.joint_state(base_state, 0)
        body_pose, body_vel = conf
        if joint == 0:
            # print('here: %s' % describe_value(conf))
            return body_pose, body_vel
        elif joint == 1:
            # FIXME: velocity not computed
            q, _ = self.top.joint_state(top_state)
            j = SE3.multiply(body_pose, q)
            jvel = se3.zero()  # @UndefinedVariable
            conf2 = j, jvel
            # print('there: %s' % describe_value(conf2))
            return conf2
        else:
            raise ValueError('No such joint %d.' % joint)


class Turret(BaseTopDynamics):

    @contract(max_linear_velocity='seq[2](>=0)',
              max_angular_velocity='>=0',)
    def __init__(self, max_linear_velocity, max_angular_velocity,
                       max_turret_velocity):
        base = SE2Dynamics(max_linear_velocity=max_linear_velocity,
                                max_angular_velocity=max_angular_velocity)
        top = CircleVel(max_velocity=max_turret_velocity)

        BaseTopDynamics.__init__(self, base=base, top=top)


