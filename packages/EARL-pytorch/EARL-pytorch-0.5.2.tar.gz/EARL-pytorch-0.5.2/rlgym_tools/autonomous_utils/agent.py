import numpy as np
from all.agents import PPO
from all.bodies import Body


class RLBody(Body):
    def __init__(self, agent, n=3):
        super().__init__(agent)
        self.n = n

    def process_action(self, action):
        actions = np.copy(action)
        actions[..., :5] = 2 * actions[..., :5] / (self.n - 1) - 1
        return actions
