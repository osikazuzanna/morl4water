## Updating Flows
<!-- start updating flows-->
Instances of `Flow` superclass just as instances of facilites must be updated within each iteration of the main `.step()` method in `water_management_system.py`. Basically for objects of `Flows` the following `.step()` method applies:

```python
    def step(self) -> tuple[Optional[ObsType], float, bool, bool, dict]:

        self.set_destination_inflow()

        terminated = self.determine_source_outflow() > self.max_capacity
        truncated = self.is_truncated()
        reward = float("-inf") if terminated else 0.0 
        info = self.determine_info()

        self.timestep += 1

        return None, reward, terminated, truncated, info
```
The core function of the `.step()` method lies in the `.set_destination_inflow()` method. This function determines the flow's destinations and any associated distribution ratios, then calculates the appropriate inflow for each destination. It does so by assessing the total inflow to the flow object and applying the distribution ratios to allocate the correct inflow amount to each destination. This is presented here:

```python
    def set_destination_inflow(self) -> None:

        for destination_index, (destination, destination_inflow_ratio) in enumerate(self.destinations.items()):
            destination_inflow = self.determine_source_outflow_by_destination(
                destination_index, destination_inflow_ratio
            )

            destination.set_inflow(self.timestep, destination_inflow * (1.0 - self.evaporation_rate))
```
<!-- end updating flows-->
