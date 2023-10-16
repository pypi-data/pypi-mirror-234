from typing import Optional, Union, List, Tuple, Any

import numpy as np
from gym import Env, Space
from gym.core import RenderFrame, ActType, ObsType
from gym.spaces import Box
from gym.vector import VectorEnv
from rlgym.envs import Match
from rlgym.gym import Gym
from rlgym.utils import ObsBuilder
from rlgym.utils.action_parsers import DefaultAction, ContinuousAction
from rlgym.utils.gamestates import PlayerData, GameState
from rlgym.utils.reward_functions.common_rewards import ConstantReward


class SimpleObs(ObsBuilder):
    def __init__(self, tick_skip):
        super().__init__()
        self.out = None
        self.tick_skip = tick_skip
        self.boost_pad_seconds_left = np.zeros((34,))

    def get_obs_space(self) -> Space:
        return Box(-np.inf, np.inf, (111,))

    def reset(self, initial_state: GameState):
        self.boost_pad_seconds_left = np.zeros((len(initial_state.boost_pads),))

    def pre_step(self, state: GameState):
        self.out = np.zeros((2 + len(state.boost_pads) + 9 +,))

        self.out[0] = state.blue_score
        self.out[1] = state.orange_score
        self.out[2:2 + len(state.boost_pads)] = self.boost_pad_seconds_left
        s = 2 + len(state.boost_pads)
        self.out[s:s + 3] = state.ball.position
        self.out[s + 3:s + 6] = state.ball.linear_velocity
        self.out[s + 6:s + 9] = state.ball.angular_velocity

        s += 9
        for player in state.players:
            self.out[s] = player.car_id
            self.out[s + 1] = player.team_num
            self.out[s + 2] = player.match_goals
            self.out[s + 3] = player.match_saves
            self.out[s + 4] = player.match_shots
            self.out[s + 5] = player.match_demolishes
            self.out[s + 6] = player.boost_pickups
            self.out[s + 7] = player.is_demoed
            self.out[s + 8] = player.on_ground
            self.out[s + 9] = player.ball_touched
            self.out[s + 10] = player.has_jump
            self.out[s + 11] = player.has_flip
            self.out[s + 12] = player.boost_amount

            self.out[s + 12: s + 15] = player.car_data.position
            self.out[s + 15: s + 18] = player.car_data.linear_velocity
            self.out[s + 18: s + 21] = player.car_data.angular_velocity
            self.out[s + 21: s + 24] = player.car_data.forward()
            self.out[s + 24: s + 27] = player.car_data.up()
            s += 27

        self.boost_pad_seconds_left = (self.boost_pad_seconds_left - self.tick_skip / 120)

    def build_obs(self, player: PlayerData, state: GameState, previous_action: np.ndarray) -> Any:
        return self.out


class BetterGym(VectorEnv, Gym):
    def __init__(self, tick_skip=6):
        match = Match(
            reward_function=ConstantReward(),
            terminal_conditions=[],
            obs_builder=SimpleObs(tick_skip),
            action_parser=ContinuousAction()
        )
        super(BetterGym, self).__init__()

    def reset(self, *, seed: Optional[int] = None, options: Optional[dict] = None) -> Tuple[ObsType, dict]:
        pass

    def reset_wait(self, seed: Optional[Union[int, List[int]]] = None, options: Optional[dict] = None):
        pass

    def step(self, action: ActType) -> Tuple[ObsType, float, bool, bool, dict]:
        pass

    def render(self) -> Optional[Union[RenderFrame, List[RenderFrame]]]:
        pass
