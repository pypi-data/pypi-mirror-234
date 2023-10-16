import torch.distributions
from all.agents import PPO, Agent
from all.approximation import FeatureNetwork, VNetwork, QNetwork
from all.bodies import Body
from all.experiments import run_experiment
from all.policies import SoftmaxPolicy, DeterministicPolicy, SoftDeterministicPolicy, GaussianPolicy
from all.policies.deterministic import DeterministicPolicyNetwork
from all.presets import Preset, PresetBuilder
from gym.spaces import Box, MultiDiscrete, Discrete
from torch import nn
from torch.nn import Sequential
from torch.optim import Adam

import rlgym
from rlgym_tools.autonomous_utils.autonomous_env import autonomous_env


class RLPreset(Preset):
    def __init__(self, env, name, device, **hyperparameters):
        super().__init__(name, device, hyperparameters)
        self.feature_model = nn.Linear(72, 128).to(device)
        self.value_model = nn.Linear(128, 1).to(device)
        self.policy_model = nn.Linear(128, 2 * 8).to(device)

    def agent(self, writer=None, train_steps=float('inf')):
        lr = self.hyperparameters.pop("lr")
        eps = self.hyperparameters.pop("eps")
        feature_optimizer = Adam(self.feature_model.parameters(), lr=lr,
                                 eps=eps)
        value_optimizer = Adam(self.value_model.parameters(), lr=lr,
                               eps=eps)
        policy_optimizer = Adam(self.policy_model.parameters(), lr=lr,
                                eps=eps)

        # approximators
        f = FeatureNetwork(self.feature_model, feature_optimizer, writer=writer)
        v = VNetwork(self.value_model, value_optimizer, writer=writer)
        p = GaussianPolicy(self.policy_model, policy_optimizer, space=Box(-1, 1, (8,)), writer=writer)

        return PPO(f, v, p, **self.hyperparameters, n_envs=1)

    def test_agent(self):
        pass


class RLBody(Body):
    def process_state(self, state):
        return

if __name__ == '__main__':
    env = autonomous_env(rlgym.make(team_size=1, self_play=True))

    agents = PresetBuilder("rlgym", default_hyperparameters={
        "discount_factor": 0.99,
        "lr": 2e-4,
        "eps": 1.5e-4,
        "minibatches": 32,
    }, constructor=RLPreset, env=env, device="cuda")

    # agents = [
    #     PresetBuilder("rlgym", None, RLPreset, env=env)
    #     for n in range(2)
    # ]
    run_experiment(agents, env, frames=1000)
