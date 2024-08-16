from gymnasium.envs.registration import register

register(
    id='CustomMujocoEnv-v0',
    entry_point='gym_env:mClariSimplifiedEnv'
)

import gymnasium as gym

# Create the environment
env = gym.make('CustomMujocoEnv-v0')

#vec_env = model.get_env()
obs, info = env.reset()
frequencies = [1,10,50,100,150]
for i, frequency in enumerate(frequencies):
    print(frequency)
    for i in range(100):
        obs, reward, done, truncated, info = env.step(frequency)

env.close()
