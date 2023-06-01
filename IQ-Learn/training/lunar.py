import gym
from stable_baselines3 import DQN

env = gym.make("LunarLander-v2")
env.reset(seed=69)

model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100_000, log_interval=10, progress_bar=True)
model.save("dqn_lunar")

env = gym.make("LunarLander-v2")
env.reset(seed=42)
model = DQN.load("dqn_lunar", env)

NUM_SAMPLES = 10

# # Evaluate the agent
for i_sample in range(NUM_SAMPLES):

    vec_env = model.get_env()
    obs = vec_env.reset()
    for i in range(1000):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = vec_env.step(action)
        vec_env.render()
    print(f"Sample {i_sample}", reward)
