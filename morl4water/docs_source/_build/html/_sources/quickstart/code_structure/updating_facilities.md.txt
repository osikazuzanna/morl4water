## Updating Facilities
<!-- start updating facilities-->
In general, the river environment is updated with `.step()` as implemented in ``water_management_system.py``. Next, this method comes down to activating `.step()` of particular facilities either instances of `ControlledFacility` or `Facility` superclass. The full implementation of superclasses can be found in `morl4water/models/facility.py`. Nevertheless, for both of those, their `.step()` methods are very similar and structured in a similar way:

1. **Appending self.all_outflow list** - Appending list of outflow rates [m^3/s] based on the current action for this facility.
2. **Providing observation variable** - Providing the current state of the facility [Only ControlledFacility] 
2. **Determinig a potential reward** - Each facility may have an objective assigned to it in `nile_river_simulation.py`.
3. **Checking if terminated** - Check if a potential constraint has been violated to end an episode.
4. **Checking if truncated** - Check if an external condition (like time limit) should end an episode. 
5. **Checking info** - Providing useful information about a facility in an `info` variable.   

An examplary `.step()` method for `ControlledFacility` is presented below: 

```python
    def step(self, action: ActType) -> tuple[ObsType, SupportsFloat, bool, bool, dict]:
        self.all_outflow.append(self.determine_outflow(action))

        observation = self.determine_observation()
        reward = self.determine_reward()
        terminated = self.is_terminated()
        truncated = self.is_truncated()
        info = self.determine_info()

        self.timestep += 1

        return (
            observation,
            reward,
            terminated,
            truncated,
            info,
        )
```
Now all of those parts of `.step()` method are handled by additional methods. Please note that some of those are defined differently for each element of the river system. Thus, to exactly see what it is behind a method you may need to refer to specific classes like reservoir etc., these can be found in `morl4water/models`. However, a high-level overview is provided below:

1. **self.determine_outflow()** - This method is responsible for making the water flow through a river element. For instances of `Facility` superclass it is one of the `Facility` methods. For instances of `ControlledFacility` superclass, one should look for the implementation within the specific class. The next section will develop more on this method.

2. **self.determine_reward()** - This refers to the method implemented in a specific class where `self.objective_function()` takes an argument and returns the reward. The `self.objective_function` is assigned to an instance of the class at its creation in `nile_river_simulation.py` as one of standard functions from `morl4water/core/models/objective.py`.

3. **self.is_terminated()** - For instances of the `Facility` superclass, this method originates from the `Facility` class and returns `False` by default. In contrast, for instances of the `ControlledFacility` superclass, the method is defined within their specific class. For instance, in the case of reservoirs, the method will return `True` if the volume of stored water exceeds its physical limits.

4. **self.is_truncated()** - This method is implemented directly in `ControlledFacility` and `Facility` superclasses. In the current state of development it always returns `False`. 

5. **self.determine_info()** - This refers to the method implemented in a specific class. Based on the class it can return a dictionary with different information. 

<!-- end updating facilities-->

### Determining Facilities Outflows
<!-- start updating facilities - Determining Facilities Outflows intro -->
Determining outflows of system's elements in the river environment is a critical part of the `.step()` method in each superclass. The function `self.determine_outflow()` allows water to flow through river elements and updates their states. The implementation of this function varies between the two superclasses.
<!-- end updating facilities - Determining Facilities Outflows intro -->

#### `Facility` Outflows
<!-- start updating facilities - `Facility` Outflows -->
For `Facility` superclass, the method `self.determine_outflow()` is defined directly within itself:

```python
    def determine_outflow(self) -> float:
        return self.get_inflow(self.timestep) - self.determine_consumption()
```
Now `self.determine_consumption()` method comes from a specific element class and `self.get_inflow()` is a method of `Facility` superclass returning an inflow for a specific `self.timestep`. The `self.get_inflow()` is, in turn, defined as:

```python
    def get_inflow(self, timestep: int) -> float:
        return self.all_inflow[timestep]
```
The `self.all_inflow` list is a list of inflows which is updated by another method within `Facility` superclass called `set_inflow`:

```python
    def set_inflow(self, timestep: int, inflow: float) -> None:
        if len(self.all_inflow) == timestep:
            self.all_inflow.append(inflow)
        elif len(self.all_inflow) > timestep:
            self.all_inflow[timestep] += inflow
        else:
            raise IndexError
```
The use of `if` and `elif` statements is necessary due to the potential for multiple inflows converging on a single facility. Given the structure of `morl4water`, the `set_inflow` method is invoked during updates of `Flow` objects. This means that `Flow` objects must be called before instances of `Facility` in the river system (this comes from elements ordering in `nile_river_simulation.py`), ensuring that there is always a flow connecting a node to the rest of the system. These `Flow` objects serve as crucial components within the overall river system, linking various `Facility` and `ControlledFacility` objects. Specifically, the `set_inflow` method is called within the `Flow` superclass in the `set_destination_inflow()` method to append the inflow rates to the `self.all_inflow` list of its destination node.

<!-- end updating facilities - `Facility` Outflows -->

#### `ControlledFacility` Outflows
<!-- start updating facilities - `ControlledFacility` Outflows -->
For `ControlledFacility` superclass, the `self.determine_outflow()` works a bit differently. Mainly, the `self.determine_outflow()` actually receives an action based on which the facility state will change. Because of this and because this action can diffferently affect the instance of `ControlledFacility`, the `self.determine_outflow()` method itself is implemented within the specific class of the river element. Usually it is a reservoir where the full process of updating water within itself is calculated based on the RL Agent's action and water evaporation based on the reservoir's data. This whole process for a reservoir can be seen in `morl4water/models/reservoir.py`. 
<!-- end updating facilities - `ControlledFacility` Outflows -->