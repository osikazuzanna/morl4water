from core.models.facility import Facility


class Catchment(Facility):
    def __init__(self, name: str, all_water_accumulated: list[float]) -> None:
        super().__init__(name)
        self.all_water_accumulated: list[float] = all_water_accumulated

    def determine_reward(self) -> float:
        return 0

    def get_inflow(self, timestep: int) -> float:
        return self.all_water_accumulated[timestep % len(self.all_water_accumulated)]

    def determine_consumption(self) -> float:
        return 0

    def is_truncated(self) -> bool:
        return self.timestep >= len(self.all_water_accumulated)

    def determine_info(self) -> dict:
        return {"water_consumption": self.determine_consumption()}
