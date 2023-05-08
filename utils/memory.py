import copy
import pickle
import random
from typing import Tuple
import warnings

import numpy as np
from gym import Env
from stable_baselines3 import SAC
import torch
from tqdm import tqdm


class MemoryBuffer:

    def __init__(self, seed: int = 0):
        self.buffer = []
        self.length = 0
        random.seed(seed)

    def add(self, experience: Tuple[np.array, np.array, np.array, float, bool]) -> None:
        """
        Add a new experience to the buffer.

        :param experience: Tuple of (state, next_state, action, reward, done)
        """
        self.length += 1
        self.buffer.append(experience)

    def generate_expert_data(self, env: Env, args: dict, seed: int):
        """
        Generate expert data using a trained agent.

        :param env: The environment to generate data for.
        :param expert_agent_dir: The directory of the trained agent.
        :param num_trajectories: The number of trajectories to generate.
        :param seed: The seed to use for the environment.
        """
        env = copy.deepcopy(env)

        model = SAC.load(args.model_dir, env)

        seed += 1

        state, _ = env.reset(seed=seed)
        for _ in tqdm(range(args.num_trajs)):
            for _ in range(args.max_traj_steps):

                action, _ = model.predict(state, deterministic=True)
                next_state, reward, done, _, _ = env.step(action)
                state = next_state

                self.add(
                    (state, next_state, action, reward, done)
                )
                if done:
                    break
            seed += 1
            state, _ = env.reset(seed=seed)

    def get_batch(self, batch_size):
        if batch_size > len(self.buffer):
            warnings.warn(
                f"Requested batch size of {batch_size} is larger than the length of the input data "
                f"({len(self.buffer)}). The function will return the entire dataset.",
                Warning)
            batch_size = len(self.buffer)

        # Select a consecutive batch of data of size batch_size starting from the random start index
        indexes = np.random.choice(
            np.arange(len(self.buffer)), size=batch_size, replace=False)
        batch = [self.buffer[i] for i in indexes]
        # First convert to np.array for performance, as told by a warning.
        obs_batch = torch.tensor(np.array([t[0] for t in batch]), dtype=torch.float)
        next_obs_batch = torch.tensor(np.array([t[1] for t in batch]), dtype=torch.float)
        # For some environments it may be necessary to unsqueeze an action too.
        action_batch = torch.tensor(np.array([t[2] for t in batch]), dtype=torch.float)
        reward_batch = torch.tensor(np.array([t[3] for t in batch]), dtype=torch.float).unsqueeze(1)
        done_batch = torch.tensor(np.array([t[4] for t in batch]), dtype=torch.float).unsqueeze(1)

        return obs_batch, next_obs_batch, action_batch, reward_batch, done_batch

# if __name__ == '__main__':
#    pass
