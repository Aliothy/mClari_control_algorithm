from stable_baselines3.common.callbacks import BaseCallback
import os
import time


class GraphicCallback(BaseCallback):
    """
    A custom callback that derives from ``BaseCallback``.

    :param verbose: Verbosity level: 0 for no output, 1 for info messages, 2 for debug messages
    """
    def __init__(self, verbose: int = 0, reward_path: str = '', model_path: str = ''):
        super().__init__(verbose)

        self.rewards = []
        self.actions = []
        self.current_reward = 0.0
        self.reward_path = reward_path
        self.model_path = model_path
        self.parameters = []
        self.frequencies = []
        self.current_frequency = 0.0
        self.initial_time = 0.0
        self.current_timestep = 0

    def _on_training_start(self) -> None:
        """
        This method is called before the first rollout starts.
        """
        self.initial_time = time.time()
        pass

    def _on_rollout_start(self) -> None:
        """
        A rollout is the collection of environment interaction
        using the current policy.
        This event is triggered before collecting new samples.
        """
        pass

    def _on_step(self) -> bool:
        """
        This method will be called by the model after each call to `env.step()`.

        For child callback (of an `EventCallback`), this will be called
        when the event is triggered.

        :return: If the callback returns False, training is aborted early.
        """
        self.current_reward += self.locals['rewards']
        self.actions.append(self.locals['actions'][0])
        # self.current_frequency += actions[0]

        # Check if the episode is done
        if self.locals['dones']:
            # Log the episode reward and reset the current episode reward
            timestep = self.locals['self'].num_timesteps
            delta_t = timestep - self.current_timestep
            self.rewards.append(self.current_reward.item()/delta_t)
            #self.frequencies.append(self.current_frequency.item()/delta_t)
            self.current_timestep = timestep
            self.current_reward = 0.0
            self.current_frequency = 0.0

        return True

    def _on_rollout_end(self) -> None:
        """
        This event is triggered before updating the policy.
        """
        pass

    def _on_training_end(self) -> None:
        """
        This event is triggered before exiting the `learn()` method.
        """
        #save the rewards
        final_time = time.time()
        rew_filename = os.path.join(self.reward_path, 'rewards_1.txt')
        self.rewards = list(self.rewards)
        with open(rew_filename,'w') as file:
            file.write(f'{self.rewards}\n')
            file.write(f'{self.actions}\n')
            file.write(f'elapsed time:{final_time-self.initial_time}')
        
        #save the model
        model_filename = os.path.join(self.model_path, 'model_1.zip')
        self.model.save(model_filename)
        if self.verbose > 0:
            print('model and rewards saved')
        
        pass