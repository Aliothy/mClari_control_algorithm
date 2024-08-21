# mClari Control Algorithm

This project involves the development of a control algorithm for the movement of the mClari robot using the MuJoCo physics engine and Gym environment. The algorithm is implemented and trained using Stable-Baselines3 (SB3).

## Prerequisites

Before running the project, ensure you have the following packages installed:

### 1. MuJoCo

MuJoCo (Multi-Joint dynamics with Contact) is a physics engine used for simulating robots and other complex physical systems.

To install MuJoCo, run:

```bash
pip install mujoco
```
For more details on setting up MuJoCo, refer to the official [MuJoCo README](https://github.com/google-deepmind/mujoco/blob/main/README.md).

### 2. GYMNASIUM

Gymnasium (formerly known as OpenAI Gym) is a toolkit for developing and comparing reinforcement learning algorithms. It provides a standard API to communicate with various environments, including MuJoCo.

To install Gymnasium, run:

```bash
pip install gymnasium
```
For more details on setting up MuJoCo, refer to the official [Gymnasium README](https://github.com/Farama-Foundation/Gymnasium).


### 3. STABLE BASELINE 3:

Stable-Baselines3 is a set of reliable implementations of reinforcement learning algorithms in PyTorch. It is used to train the control algorithm for the mClari robot.

To install SB3, run:

```bash
pip install stable-baselines3
```
For more details on setting up MuJoCo, refer to the official [Gymnasium README](https://github.com/DLR-RM/stable-baselines3).

## Getting Started
To get started with the project, follow these steps:

1. Clone this repository:
```bash
git clone https://github.com/Aliothy/mClari_control_algorithm
```
2. Install the required packages as mentioned above.
3. Follow the instructions in the script files to run simulations and train the control algorithm.

## Project Structure

- `phy_models/`: Contains the MuJoCo files for the physical environments
  - `STL_files/`: Contains all the STL files obtained from the SolidWorks files
  - `mClari_.xml`: These are the three simulations of the devices—complete, simplified, and extra simplified versions.
  - `task_n.xml`: These are the MuJoCo environments composed of one of the microbots and the floor.
-  `training/ `: gymnasium environments for the reinforcement learning system (called gym_env_n.py) and the files for training.
- other files for testing.
  
## Usage
1. Navigate to the project directory.
2. Run the training script:
```bash
python src/train_control_algorithm.py
```
3. Use the trained model to control the mClari robot in the simulation environment:
```bash
python src/run_simulation.py
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request or open an Issue to discuss any changes or suggestions.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

