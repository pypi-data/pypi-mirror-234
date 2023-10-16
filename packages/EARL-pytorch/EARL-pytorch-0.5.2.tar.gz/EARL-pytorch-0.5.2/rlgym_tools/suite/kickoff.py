import numpy as np

from rlgym.utils import RewardFunction
from rlgym.utils.common_values import BLUE_TEAM, BACK_WALL_Y
from rlgym.utils.gamestates import PlayerData, GameState


class KickoffReward(RewardFunction):
    def reset(self, initial_state: GameState):
        pass

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray) -> float:
        if player.team_num == BLUE_TEAM:
            player_data = player.car_data
            ball_data = state.ball
        else:
            player_data = player.inverted_car_data
            ball_data = state.inverted_ball
        return ball_data.position[1] / BACK_WALL_Y


class KickoffTerminal(RewardFunction):
    def reset(self, initial_state: GameState):
        pass

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray) -> float:
        pass


kickoff_config = dict(
    reward_function=ConstantReward(),
    terminal_conditions=[AirDribbleTerminal()],
    state_setter=AirDribbleState(),
    team_size=1,
    spawn_opponents=True
)
