import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# Example data
frequencies = [0, 1, 2, 3, 4, 5]
total_power = [0.001, 0.002, 0.003, 0.004, 0.005, 0.006]
mean_velocities = [0.0005, 0.0015, 0.0025, 0.0035, 0.0045, 0.0055]
efficiencies = [0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.0006]

# Create subplots
fig, axs = plt.subplots(3, 1, figsize=(4, 12))  # 3 rows, 1 column

# Plot data
axs[0].plot(frequencies, total_power, label='Power')
axs[1].plot(frequencies, mean_velocities, label='Velocity')
axs[2].plot(frequencies, efficiencies, label='Efficiency')

# Set titles and labels
axs[0].set_title('Power vs Frequency')
axs[0].set_xlabel('Frequency (Hz)')
axs[0].set_ylabel('Overall Power Consumed (W)')

axs[1].set_title('Velocity vs Frequency')
axs[1].set_xlabel('Frequency (Hz)')
axs[1].set_ylabel('Mean Velocity (m/s)')

axs[2].set_title('Efficiency vs Frequency')
axs[2].set_xlabel('Frequency (Hz)')
axs[2].set_ylabel('Efficiency')

# Add legends
for ax in axs:
    ax.legend()
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))

fig.suptitle(r'$(0,0,0), (\pi,\pi,0), (\pi,0,\pi)$', fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.96])
# Show plot
plt.show()