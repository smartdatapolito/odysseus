# Get started with e3f2s

## Introduction

e3f2s is a software for simulation of shared electric fleets in urban environments.
It is still a prototype in active development. However, it is already stable enough to be used for research activities.
In order to understand what e3f2s is capable of, please first read the three papers available in the folder /home/det_tesi/a.ciociola/input_simulator/papers.

e3f2s is composed by three main modules:
* city_data_manager: receives in input data from different sources and output a simulation-ready version of the same data.
* simulator: contains data structures and algorithms for actual simulations.
* utils: contains some utility functions used across the other modules.

In this tutorial, we focus on running our first simulation with e3f2s.

## Setup repository, environment and data

First, let's clone the public git repository and move data into the right folder.
For now, we skip explanations about city_data_manager functionalities.

```console
git clone https://github.com/AleCioc/e3f2s my-e3f2s-folder
cp -r /home/det_tesi/a.ciociola/input_simulator/data my-e3f2s-folder/e3f2s/city_data_manager
```

Then, let's install all the necessary libraries.

```console
pip install --user -r my-e3f2s-folder/requirements.txt
```


## Configuring simulation input

The folder e3f2s/simulator/simulation_input contains configuration files for simulation.

In particular:

* sim_configs_target.json: contains the name of the configuration to run
* sim_configs_versioned: contains one folder for each saved configuration
    * e.g. sim_configs_versioned/turin_iscc_set1 contains the configuration for the first set of simulation used in ISCC paper.

Each configuration folder must contain the following Python files:

* sim_run_conf.py: specifies used data source, run mode (single_run or multiple_runs), number of cores to use in case of multiple runs, simulation type (trace-driven or model-driven) and output folder name
* sim_general_conf.py: specifies macroscopic parameters about spatial and temporal configuration, as well as fleet load factor policy.
* single_run_conf.py: specifies scenario configuration for single run
    * model_validation_conf.py: special case of single run
* multiple_runs_conf.py: specifies scenario configuration for multiple runs
* vehicle_config.py: specifies vehicles characteristics
* cost_conf.py: specifies cost/revenue configuration

Let's create a new folder for a new configuration:

```console
cp -r /home/det_tesi/a.ciociola/input_simulator/ my-e3f2s-folder/e3f2s/simulator/simulation_input/sim_configs_versioned/
```

Modify configurations as you desire, then run the simulator:

```console
cd my-e3f2s-folder/
python -m e3f2s.simulator
```

Let's wait for simulation to finish and let's check the results folder and the figures folder (figures are created automatically only in single run mode)

```console
ls my-e3f2s-folder/simulator/results/Torino/single_run/test
ls my-e3f2s-folder/simulator/figures/Torino/single_run/test
```

Done! Now we can explore our results and eventually produce other analysis and plots.

