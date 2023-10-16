from typing import Any, Tuple, Dict, Union

import numpy as np
from maze.core.env.core_env import CoreEnv
from maze.core.env.environment_context import EnvironmentContext
from maze.core.env.maze_action import MazeActionType
from maze.core.env.maze_env import MazeEnv
from maze.core.env.maze_state import MazeStateType
from maze.core.env.structured_env import StepKeyType, ActorID
from maze.core.rendering.renderer import Renderer

from rlgym.envs import Match
from rlgym.gym import Gym


class MazeRLGymEnv(CoreEnv):
    def __init__(self, env: Gym):
        super().__init__()
        self.env = env
        self.current_state = None
        self.current_actions = None
        self.n_agents = env._match.agents
        self.current_agent = 0

    def step(self, maze_action: MazeActionType) -> \
            Tuple[MazeStateType, Union[float, np.ndarray, Any], bool, Dict[Any, Any]]:

        if self.current_agent == self.n_agents - 1:
            self.env.step(self.current_actions)
            self.current_agent = 0
            EnvironmentContext.increment_env_step()
        else:
            self.current_agent += 1

    def reset(self) -> MazeStateType:
        self.current_actions = []
        self.current_state = []
        return self.env.reset()

    def seed(self, seed: int) -> None:
        return self.env.seed(seed)

    def close(self) -> None:
        return self.env.close()

    def get_maze_state(self) -> MazeStateType:
        pass

    def get_serializable_components(self) -> Dict[str, Any]:
        pass

    def get_renderer(self) -> Renderer:
        raise NotImplementedError

    def actor_id(self) -> ActorID:
        pass

    def is_actor_done(self) -> bool:
        pass

    @property
    def agent_counts_dict(self) -> Dict[StepKeyType, int]:
        pass

    def clone_from(self, env: 'CoreEnv') -> None:
        pass
