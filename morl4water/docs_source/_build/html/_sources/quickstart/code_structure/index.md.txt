

# Code Structure Overview
<!-- start code structure - intro -->
MORL4Water models a multi-objective water resource management environment by simulating interconnected components like reservoirs, irrigation districts, power plants, inflows, and catchments. It is organized around facilities that exchange water via flows, all within an environment managed by a custom (MO)Gym-compatible class. 

Top-level, general structure of the codebase:

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

```

## Core Environment: `WaterManagementSystem`

The `WaterManagementSystem` class, defined in `core/envs/water_management_system.py`, implements a custom environment that is fully compatible with `mo-gymnasium.Env`. It simulates a complex water infrastructure system over time.

### Key Features
- Inherits from `gym.Env`
- Supports multi-objective settings
- Fully vectorized observation and reward spaces
- Modular design via a list of facilities and flow objects

### Components of the Gym Environment API

#### `__init__()`
- Initializes the environment with:
  - A list of components (facilities and flows)
  - A dictionary of reward signals
  - Start date and timestep duration
  - Optional timestamp and custom reward objectives
- Determines:
  - `observation_space` and `action_space`
  - `reward_space`
  - `max_capacities` (used to normalize observations)

#### `reset(seed, options)`
- Resets the environment state:
  - Sets date and timestep to initial values
  - Resets each facility's internal state
  - Returns normalized observation and info dictionary

#### `step(action)`
- Core simulation logic:
  - Propagates actions to `ControlledFacility` objects
  - Steps through all components (facilities, flows)
  - Aggregates rewards based on objectives
  - Advances the environment time
  - Returns:
    - `observation`: normalized state of `ControlledFacility`, which represents volume of water stored at the specific timestep in the Resevoir
    - `reward`: vector of objective values
    - `terminated`: True if the capacity of any Facility is exceeded 
    - `truncated`: False unless simulation ends
    - `info`: dictionary with simulation metadata

---

## Model Components

### `Facility` and `ControlledFacility`
- Base classes in `core/models/facility.py`
- `Facility` is for passive components (e.g. irrigation districts)
- `ControlledFacility` is for components with actions (reservoirs, reservoirs with a pump and weir)
- Provide common methods:
  - `reset()`, `step()`, `determine_reward()`, `determine_observation()`

### Flow Routing: `flow.py`
- `Flow`, `Inflow`, and `Outflow` classes define directed edges between components
- Handle delay, capacity, and direction of water flow
- Connect upstream and downstream `Facility` instances

### Objective Functions: `objective.py`
- Provides a library of scalarizable reward functions:
  - `deficit_minimised`, `scalar_identity`, etc.
- Used by each facility to compute its local reward contribution

### Specialized Components
- `Reservoir`, `ReservoirWithPump` (storage and release logic)
- `PowerPlant` (hydropower generation)
- `IrrigationDistrict` (demand satisfaction)
- `Catchment` (rainfall accumulation)
- `Weir` (overflow mechanisms)

Each inherits from either `Facility` or `ControlledFacility` and overrides reward and flow handling logic.

---

## Interaction Flow

1. User constructs an environment (e.g., via `create_nile_river_env()`)
2. Gym agent calls `reset()` and `step(action)`
3. Each component updates state, computes reward
4. `WaterManagementSystem` aggregates outputs and steps simulation

---

## Extensibility
- New components can be added by subclassing `Facility`
- Objectives can be extended in `objective.py`
- Works seamlessly with MO-RL algorithms via `gymnasium`

## Data Flow in the Environment

The environment simulates time-dependent water movement across interconnected infrastructure components. Each timestep, the environment performs the following sequence:

1. **External Inputs**  
   Components such as `Inflow` and `Catchment` introduce water into the system using external time-series data (e.g., rainfall or river inflows).

2. **Processing Nodes**  
   - `Reservoir`, `PowerPlant`, and `Weir` components store, transform, or release water based on physical constraints and action inputs.  
   - `IrrigationDistrict` components withdraw water based on predefined or data-driven demand.

3. **Routing**  
   - `Flow`, `Inflow`, and `Outflow` classes connect components, enforcing directionality, capacity limits, and transport delays.

4. **State Updates**  
   - Each facility and flow updates its internal state.
   - The environment collects and normalizes observations across all `ControlledFacility` components.

5. **Reward Calculation**  
   - Rewards are computed at the facility level using objective functions defined in `objective.py`.
   - The environment aggregates and normalizes these values into a vectorized reward output.



```{toctree}
:maxdepth: 1
:caption: Code Structure

updating_facilities
updating_flows

```
