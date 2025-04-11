from core.models.facility import ControlledFacility
from gymnasium.spaces import Box, Space
import numpy as np
from dateutil.relativedelta import relativedelta
from datetime import datetime
from numpy.core.multiarray import interp as compiled_interp


class Weir(ControlledFacility):
    """
    A class used to represent reservoirs of the problem

    Attributes
    ----------
    name: str
        Lowercase non-spaced name of the reservoir
    storage_vector: np.array (1xH)
        m3
        A vector that holds the volume of the water in the reservoir
        throughout the simulation horizon
    level_vector: np.array (1xH)
        m
        A vector that holds the elevation of the water in the reservoir
        throughout the simulation horizon
    release_vector: np.array (1xH)
        m3/s
        A vector that holds the actual average release per month
        from the reservoir throughout the simulation horizon
    evap_rates: np.array (1x12)
        cm
        Monthly evaporation rates of the reservoir

    Methods
    -------
    determine_info()
        Return dictionary with parameters of the reservoir.
    storage_to_level(h=float)
        Returns the level(height) based on volume.
    level_to_storage(s=float)
        Returns the volume based on level(height).
    level_to_surface(h=float)
        Returns the surface area based on level.
    determine_outflow(action: float)
        Returns average monthly water release.
    """

    def __init__(
        self,
        name: str,
        max_capacity: float,
        max_action: list[float],
        objective_function,
        integration_timestep_size: relativedelta,
        objective_name: str = "",
        stored_water: float = 0,
        spillage: float = 0,
        observation_space = Box(low=0, high=1),
        action_space = Box(low=0, high=1),

                ) -> None:
        super().__init__(name, observation_space, action_space, max_capacity, max_action)
        self.stored_water: float = stored_water

        self.should_split_release = True
        
        
        self.storage_vector = []
        self.level_vector = []
        self.release_vector = []

        # Initialise storage vector
        self.storage_vector.append(stored_water)

        self.objective_function = objective_function
        self.objective_name = objective_name

        self.integration_timestep_size: relativedelta = integration_timestep_size
        self.spillage = spillage


    def determine_reward(self) -> float:
        #Pass average inflow (which is stored_water ) to reward function
        return self.objective_function(self.stored_water)

    def determine_outflow(self, actions: np.array) -> list[float]:

        destination_1_release = np.empty(0, dtype=np.float64)
        weir_observation_lst = []

        final_date = self.current_date + self.timestep_size

        while self.current_date < final_date:
            next_date = min(final_date, self.current_date + self.integration_timestep_size)

            #See what is the current inflow to weir and scale up the action to the first destination ( the action is a percentage of water going to destination 1)
            weir_observation = self.get_inflow(self.timestep)
            max_action = weir_observation 
            actions_scaled_up = actions*max_action

            destination_1_release = np.append(destination_1_release, actions_scaled_up)

            weir_observation_lst = np.append(weir_observation_lst, weir_observation)
            
            self.current_date = next_date

        #Averaging inflow to weir over last step (usually month) as a potential observation space to be used
        average_release = np.mean(weir_observation_lst, dtype=np.float64)
        self.storage_vector.append(average_release) #TODO does it make sense to keep it?
        self.stored_water = average_release # TODO used in determine_observation
      
        #potential storage (observation space understood as total inflow) is same as the total release
        self.release_vector.append(average_release)

        # Split release for different destinations, action is expected to be in range [0,1]
        self.split_release = [actions, (1-actions)]
        

        return average_release

    def determine_info(self) -> dict:
        info = {
            "name": self.name,
            "average_release": self.stored_water,
        }
        return info

    def determine_observation(self) -> float:
        if self.stored_water > 0:
            return self.stored_water
        else:
            return 0.0

    def is_terminated(self) -> bool:
        return self.stored_water > self.max_capacity or self.stored_water < 0
    
    def reset(self) -> None:
        super().reset()
        stored_water = self.storage_vector[0]
        self.storage_vector = [stored_water]
        self.stored_water = stored_water
        self.level_vector = []
        self.release_vector = []
