from gymnasium.envs.registration import register

register(
    id='CustomMujocoEnv-v0',
    entry_point='gym_env:mClariEnv'
)

import gymnasium as gym

from stable_baselines3 import SAC
from graphic_callback import GraphicCallback

env = gym.make('CustomMujocoEnv-v0')
callback = GraphicCallback(verbose = 1)

model = SAC("MlpPolicy", env, learning_rate=0.01, verbose=1, policy_kwargs=dict(net_arch=[10, 3]) )
model.learn(total_timesteps=500000, callback=callback)

# this section is to evaluate the results
# vec_env = model.get_env()
# obs = vec_env.reset()
# rewards = []
# for i in range(540):
#     action, _states = model.predict(obs, deterministic=True)
#     obs, reward, done, info = vec_env.step(action)
#     rewards.append(reward)

# env.close()

# filename = 'results4.txt'
# with open(filename,'w') as file:
#     file.write(str(rewards))
