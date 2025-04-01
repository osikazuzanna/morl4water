class Objective:

    @staticmethod
    def no_objective(*args):
        return 0.0

    @staticmethod
    def identity(value: float) -> float:
        return value

    @staticmethod
    def is_greater_than_minimum(minimum_value: float) -> float:
        return lambda value: 1.0 if value >= minimum_value else 0.0

    @staticmethod
    def is_greater_than_minimum_with_condition(minimum_value: float) -> float:
        return lambda condition, value: 1.0 if condition and value >= minimum_value else 0.0

    @staticmethod
    def deficit_minimised(demand: float, received: float) -> float:
        return -max(0.0, demand - received)

    @staticmethod
    def deficit_squared_ratio_minimised(demand: float, received: float) -> float:
        return -((max(0.0, demand - received) / demand) ** 2)

    @staticmethod
    def supply_ratio_maximised(demand: float, received: float) -> float:
        return received / demand if received / demand < 1.0 else 1.0

    @staticmethod
    def scalar_identity(scalar: float) -> float:
        return lambda value: value * scalar

    @staticmethod
    def sequential_scalar(scalar: list[float]) -> float:
        return lambda index, value: value * scalar[index]
