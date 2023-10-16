import numpy as np

from rlgym.utils import TerminalCondition, RewardFunction
from rlgym.utils.common_values import BALL_RADIUS
from rlgym.utils.gamestates import GameState, PlayerData
from rlgym.utils.reward_functions.common_rewards import ConstantReward
from rlgym.utils.state_setters import StateWrapper
from rlgym.utils.state_setters.random_state import RandomState, X_MAX, Y_MAX, PITCH_MAX, Z_MAX_BALL, YAW_MAX

MAX_CAR_HEIGHT = 62  # Slightly higher than Merc height at back
MIN_CAR_Z = 29  # Slightly below Batmobile z-coordinate (not top of car)


class BallOnGround(TerminalCondition):
    def reset(self, initial_state: GameState):
        pass

    def is_terminal(self, current_state: GameState) -> bool:
        # Check if bottom of ball is below car center of mass.
        # Technically this can be recovered from but there's no easy way to check for ball on ground.
        return current_state.ball.position[2] < BALL_RADIUS + MIN_CAR_Z


class DribbleReward(RewardFunction):
    def reset(self, initial_state: GameState):
        pass

    def get_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray) -> float:
        return 0

    def get_final_reward(self, player: PlayerData, state: GameState, previous_action: np.ndarray) -> float:
        return -1


class DribbleState(StateWrapper):
    def reset(self, state_wrapper: StateWrapper):
        car = state_wrapper.cars[0]
        car.set_pos(
            np.random.uniform(-X_MAX, X_MAX),
            np.random.uniform(-Y_MAX, Y_MAX),
            17,
        )
        car.set_rot(
            pitch=0,
            roll=0,
            yaw=np.random.uniform(-YAW_MAX, YAW_MAX)
        )
        r = np.random.normal(0, 10)
        theta = np.random.uniform(-np.pi, np.pi)
        eps_x, eps_y = r * np.cos(theta), r * np.sin(theta)
        state_wrapper.ball.set_pos(
            car.position[0] + eps_x,  # Displace a little bit so the ball is not balanced on the car
            car.position[1] + eps_y,
            MAX_CAR_HEIGHT + BALL_RADIUS,  # np.random.uniform(MAX_CAR_HEIGHT + BALL_RADIUS, Z_MAX_BALL)
        )
        theta = np.random.uniform(-np.pi, np.pi)
        eps_x, eps_y = r * np.cos(theta), r * np.sin(theta)
        state_wrapper.ball.set_lin_vel(
            x=eps_x,
            y=eps_y
        )


dribble_config = dict(
    reward_function=DribbleReward(),
    terminal_conditions=[BallOnGround()],
    state_setter=DribbleState(),
    team_size=1,
    spawn_opponents=False
)
