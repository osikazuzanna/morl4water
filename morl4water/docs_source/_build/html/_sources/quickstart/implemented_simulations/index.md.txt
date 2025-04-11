## Water Simulations
<!-- start implemented simulations -->


Below is a summary of the implemented simulations in `morl4water`, showing key configuration properties such as duration, objective count, and state/action dimensions. Please note, morl4water assumes observation space and action space to be continous and normalizes the values based on the provided maximum value for each component.

| Simulation   | Timesteps & Size             | # Objectives | Obs. Space Dim | Action Space Dim |
|--------------|-------------------------------|--------------|----------------|------------------|
| [**Nile**](nile.md)         | 240 steps (monthly)         | 4         | 5              | 4                |
| [**Susquehanna**](susquehanna.md) | 2190 steps (4-hourly)       | 6         | 2              | 4                |
| [**Omo**](omo.md)          | 144 steps (monthly)         | 3           | 4              | 3                |




They all differ in their structure, river elements, observation space, action space and objectives. Below you should be able to find detailed descriptions of these simulations.
The code structure for the implemented simulations: 

```text
morl4water
├── core    
├── examples
│   ├── data
│   │   ├── nile_river
│   │   │   ├── catchments
│   │   │   ├── irrigation
│   │   │   └── reservoirs
│   │   ├── omo_river
│   │   │   ├── catchments
│   │   │   ├── irrigation
│   │   │   └── reservoirs
│   │   └── susquehanna_river
│   │       ├── demands
│   │       ├── inflows
│   │       └── reservoirs
│   ├── nile_river_simulation.py
│   ├── omo_river_simulation.py
│   └── susquehanna_river_simulation.py
```


<!-- end implemented simulations -->





```{toctree}
:maxdepth: 1
:caption: Implemented Simulations

nile
susquehanna
omo

```