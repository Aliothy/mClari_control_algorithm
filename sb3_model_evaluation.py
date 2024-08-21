from gymnasium.envs.registration import register

register(
    id='CustomMujocoEnv-v0',
    entry_point='training.gym_env:mClariEnv'
)

import gymnasium as gym
from stable_baselines3 import SAC 
import matplotlib.pyplot as plt

# Load the trained model
model = SAC.load("model_1.zip")

# Create the environment
env = gym.make('CustomMujocoEnv-v0')
print(env.phase_angles) 

#vec_env = model.get_env()
obs, info = env.reset()
rewards = []
ep_reward = []
dones = []
infos = []
for i in range(1000):
    action = model.predict(obs, deterministic=True)
    obs, reward, done, truncated, info = env.step(action)
    ep_reward.append(reward) 
    if done:
        dones.append(done)
        rewards.append(ep_reward)
        ep_reward = []
    if info != {}:
        infos.append(info)

env.close()

print(dones)
print(infos)