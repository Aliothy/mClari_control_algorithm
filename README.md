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
git clone https://github.com/Aliothy/mClari_control_algorithm.git
```
2. Install the required packages as mentioned above.
Follow the instructions in the script files to run simulations and train the control algorithm.
Project Structure
src/: Contains the source code for the control algorithm and environment setup.
models/: Pre-trained models and results of the training process.
scripts/: Utility scripts for running experiments and visualizations.
Usage
Navigate to the project directory.
Run the training script:
bash
Copy code
python src/train_control_algorithm.py
Use the trained model to control the mClari robot in the simulation environment:
bash
Copy code
python src/run_simulation.py
Contributing
Contributions are welcome! Please feel free to submit a Pull Request or open an Issue to discuss any changes or suggestions.

License
This project is licensed under the MIT License - see the LICENSE file for details.

