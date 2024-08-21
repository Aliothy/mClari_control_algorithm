import numpy as np
import mujoco
import mujoco.viewer

'''this environment has the only purpose to evaluate the behavior of the models without implementing any reward or others'''
class mClariEnv():

    def __init__(self, filename = None):
        if filename is None:
            filename = 'phy_models/task1.xml'
            
        self.model = mujoco.MjModel.from_xml_path(filename) 
        self.data = mujoco.MjData(self.model)
        mujoco.mj_resetData(self.model,self.data)
        self.viewer = None

    def step(self, action):
        
        if type(action) is tuple:
            frequency = action[0] 
            timesteps = int(500*frequency)
            self.model.opt.timestep = 1/timesteps
            phase_angles = np.array([0,np.pi/2,action[1][0],np.pi/2+action[1][0],action[1][1],np.pi/2+action[1][1],action[1][2],np.pi/2+action[1][2]]) 
            for i in range(timesteps):
                actuation_signals = np.sin(2*np.pi*frequency*self.data.time + phase_angles)
                self.data.ctrl[:] = actuation_signals
                mujoco.mj_step(self.model, self.data)

        return 

    def reset(self, seed = None, options = None):

        if seed is not None:
            self.seed = seed

        mujoco.mj_resetData(self.model,self.data)
        observation = np.array([0.0,0.0]).astype(np.float64)
        info = {}

        return observation,info

    def render(self, mode='human'):
        if self.viewer is None:
            self.viewer = mujoco.viewer.launch_passive(self.model, self.data)
        self.viewer.sync()

    def close(self):
        if self.viewer is not None:
            self.viewer = None

    def _compute_reward(self):
        
        ''' here write the reward function'''

        pass
    
    def _check_done(self):
        # Implement your termination condition
        terminated = False
        truncated = False
        info = {}
        
        return terminated, truncated, info

    def _get_obs(self, final_pose, initial_pose = None, dt = None):

        ''' here write the code to find the observations, they have to be 
        in the shape of the gym.space defined above'''
        
        observations =np.array((final_pose - initial_pose) / dt).astype(np.float64)

        return observations