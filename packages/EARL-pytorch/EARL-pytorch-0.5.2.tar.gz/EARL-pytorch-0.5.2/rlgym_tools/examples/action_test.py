import random

import numpy as np
import torch
from gym.spaces import MultiDiscrete
from rlgym.envs import Match
from rlgym.utils.reward_functions import CombinedReward
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.vec_env import VecMonitor, VecNormalize, VecCheckNan, VecEnvWrapper, VecEnv
from stable_baselines3.common.vec_env.base_vec_env import VecEnvObs, VecEnvStepReturn
from stable_baselines3.ppo import MlpPolicy

from rlgym.utils.obs_builders import AdvancedObs
from rlgym.utils.reward_functions.common_rewards import VelocityPlayerToBallReward, LiuDistancePlayerToBallReward, \
    EventReward
from rlgym.utils.state_setters import DefaultState
from rlgym.utils.terminal_conditions.common_conditions import TimeoutCondition, GoalScoredCondition

from rlgym_tools.extra_rewards.diff_reward import DiffReward
from rlgym_tools.sb3_utils import SB3MultipleInstanceEnv
from rlgym_tools.sb3_utils.sb3_multidiscrete_wrapper import SB3MultiDiscreteWrapper


class SB3MultiDiscreteWrapperV2(VecEnvWrapper):
    """
    Simply converts env such that action space is MultiDiscrete instead of Box (basically KBM).
    """

    def __init__(self, venv: VecEnv, n=3):
        super().__init__(venv)
        assert n % 2 == 1
        self.action_space = MultiDiscrete((n, n, 2, 2, 2))
        self.n = n

    def reset(self) -> VecEnvObs:
        return self.venv.reset()

    def step_async(self, actions: np.ndarray) -> None:
        actions = np.array(actions, copy=True)
        actions = actions.reshape((-1, 5))
        actions[:, 0] = actions[:, 0] / (self.n // 2) - 1
        actions[:, 1] = actions[:, 1] / (self.n // 2) - 1

        parsed = np.zeros((actions.shape[0], 8))
        parsed[:, 0] = actions[:, 0]  # throttle
        parsed[:, 1] = actions[:, 1]  # steer
        parsed[:, 2] = actions[:, 0]  # pitch
        parsed[:, 3] = actions[:, 1] * (1 - actions[:, 4])  # yaw
        parsed[:, 4] = actions[:, 1] * actions[:, 4]  # roll
        parsed[:, 5] = actions[:, 2]  # jump
        parsed[:, 6] = actions[:, 3]  # boost
        parsed[:, 7] = actions[:, 4]  # handbrake
        self.venv.step_async(parsed)

    def step_wait(self) -> VecEnvStepReturn:
        return self.venv.step_wait()


if __name__ == '__main__':  # Required for multiprocessing
    random.seed(123)
    np.random.seed(123)
    torch.manual_seed(123)
    frame_skip = 8  # Number of ticks to repeat an action
    half_life_seconds = 5  # Easier to conceptualize, after this many seconds the reward discount is 0.5

    fps = 120 / frame_skip
    gamma = np.exp(np.log(0.5) / (fps * half_life_seconds))  # Quick mafs
    print(f"fps={fps}, gamma={gamma})")


    def get_match():  # Need to use a function so that each instance can call it and produce their own objects
        return Match(
            team_size=2,  # 3v3 to get as many agents going as possible, will make results more noisy
            tick_skip=frame_skip,
            reward_function=CombinedReward.from_zipped(
                DiffReward(LiuDistancePlayerToBallReward()),
                EventReward(touch=1.)
            ),  # Simple reward since example code
            self_play=True,
            terminal_conditions=[TimeoutCondition(round(fps * 30)), GoalScoredCondition()],  # Some basic terminals
            obs_builder=AdvancedObs(),  # Not that advanced, good default
            state_setter=DefaultState()  # Resets to kickoff position
        )


    env = SB3MultipleInstanceEnv(get_match, 6, wait_time=30)  # Start 2 instances, waiting 60 seconds between each
    env = SB3MultiDiscreteWrapper(env)  # Convert action space to multidiscrete
    env = VecCheckNan(env)  # Optional
    env = VecMonitor(env)  # Recommended, logs mean reward and ep_len to Tensorboard
    env = VecNormalize(env, norm_obs=False, gamma=gamma)  # Highly recommended, normalizes rewards

    # Hyperparameters presumably better than default; inspired by original PPO paper
    model = PPO(
        MlpPolicy,
        env,
        n_epochs=32,  # PPO calls for multiple epochs
        learning_rate=1e-5,  # Around this is fairly common for PPO
        ent_coef=0.01,  # From PPO Atari
        vf_coef=1.,  # From PPO Atari
        gamma=gamma,  # Gamma as calculated using half-life
        verbose=3,  # Print out all the info as we're going
        batch_size=4096,  # Batch size as high as possible within reason
        n_steps=4096,  # Number of steps to perform before optimizing network
        tensorboard_log="out/logs",  # `tensorboard --logdir out/logs` in terminal to see graphs
        device="auto"  # Uses GPU if available
    )

    # Save model every so often
    # Divide by num_envs (number of agents) because callback only increments every time all agents have taken a step
    # This saves to specified folder with a specified name
    # callback = CheckpointCallback(round(1_000_000 / env.num_envs), save_path="policy", name_prefix="rl_model")

    model.learn(100_000_000)

    # # Now, if one wants to load a trained model from a checkpoint, use this function
    # # This will contain all the attributes of the original model
    # # Any attribute can be overwritten by using the custom_objects parameter,
    # # which includes n_envs (number of agents), which has to be overwritten to use a different amount
    # model = PPO.load("policy/rl_model_1000002_steps.zip", env, custom_objects=dict(n_envs=env.num_envs))
    # env.reset()  # Important when loading models, SB3 does not do this for you
    # # Use reset_num_timesteps=False to keep going with same logger/checkpoints
    # model.learn(100_000_000, callback=callback, reset_num_timesteps=False)
