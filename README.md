# RL4Water
<!-- start main body -->
<!-- Repository with a mondular gym environment, which lets you build a multi-objective water simulations to train you MORL agents on. -->
Welcome to morl4water, a flexible gym environment designed for simulating water management in river systems. With morl4water, 
you can build detailed water simulations and train or test your multi-objective reinforcement learning (MORL) agents in these settings. 
This guide will walk you through the key features of the tool. Please refer to the relevant sections based on your needs. 

Currently, we have three water systems implemented in a form of gym environments: Nile River Basin, Susquehanna River Basin and Omo River Basin.

Our toolkit is designed in a modular way, allowing users to build their own systems. For the overview of the systems, please go to System Elements.


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

water_management_system = mo_gymnasium.make('omo-v0')

def run_omo():
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
run_omo()
```
<!-- end installation-->


## Documentation

For detailed documentation, please visit [https://osikazuzanna.github.io/morl4water/](https://osikazuzanna.github.io/morl4water/)









<!-- [Structure](file:///C:/Users/milos/Desktop/ROB_Delft/Courses/Year_2/HIPPO_Internship/Active_Codes_HIPPO/morl4water/docs/_build/html/quickstart/code_structure.html) -->
<!-- To illustrate explanation further the Nile river simulation will serve as an example. Thus  -->
<!-- end creating a simulation -->

<!-- end main body -->
