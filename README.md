# Drone
## Objective
Develop a program that can interpret brain signals from an EEG headset and convert them to instructions
that control the flight of a drone, relaying those instructions in real time.

## Hardware
- OpenBCI UltraCortex Mark IV (with Daisy expansion)
- DJI Tello Drone

## Repository Structure
**DataCollection** - contains code related to data acquisition for this project. See NeuroData repo for 
general data collection code.\
**Machine Learning and Signal Processing (ML-SP)** - contains code related to data manipulation
for any part of the project, including pre-processing, post-processing, model training and storage, etc.\
**Systems and Applications** - contains code related to the final application, including GUI code, 
main process loop, ML model integrations, etc.

## Environment Setup and Package Management
### Conda (recommended)
- If you haven't already, [install](https://docs.conda.io/projects/miniconda/en/latest/index.html) the Conda package and environment management system for your operating system. Miniconda is recommended, but full Anaconda will also work.
- On Windows, open an Anaconda Prompt or an Anaconda Powershell from the start menu and navigate to where this repo is cloned.
- On Mac/Linux, open a terminal and navigate to where this repo is cloned.
- Create a new environment with `conda env create -f environment.yml`
- If environment setup or package installation fails, try
  - updating conda with `conda update conda`
  - updating pip with `conda upgrade pip`
  - installing packages without specific version numbers
- Activate environment with `conda activate drone-env`
