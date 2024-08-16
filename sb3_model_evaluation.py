from gymnasium.envs.registration import register

register(
    id='CustomMujocoEnv-v0',
    entry_point='gym_env_simplified_3:mClariSimplifiedEnv'
)

import gymnasium as gym
from stable_baselines3 import SAC 
import matplotlib.pyplot as plt

# Load the trained model
#model = SAC.load("model_2.zip")

# Create the environment
env = gym.make('CustomMujocoEnv-v0')
print(env.phase_angles) 

#vec_env = model.get_env()
obs, info = env.reset()
rewards = []
ep_reward = []
dones = []
frequencies = []
ep_freq = []
indeces = []
ep_ind = []
infos = []
for i in range(1000):
    action = -1.0 #model.predict(obs, deterministic=True)
    obs, reward, done, truncated, info = env.step(action)
    ep_reward.append(reward) 
    if done:
        dones.append(done)
        rewards.append(ep_reward)
        ep_reward = []
        frequencies.append(ep_freq)
        ep_freq = []
        indeces.append(ep_ind)
        ep_ind = []
    if info != {}:
        infos.append(info)
    
    ep_freq.append(env.unwrapped.frequency)
    ep_ind.append(env.unwrapped.phase_index)

  

env.close()

print(dones)
print(infos)