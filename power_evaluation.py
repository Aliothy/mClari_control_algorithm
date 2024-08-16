import numpy as np
import itertools
from gym_env import mClariSimplifiedEnv
import matplotlib.pyplot as plt
import ast
from matplotlib.ticker import ScalarFormatter

'''
in the function the system is evaluated for different triple of angles each corresponding to interleg 
angles, for each the gait is evaluated and a text file is create containing for each triple the trajectories
obtained with each frequency
'''
def gait_evaluation(simulation_file):

    frequencies = [1,10,30,50,70,90,110,130,150]
    # # frequency = 1
    # triples = [[0,0,0],[np.pi,np.pi,0],[np.pi,0,np.pi]]
    # timesteps = 10
    # env = mClariEnv(simulation_file)
    # total_power = []
    # total_velocities = []
    # total_efficiencies = []
    

    # for triple in triples:

    #     # trajectories = []
    #     # for frequency in frequencies:
    #     # x_pos = []
    #     # y_pos = []
    #     action = (frequency, triple)
    #     env.reset()
    #     for i in range(timesteps):
    #         env.step(action)
    #         # if i%100 == 0:
    #             # pos_step = int(len(env.data.qpos)/4)
    #             # x_COM = np.sum(env.data.qpos[:-1:pos_step])/4
    #             # y_COM = np.sum(env.data.qpos[1:-1:pos_step])/4
    #             # x_pos.append(x_COM)
    #             # y_pos.append(y_COM)
    #     # trajectories.append([x_pos,y_pos])
        
    #     # plt.figure()
    #     # for coordinates in trajectories:
    #     #     plt.plot(coordinates[0],coordinates[1])
    #     # plt.legend(str(frequencies))
    #     # plt.title(f'{triple}')
    #     # plt.savefig(f'gait_evaluation_{triple}.png')

    #     # filename = f'gait_evaluation_{triple}.txt'
    #     # with open(filename,'w') as file:
    #     #     file.write(trajectories)


    # for triple in triples:
    #     powers_act = []
    #     mean_velocities = []
    #     efficiencies = []
    #     for frequency in frequencies:
    #         mean_power = 0
    #         mean_velocity = 0
    #         action = (frequency, triple)
    #         env.reset()
    #         for i in range(timesteps):
    #             env.step(action)
    #             powers = np.array(env.powers)
    #             powers = powers.T
    #             powers = np.sum([np.sqrt(np.sum(power**2)) for power in powers])/1000000000
    #             velocity = np.sqrt(np.sum(env.final_position**2))/1000
    #             mean_power += powers
    #             mean_velocity += velocity
    #         efficiency = 0.01*mean_velocity/mean_power
    #         powers_act.append(powers/9)
    #         mean_velocities.append(velocity/9)
    #         efficiencies.append(efficiency)
    #     total_power.append(powers_act)
    #     total_velocities.append(mean_velocities)
    #     total_efficiencies.append(efficiencies)


    # # Create subplots
    # fig, axs = plt.subplots(4, 2, figsize=(10, 10))  # 4 rows, 2 columns

    # # Plot data
    # for i in range(8):
    #     row = i // 2
    #     col = i % 2
    #     axs[row, col].plot(powers[i])
    #     axs[row, col].set_title(f'Actuator {i+1}')
    #     axs[row, col].set_xlabel('n timestep')
    #     axs[row, col].set_ylabel('Power')

    # # Adjust layout
    # plt.tight_layout()
    filename = "values.txt"
    # with open(filename,'w') as file:
    #     file.write(str(total_power)+'\n')
    #     file.write(str(total_velocities)+'\n')
    #     file.write(str(total_efficiencies)+'\n')

    with open(filename,'r') as file:
        lines = file.readlines()

    total_power = ast.literal_eval(lines[0][:-1])
    total_velocities = ast.literal_eval(lines[1][:-1])
    total_efficiencies = ast.literal_eval(lines[2][:-1])    

    # Create subplots
    fig, axs = plt.subplots(3,3,figsize=(8, 14))  

    # Plot data
    for i in range(len(total_power)):
        axs[i,0].plot(frequencies, total_power[i])
        axs[i,1].plot(frequencies, total_velocities[i])
        axs[i,2].plot(frequencies, total_efficiencies[i])

        # Set titles and labels
        
        axs[i,0].set_xlabel('Frequency (Hz)')
        axs[i,0].set_ylabel('Overall Power Consumed (W)')

        axs[i,1].set_xlabel('Frequency (Hz)')
        axs[i,1].set_ylabel('Mean Velocity (m/s)')

        axs[i,2].set_xlabel('Frequency (Hz)')
        axs[i,2].set_ylabel('Efficiency')
        axs[i, 0].xaxis.labelpad = 5 
        axs[i, 1].xaxis.labelpad = 2 
        axs[i, 2].xaxis.labelpad = 4 

    axs[0,0].set_title('Power vs Frequency')
    axs[0,1].set_title('Velocity vs Frequency')
    axs[0,2].set_title('Efficiency vs Frequency')

    for axis in axs:
        for ax in axis:
            ax.xaxis.set_label_coords(0.6, -0.2)
            ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
            ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))

    fig.suptitle(r'$(0,0,0), (\pi,\pi,0), (\pi,0,\pi)$', fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    # Show plot
    plt.show()


if __name__ == "__main__":
    gait_evaluation('mCLARI_extra_simplified.xml')