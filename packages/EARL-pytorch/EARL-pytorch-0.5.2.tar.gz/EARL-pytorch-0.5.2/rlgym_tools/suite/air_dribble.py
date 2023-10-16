import numpy as np

from rlgym.utils import TerminalCondition
from rlgym.utils.common_values import BALL_RADIUS
from rlgym.utils.gamestates import GameState
from rlgym.utils.reward_functions.common_rewards import ConstantReward
from rlgym.utils.state_setters import StateWrapper
from rlgym.utils.state_setters.random_state import RandomState, CAR_MARGIN, X_MAX, Y_MAX, ROLL_MAX, PITCH_MAX, YAW_MAX, \
    Z_MAX_BALL, Z_MAX_CAR
from rlgym_tools.suite.dribble import DribbleState, DribbleReward


class AirDribbleTerminal(TerminalCondition):
    def reset(self, initial_state: GameState):
        pass

    def is_terminal(self, current_state: GameState) -> bool:
        return not CAR_MARGIN <= current_state.players[0].car_data.position[2] <= current_state.ball.position[2]


class AirDribbleState(StateWrapper):
    def reset(self, state_wrapper: StateWrapper):
        car = state_wrapper.cars[0]
        car.set_pos(
            0,
            0,
            np.random.uniform(CAR_MARGIN, Z_MAX_CAR - 2 * BALL_RADIUS),
        )
        car.set_rot(
            pitch=np.pi / 2,
            roll=np.random.uniform(-ROLL_MAX, ROLL_MAX),
            yaw=np.random.uniform(-YAW_MAX, YAW_MAX)
        )
        r = np.random.normal(0, 10)
        theta = np.random.uniform(-np.pi, np.pi)
        eps_x, eps_y = r * np.cos(theta), r * np.sin(theta)
        state_wrapper.ball.set_pos(
            car.position[0] + eps_x,  # Displace a little bit so the ball is not balanced on the car
            car.position[1] + eps_y,
            np.random.uniform(car.position[2] + 2 * BALL_RADIUS, Z_MAX_BALL)
        )
        theta = np.random.uniform(-np.pi, np.pi)
        eps_x, eps_y = r * np.cos(theta), r * np.sin(theta)
        state_wrapper.ball.set_lin_vel(
            x=eps_x,
            y=eps_y
        )


air_dribble_config = dict(
    reward_function=DribbleReward(),
    terminal_conditions=[AirDribbleTerminal()],
    state_setter=AirDribbleState(),
    team_size=1,
    spawn_opponents=False
)
