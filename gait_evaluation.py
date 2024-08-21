import numpy as np
from training.gym_env3 import mClariEnv 
import matplotlib.pyplot as plt
import itertools

'''
in the function the system is evaluated for different triple of angles each corresponding to interleg 
angles, for each the gait is evaluated and an image is create containing for each triple the trajectories
obtained with each frequency
'''
def gait_evaluation2(simulation_file, final_time):

    values = [0, np.pi/2, np.pi]
    triples = list(itertools.product(values, repeat=3))
    # titles = [r'$(\pi,\pi,0)$',r'$(\pi,0,\pi)$',r'$(\pi/2,\pi,\pi/2)$']
    frequencies = [1,20,40,60,80,100,120,150]
    
    timesteps = [final_time*500*frequency for frequency in frequencies]
    env = mClariEnv(simulation_file)

    for index, triple in enumerate(triples):

        trajectories = []
        for i, frequency in enumerate(frequencies):
            x_pos = []
            y_pos = []
            action = (frequency,list(triple))
            env.reset()
            for j in range(timesteps[i]):
                env.step(action)
                if j%np.floor(timesteps[i]/6000) == 0:
                    pos_step = int(len(env.data.qpos)/4)
                    x_COM = np.sum(env.data.qpos[:-1:pos_step])/4
                    y_COM = np.sum(env.data.qpos[1:-1:pos_step])/4
                    x_pos.append(x_COM)
                    y_pos.append(y_COM)
            trajectories.append([x_pos,y_pos])
        
        fig, ax = plt.subplots(figsize=(6, 6))
        #plt.figure()
        for coordinates in trajectories:
            ax.plot(coordinates[0],coordinates[1])
        if index == 0:
            ax.set_aspect('equal', adjustable='datalim')

        # Set axis limits to be equal
        # x_limits = ax.get_xlim()
        # y_limits = ax.get_ylim()
        # ax.set_xlim(min(x_limits[0], y_limits[0]), max(x_limits[1], y_limits[1]))
        # ax.set_ylim(min(x_limits[0], y_limits[0]), max(x_limits[1], y_limits[1]))

        ax.legend(frequencies,bbox_to_anchor=(0.9, 1), loc='upper left')
        ax.set_xlabel('x(mm)')
        ax.set_ylabel('y(mm)')
        ax.set_title(str(triple))
        plt.savefig(f'images/gait_evaluation_{triple}.png')
        plt.close()
        print(f'{index}')

        # filename = f'gait_evaluation_{triple}.txt'
        # with open(filename,'w') as file:
        #     file.write(str(trajectories))       

if __name__ == "__main__":
    gait_evaluation2('phy_models/task1.xml', 60)