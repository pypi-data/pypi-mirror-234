from all.environments import MultiagentEnvironment, MultiagentPettingZooEnv

from rlgym.gym import Gym
from rlgym_tools.pettingzoo_utils import PettingZooEnv


def autonomous_env(env: Gym):
    return MultiagentPettingZooEnv(PettingZooEnv(env), name="rlgym_pettingzoo")


# class AutonomousEnv(MultiagentEnvironment):
#     def __init__(self, env: Gym):
#         self.env = env
#         self.
#
#     def reset(self):
#         return self.env.reset()
#
#     def step(self, action):
#         pass
#
#     def render(self, **kwargs):
#         pass
#
#     def close(self):
#         pass
#
#     def agent_iter(self):
#         pass
#
#     def last(self):
#         pass
#
#     def is_done(self, agent):
#         pass
#
#     @property
#     def name(self):
#         pass
#
#     @property
#     def state_spaces(self):
#         pass
#
#     @property
#     def action_spaces(self):
#         pass
#
#     @property
#     def device(self):
#         pass
