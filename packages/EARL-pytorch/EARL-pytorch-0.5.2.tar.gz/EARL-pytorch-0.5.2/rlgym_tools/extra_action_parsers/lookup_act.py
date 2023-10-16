from typing import Any

import gym
import numpy as np
from gym.spaces import Discrete
from rlgym.utils.action_parsers import ActionParser
from rlgym.utils.gamestates import GameState


class LookupAction(ActionParser):
    def __init__(self, bins=None):
        super().__init__()
        if bins is None:
            self.bins = [(-1, 0, 1)] * 5
        elif isinstance(bins, int):
            assert bins % 2 == 1, "Need an odd number of bins"
            self.bins = [tuple(np.linspace(-1, 1, bins))] * 5
        elif isinstance(bins[0], (float, int)):
            self.bins = [bins] * 5
        else:
            assert len(bins) == 5, "Need bins for throttle, steer, pitch, yaw and roll"
            self.bins = bins
        self.lookup_table = self.make_lookup_table(self.bins)

    @staticmethod
    def make_lookup_table(bins):
        actions = []
        # Ground
        for throttle in bins[0]:
            for steer in bins[1]:
                for boost in (0, 1):
                    for handbrake in (0, 1):
                        if boost == 1 and throttle != 1:
                            continue
                        actions.append([throttle or boost, steer, 0, steer, 0, 0, boost, handbrake])
        # Aerial
        for pitch in bins[2]:
            for yaw in bins[3]:
                for roll in bins[4]:
                    for jump in (0, 1):
                        for boost in (0, 1):
                            if jump == 1 and yaw != 0:
                                continue  # Only need roll for sideflip
                            if pitch == roll == jump == 0:
                                continue  # Duplicate with ground

                            is_flip = jump == 1 and not pitch == roll == 0
                            if is_flip and abs(pitch) != 1 and abs(roll) != 1:
                                continue  # Deadzone is inconsistent, only allow flips if pitch/yaw is fully pressed

                            handbrake = is_flip  # Enable handbrake for potential wavedashes
                            actions.append([boost, yaw, pitch, yaw, roll, jump, boost, handbrake])
        actions = np.array(actions)
        return actions

    def get_action_space(self) -> gym.spaces.Space:
        return Discrete(len(self.lookup_table))

    def parse_actions(self, actions: Any, state: GameState) -> np.ndarray:
        indexes = np.array(actions, dtype=np.int32)
        indexes = np.squeeze(indexes)
        return self.lookup_table[indexes]
