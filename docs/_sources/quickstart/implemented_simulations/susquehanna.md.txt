### Susquehanna
<!-- start implemented simulations -Susquehanna -->
The Susquehanna River, regulated by the Conowingo Dam, supports diverse needs, including hydroelectric power, water supply, and recreation. However, low-flow conditions create challenging trade-offs, forcing Conowingo to balance energy production with environmental and community water needs.

Originally, the simulation starts at **(2021, 1, 1)** and the decisions are made every 4 hours throughout a year resulting in **2190 time steps** per episode (the whole simulation). It also has 6 following objectives:


1. <span style="color:blue"> Recreation (max), ref point: 0.0<span style="color:blue">
2. <span style="color:blue"> Energy revenue (max), ref point: 0.0 <span style="color:blue">
3. <span style="color:blue"> Baltimore (max), ref point: 0.0  <span style="color:blue">
4. <span style="color:blue"> Atomic (max), ref point: 0.0 <span style="color:blue">
5. <span style="color:blue"> Chester (max), ref point: 0.0 <span style="color:blue">
6. <span style="color:blue"> Environment (min), ref point: -2190 <span style="color:blue">

Where max/main signifies whether an objective is to be maximised or minimised. The reference point is used for calculating hypervolume as the worst case scenario in terms of acquired rewards by the agent at the end of the simulation.


- Observation space: Water level, month (2 dimensions)
- Action space: Release per each reservoir (4 dimensions)

Here you can see a picture visualising Omo river structure:
<img src="../../_static/_images/susq_struct.png" alt="Alt text" style="width: 50%;" />


#### Running

```python
import mo_gymnasium
import morl4water.examples

water_management_system = mo_gymnasium.make('susquehanna-v0')

def run():
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
run()
```

Taken from: _Muniak, K. (2024). RL4Water: Reinforcement Learning Environment for Water Management (Bachelor’s thesis). Delft University of Technology, Faculty of EEMCS._
<!-- end implemented simulations -Susquehanna -->

#### Data & Data Sources
<!-- start Data -->

| **Data**                                      | **Facility**                                     | **Value**                                                                                   | **Source**                       |
|----------------------------------------------|--------------------------------------------------|---------------------------------------------------------------------------------------------|----------------------------------|
| max release                                  | Conowingo (with 4 outflows)                      | 41.302169, 464.16667, 54.748458, 85412                                                      | Salazar et al. (2024)           |
| initial storage                              | Conowingo reservoir with Muddy Run Pump          | 2.6BCM                                                                                      | Salazar et al. (2024)           |
| max capacity                                 | Conowingo reservoir with Muddy Run Pump          | 7BCM                                                                                        | Salazar et al. (2024)           |
| evaporation rate                             | Conowingo reservoir with Muddy Run Pump          | Daily evaporation rates for Conowingo (see `examples/data/susquehanna/reservoir`)           | Salazar et al. (2024)           |
| storage to min max release                   | Conowingo reservoir with Muddy Run Pump          | Tabular data (see `examples/data/susquehanna_river/reservoirs`)                            | Salazar et al. (2024)           |
| storage to level to surface relationship     | Conowingo reservoir with Muddy Run Pump          | Tabular data for Conowingo                                                                 | Salazar et al. (2024)           |
| initial storage of the pump                  | Conowingo reservoir with Muddy Run Pump          | 1.9BCM                                                                                      | Salazar et al. (2024)           |
| evaporation rates of the pump                | Conowingo reservoir with Muddy Run Pump          | Daily evaporation rates for Muddy Run (see `examples/data/susquehanna/reservoir`)           | Salazar et al. (2024)           |
| storage to level to surface relationship pump| Conowingo reservoir with Muddy Run Pump          | Tabular data for Muddy Run Pump                                                             | Salazar et al. (2024)           |
| pumping rules                                | Conowingo reservoir with Muddy Run Pump          | Function `muddyrun_pumpturb` in main Susquehanna script                                     | Salazar et al. (2024)           |
| inflows to the pump                          | Conowingo reservoir with Muddy Run Pump          | Daily inflow data to Muddy Run                                                              | Salazar et al. (2024)           |
| efficiency                                   | Conowingo Power Plant                            | 79%                                                                                        | Salazar et al. (2024)           |
| head start level                             | Conowingo Power Plant                            | 0                                                                                           | Salazar et al. (2024)           |
| n_turbines                                   | Conowingo Power Plant                            | 13                                                                                          | Salazar et al. (2024)           |
| water demand                                 | Atomice, Baltimore and Chester Irrigation Districts | Daily time series data with water demand                                                  | Salazar et al. (2024)           |
| turbines                                     | Conowingo Power Plant                            | Tabular data with min/max turbine flow per turbine                                          | Salazar et al. (2024)           |
| inflow                                       | Later and Main Conowingo Inflow                  | Daily time series data of inflows                                                           | Salazar et al. (2024)           |


<!-- end Data -->
