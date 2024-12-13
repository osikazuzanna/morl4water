# WaterManagementSystem

Inputs:
- water_systems: list of all the water systems including reservoirs, flows, irrigation districts, arranged from the upstream to downstream
- rewards: dictionary with all the names of the rewards (defined in the water systems) with their initial value
- start_date: start date of the simulation
- timestep_size: timestep between each release decision - one month, one hour, 4 hours, one day etc.
- add_timestamp: timestamp added to the observation ('m' month of the year, 'h' hour of the day, 'd' day of the year)
- custom_obj: used when creating instances of the same environment with different objectives, a list of names of rewards

methods: reset - sets the seed, sets the start date, sets the initial storage in the reservoirs
step: iterates over all the components of the water system 

Metric system:
Water reservoir is measured with water level (eg. meters) or storage volume (eg. in m3). Our measurement system currently is in storage volume, but for Susquehanna we introduce how it can be recalculated into measuring in storage.

## Flow
 determines flows between different facilities

## Water simulations

Currently we have 2 real-world water simulations with objectives varying from 2 - 6 (in total 8 simulations available).

- **Nile** - originally, it has 4 objectives:
  - Ethiopia power (max)
  - Sudan deficit (min)
  - Egypt deficit (min)
  - HAD minimum level (max)
- **Susquehanna**
  - Recreation (max)
  - Energy revenue (max)
  - Baltimore (max)
  - Atomic (max)
  - Chester (max)
  - Environment (max)

As MORL algorithms have only been tested with a maximum of 3 objectives, we are testing the algorithms for cases with 2, 3, and 4 objectives per each simulation. Thus, we have 6 different cases to test against:

- **Nile:**
  - 2 objectives: Ethiopia power (max) and Egypt deficit (min)
  - 3 objectives: Ethiopia power (max), Egypt deficit (min), and Sudan deficit (min)
  - 4 objectives: All original objectives
- **Susquehanna:**
  - 2 objectives: Baltimore (max) vs Chester (max)
  - 3 objectives: Baltimore (max), Atomic (max), Chester (max)
  - 4 objectives: Baltimore (max), Atomic (max), Chester (max), Recreation (max)

**Nile - Settings**
- Observations: Storage in 4 reservoirs, month (5 dimensions)
- Actions: Release per each reservoir (4 dimensions)

**Susquehanna - Settings**
- Observations: Water level, month (2 dimensions)
- Actions: Release per each destination (4 dimensions)


## Usage


## Docs


## Running

- **Nile:** ``mo_gymnasium.make('nile-v0')``
  - 2 objectives: ``mo_gymnasium.make('nile2-v0')``
  - 3 objectives: ``mo_gymnasium.make('nile3-v0')``
  - 4 objectives: ``mo_gymnasium.make('nile-v0')``
- **Susquehanna:** ``mo_gymnasium.make('susquehanna-v0')``
  - 2 objectives: ``mo_gymnasium.make('susquehanna2-v0')``
  - 3 objectives: ``mo_gymnasium.make('susquehanna3-v0')``
  - 4 objectives: ``mo_gymnasium.make('susquehanna4-v0')``



