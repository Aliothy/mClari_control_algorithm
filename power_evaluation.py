from training.gym_env2 import mClariSimplifiedEnv
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
    timesteps = 20
    env = mClariSimplifiedEnv()
    total_power = []
    total_velocities = []
    total_efficiencies = []
    filename = "env_check.txt"
    indeces = [0,5,6]
    with open(filename,'w') as file:
        for index in indeces:
            powers_act = []
            mean_velocities = []
            efficiencies = []
            env.phase_index = index
            env.initialize_model()
            for frequency in frequencies:
                mean_power = 0
                mean_velocity = 0
                env.reset()
                for _ in range(timesteps):
                    observation, reward, terminated, truncated, info = env.step([frequency,index])
                    mean_power += observation[0]
                    mean_velocity += observation[1]
                    file.write(str(env.task_number))
                efficiency = 0.01*mean_velocity/mean_power
                powers_act.append(mean_power/9)
                mean_velocities.append(mean_velocity/9)
                efficiencies.append(efficiency)
            total_power.append(powers_act)
            total_velocities.append(mean_velocities)
            total_efficiencies.append(efficiencies)


    # Create subplots
    filename = "values.txt"
    with open(filename,'w') as file:
        file.write(str(total_power)+'\n')
        file.write(str(total_velocities)+'\n')
        file.write(str(total_efficiencies)+'\n')

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