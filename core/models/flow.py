from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Union, Optional
from core.models.facility import Facility, ControlledFacility
from gymnasium.core import ObsType


class Flow:
    def __init__(
        self,
        name: str,
        sources: list[Union[Facility, ControlledFacility]],
        destinations: Facility | ControlledFacility | dict[Facility | ControlledFacility, float],
        max_capacity: float,
        evaporation_rate: float = 0.0,
        delay: int = 0,
        default_outflow: Optional[float] = None,
    ) -> None:
        self.name: str = name
        self.sources: list[Union[Facility, ControlledFacility]] = sources

        if isinstance(destinations, Facility) or isinstance(destinations, ControlledFacility):
            self.destinations = {destinations: 1.0}
        else:
            self.destinations: dict[Union[Facility, ControlledFacility], float] = destinations

        self.max_capacity: float = max_capacity
        self.evaporation_rate: float = evaporation_rate

        self.delay: int = delay
        self.default_outflow: Optional[float] = default_outflow

        self.current_date: Optional[datetime] = None
        self.timestep_size: Optional[relativedelta] = None
        self.timestep: int = 0

    def determine_source_outflow(self) -> float:
        if self.timestep - self.delay < 0 and self.default_outflow:
            return self.default_outflow
        else:
            timestep_after_delay_clipped = max(0, self.timestep - self.delay)

            return sum(source.get_outflow(timestep_after_delay_clipped) for source in self.sources)

    def determine_source_outflow_by_destination(self, destination_index: int, destination_inflow_ratio: float) -> float:
        if self.timestep - self.delay < 0 and self.default_outflow:
            return self.default_outflow
        else:
            timestep_after_delay_clipped = max(0, self.timestep - self.delay)
            total_source_outflow = 0

            # Calculate each source contribution to the destination
            for source in self.sources:
                source_outflow = source.get_outflow(timestep_after_delay_clipped)

                # Determine if source has custom split policy
                if source.split_release:
                    total_source_outflow += source_outflow * source.split_release[destination_index]
                else:
                    total_source_outflow += source_outflow * destination_inflow_ratio

            return total_source_outflow

    def set_destination_inflow(self) -> None:
        for destination_index, (destination, destination_inflow_ratio) in enumerate(self.destinations.items()):
            destination_inflow = self.determine_source_outflow_by_destination(
                destination_index, destination_inflow_ratio
            )

            destination.set_inflow(self.timestep, destination_inflow * (1.0 - self.evaporation_rate))

    def is_truncated(self) -> bool:
        return False

    def determine_info(self) -> dict:
        return {"name": self.name, "flow": self.determine_source_outflow()}

    def step(self) -> tuple[Optional[ObsType], float, bool, bool, dict]:
        self.set_destination_inflow()

        terminated = self.determine_source_outflow() > self.max_capacity
        truncated = self.is_truncated()
        reward = float("-inf") if terminated else 0.0 
        info = self.determine_info()

        self.timestep += 1

        return None, reward, terminated, truncated, info

    def reset(self) -> None:
        self.timestep = 0


class Inflow(Flow):
    def __init__(
        self,
        name: str,
        destinations: Facility | ControlledFacility | dict[Facility | ControlledFacility, float],
        max_capacity: float,
        all_inflow: list[float],
        evaporation_rate: float = 0.0,
        delay: int = 0,
        default_outflow: Optional[float] = None,
    ) -> None:
        super().__init__(name, None, destinations, max_capacity, evaporation_rate, delay, default_outflow)
        self.all_inflow: list[float] = all_inflow

    def determine_source_outflow(self) -> float:
        if self.timestep - self.delay < 0 and self.default_outflow:
            return self.default_outflow
        else:
            timestep_after_delay_clipped = max(0, self.timestep - self.delay) % len(self.all_inflow)

            return self.all_inflow[timestep_after_delay_clipped]

    def determine_source_outflow_by_destination(self, destination_index: int, destination_inflow_ratio: float) -> float:
        if self.timestep - self.delay < 0 and self.default_outflow:
            return self.default_outflow
        else:
            timestep_after_delay_clipped = max(0, self.timestep - self.delay) % len(self.all_inflow)

            return self.all_inflow[timestep_after_delay_clipped] * destination_inflow_ratio

    def is_truncated(self) -> bool:
        return self.timestep >= len(self.all_inflow)


class Outflow(Flow):
    def __init__(
        self,
        name: str,
        sources: list[Union[Facility, ControlledFacility]],
        max_capacity: float,
    ) -> None:
        super().__init__(name, sources, None, max_capacity)

    def set_destination_inflow(self) -> None:
        pass
