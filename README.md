# MORL4Water
<!-- start main body -->
<!-- Repository with a mondular gym environment, which lets you build a multi-objective water simulations to train you MORL agents on. -->
Welcome to morl4water, a flexible gym environment designed for simulating water management in river systems. With morl4water, 
you can build detailed water simulations and train or test your multi-objective reinforcement learning (MORL) agents in these settings. 
This guide will walk you through the key features of the tool. Please refer to the relevant sections based on your needs. 

Currently, we have three water systems implemented in a form of gym environments: Nile River Basin, Susquehanna River Basin and Omo River Basin (under development).

Our toolkit is designed in a modular way, allowing users to build their own systems. For the overview of the systems, please go to System Elements.




## Code Structure
The codebase is organized into two main components:

### `core/`
This directory contains the core simulation logic and modular building blocks for modeling water systems:

- **`envs/`**:  
  Contains the main environment implementation:
  - `water_management_system.py` — Defines how water systems are simulated and interacted with by reinforcement learning agents.

- **`models/`**:  
  Encapsulates domain-specific components such as:
  - **Hydrological and infrastructure models**:  
    - `catchment.py`, `flow.py`, `reservoir.py`, `weir.py`
  - **Operational units**:  
    - `facility.py`, `irrigation_district.py`, `power_plant.py`, `reservoir_with_pump.py`
  - **Objective definitions**:  
    - `objective.py` — Captures performance criteria (e.g., water supply reliability, hydropower generation, ecological flow maintenance)

Each model varies in its structural configuration, observation/action spaces, and optimization objectives, supporting the simulation of diverse river basin settings.

### `examples/`
This directory includes ready-to-run simulation scripts and datasets for real-world river basins:

- **Data**:  
  Subdirectories with input data for:
  - `nile_river/`
    - `catchments/`, `irrigation/`, `reservoirs/`
  - `omo_river/` (under construction)
    - `catchments/`, `irrigation/`, `reservoirs/`
  - `susquehanna_river/`
    - `demands/`, `inflows/`, `reservoirs/`

- **Simulation scripts**:
  - `nile_river_simulation.py`
  - `omo_river_simulation.py` (under construction)
  - `susquehanna_river_simulation.py`

These examples demonstrate how to instantiate and run MORL simulations for each river system, showcasing the flexibility of the framework across geographic and hydrological contexts.

### Code Skeleton

```text
morl4water
├── core
│   ├── envs
│   │   └── water_management_system.py
│   ├── models
│   │   ├── catchment.py
│   │   ├── facility.py
│   │   ├── flow.py
│   │   ├── irrigation_district.py
│   │   ├── objective.py
│   │   ├── power_plant.py
│   │   ├── reservoir.py
│   │   ├── reservoir_with_pump.py
│   │   └── weir.py
├── examples
│   ├── data
│   │   ├── nile_river/
│   │   ├── omo_river/
│   │   └── susquehanna_river/
│   ├── nile_river_simulation.py
│   ├── omo_river_simulation.py
│   └── susquehanna_river_simulation.py
```

### Documentation

For detailed documentation, please visit [https://osikazuzanna.github.io/morl4water/](https://osikazuzanna.github.io/morl4water/)


## Installation and running
<!-- start installation-->
#### Installation
To install, run this code (please note that it requires Python >= 3.11): 

```
pip install morl4water
```

#### Running
An example on how to run a simulation:

```python
import mo_gymansium
import morl4water.examples

water_management_system = mo_gymnasium.make('nile-v0')

def run_nile():
    #reset
    obs, info = water_management_system.reset()
    print(f'Initial Obs: {obs}')
    final_truncated = False
    final_terminated = False
    for t in range(10):
        if not final_terminated and not final_truncated:
            action = water_management_system.action_space.sample()
            print(f'Action for month: {t}: {action}')

            (
                        final_observation,
                        final_reward,
                        final_terminated,
                        final_truncated,
                        final_info
                    ) = water_management_system.step(action)
            # print(f'Final final_info: ', final_info)
            print(f'Observation: {final_observation}')
            print(f'Reward: {final_reward}')         
        else:
            break
    return final_observation
run_nile()
```
<!-- end installation-->











<!-- [Structure](file:///C:/Users/milos/Desktop/ROB_Delft/Courses/Year_2/HIPPO_Internship/Active_Codes_HIPPO/morl4water/docs/_build/html/quickstart/code_structure.html) -->
<!-- To illustrate explanation further the Nile river simulation will serve as an example. Thus  -->
<!-- end creating a simulation -->

<!-- end main body -->
