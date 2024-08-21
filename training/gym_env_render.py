import gymnasium as gym
from gymnasium.spaces import Box
import numpy as np
import mujoco
import mujoco.viewer
import itertools


'''gym environment for controlling the mClari robot, this environment works with the simplified or extrasimplied version of the system
for problematics related to the observational space, it is the same environment as gym_env but it also give the image of the robot '''

#this one has phase angles reduced to 8 elements and fixed phase per episod
class mClariEnv(gym.Env):
    metadata = {'render_modes': ['human', 'rgb_array']}

    def __init__(self):

        '''initial parameter definition'''

        super(mClariEnv, self).__init__()
        self.task_number = 1
        self.viewer = None
        self.initialize_model()
        

        # Define action and observation space
        # The action space is a box of two variables one for frequency and the other for phase angle groups
        self.action_space = Box(low=-1.0 , high=1.0 , shape=(2,), dtype=np.float64)
        # The observation space is 4 dimensional: power consumed, mean velocity and errors
        self.observation_space = Box(low=-np.inf, high=np.inf, shape=(4,), dtype=np.float64)

        #create an array of phase angles it will be self.phase_angles
        self.initialize_phasediff()
        
        self.powers = np.array([0.0 for _ in range(8) ])   # array to store the power consumed
        self.range = 10                                    # maximum increase or decrease of frequency
        self.max_time = 180                                # maximum time
        self.angles_group = 8                              # number of phase angle groups
        
    def step(self, action):

        #compute the new frequency and the desired angle group
        self.compute_actsign(action)

        #define the number of timesteps and the timestep of the model
        n_timesteps = 500*self.frequency
        self.model.opt.timestep = 1/n_timesteps
        
        initial_pose = self.find_pose(self.data.qpos)
        
        self.phases = self.phase_angles[self.phase_index]

        for i in range(n_timesteps):
        
            self.data.ctrl[:] = np.sin(2*np.pi*self.frequency*self.data.time+self.phases)
            mujoco.mj_step(self.model, self.data)

            if i % self.frequency == 0:
                self._get_power()
                self.render()
                print('sì')

        final_pose = self.find_pose(self.data.qpos)
        observation = self._get_obs(final_pose, initial_pose)
        reward = self._compute_reward(observation)
        terminated, truncated, info = self._check_done(final_pose)
        if hasattr(info,'fallen'):
            reward -= 100
        
        if hasattr(info,'target reached'):
            reward += 10
            
        if terminated:
            self.task_number += 1
            self.initialize_model()
            self.reset()

        return observation, reward, terminated, truncated, info

    def reset(self, seed = None, options = None):

        if seed is not None:
            self.seed = seed

        mujoco.mj_resetData(self.model,self.data)
        final_pose = self.find_pose(self.data.qpos)
        for i in range(100):
            mujoco.mj_step(self.model,self.data)
        observation = self._get_obs(final_pose)
        info = {}

        return observation,info

    def render(self, mode='human'):
        if self.viewer is None:
            self.viewer = mujoco.viewer.launch_passive(self.model, self.data)
        self.viewer.sync()
        pass

    def close(self):
        if self.viewer is not None:
            self.viewer = None

    def _compute_reward(self, observation):
        # Implement your reward calculation logic
        reward = 0.01*observation[1]/observation[0]

        return reward
    
    def _check_done(self, final_pose):

        # Implement the termination condition
        terminated = False
        truncated = False
        info = {}

        if self.data.time > self.max_time:
            terminated = True
            truncated = True

        if np.sum((final_pose-self.desired_pose)**2) > 0.5:
            terminated = True
            info = {'target reached' : True}
        
        for i in range(self.data.ncon):
            contact = self.data.contact[i]
            if contact.geom1 == 0 and (contact.geom2 != 2 and contact.geom2 != 5 and contact.geom2 != 8 and contact.geom2 != 11):
                info = {'fallen' : True}
                terminated = True
                truncated = True
        
        return terminated, truncated, info

    def find_pose(self, qpos):
        
        # the microbot is defined as 4 entities connected together so the CoM is at the center of the legs
        pos_step = int(len(qpos)/4)
        x_COM = np.sum(qpos[:-1:pos_step])/4
        y_COM = np.sum(qpos[1:-1:pos_step])/4

        return np.array([x_COM, y_COM]).astype(np.float64)    

    def _get_obs(self, final_pose, initial_pose = None):

        if initial_pose is None : 
            observations = np.array([[0.0,0.0],list(final_pose)]).reshape(-1)
            return observations.astype(np.float64)
        
        mean_velocity = np.sqrt(np.sum((final_pose - initial_pose)**2))/1000
        mean_power = np.sum(np.sqrt(self.powers))/1000000000
        errors = self.desired_pose-final_pose
        observations = np.array([[mean_power,mean_velocity],list(errors)])
        observations = observations.reshape(-1)
        self.powers = np.array([0.0 for _ in range(8)])

        return observations.astype(np.float64)

    def compute_actsign(self,action):

        self.frequency = int(self.frequency + action[0]*self.range)
        if self.frequency < 1:
            self.frequency = 1
        if self.frequency > 150:
            self.frequency = 150
        
        self.phase_index = int(action[1]*3.5+3.5) #the groups are numered from 0 to 7

    def _get_power(self):
        torque = self.data.qfrc_actuator
        angular_velocity = self.data.qvel
        powers = torque*angular_velocity
        powers = np.array(powers[[6,7,14,15,22,23,30,31]])
        powers = powers**2
        self.powers += powers

    def _get_pose(self):
        qpos = self.data.qpos
        pos_step = int(len(qpos)/4)
        x_COM = np.sum(qpos[:-1:pos_step])/4
        y_COM = np.sum(qpos[1:-1:pos_step])/4

        return np.array([x_COM, y_COM]).astype(np.float64)
    
    def initialize_model(self):
        
        if self.task_number > 6:
            self.task_number = 1

        filename = 'phy_models/task' + str(self.task_number) + '.xml'
        self.model = mujoco.MjModel.from_xml_path(filename)
        self.data = mujoco.MjData(self.model)
        self.render()

        # in some environment the robot doesn't touch the ground at the beginning, so let's run some free forces steps to start properly
        for _ in range(100):
            mujoco.mj_step(self.model,self.data)
        
        self.phase_index = 0
        self.frequency = 1

        self.desired_pose = 120*np.random.rand(2)-60

    def initialize_phasediff(self):

        # for the angles group just 8 will be used considering all the groups in which the leg angles are paired 
        values = [0.0, np.pi]
        triples = list(itertools.product(values, repeat=3))
        phase_shift = []
        for triple in triples:
            new_array = [0.0,0.0] + [x for elem in triple for x in (elem,elem)]
            phase_shift.append(new_array)
        phase_shift = np.array(phase_shift)
        self.phase_angles = np.array([[0.0,np.pi/2,0.0,np.pi/2,0.0,np.pi/2,0.0,np.pi/2] for i in range(len(triples))])
        self.phase_angles = self.phase_angles + phase_shift