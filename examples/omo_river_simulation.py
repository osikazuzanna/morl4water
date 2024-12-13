import numpy as np
from pathlib import Path
from gymnasium.spaces import Box
from gymnasium.wrappers.time_limit import TimeLimit
from core.envs.water_management_system import WaterManagementSystem
from core.models.reservoir import Reservoir
from core.models.weir import Weir
from core.models.flow import Flow, Inflow
from core.models.objective import Objective
from core.models.power_plant import PowerPlant
from core.models.irrigation_district import IrrigationDistrict
from core.models.catchment import Catchment
from core.wrappers.transform_action import ReshapeArrayAction
from datetime import datetime
from dateutil.relativedelta import relativedelta
from gymnasium.envs.registration import register

data_directory = Path(__file__).parents[1] / "examples" / "data" / "omo_river"

register(
    id='omo-v0',
    entry_point='examples.omo_river_simulation:create_omo_river_env',
)


#TODO translate all flows and nodes:

#reservoirs: Gibe_III_reservoir, Koysha_reservoir
#Power plants: Gibe_III_power_plant, Koysha_power_plant
#weir: Kuraz Headworks
#Inflow: Flow A, Flow B, Flow C
#Flow: Gibe_III_reservoir_to_power_plant, Koysha_reservoir_to_power_plant, Gibe_III_Release, Koysha_Release, {Main_Channel, Canals_to_Kuraz}, 
#Irrigation: Omorate, Canals to Kuraz Sugar Plantations



def create_omo_river_env(custom_obj = None, render_mode=None) -> WaterManagementSystem:


    #Gibe_III
    GIBE_III_reservoir = Reservoir(
        "GIBE_III",
        max_capacity=11750000000.0, #m^3 11750000000.0
        max_action=[1064], #From Yugdeep it is equal to turbine_max_flow_rate (implemented in scaling actions back after rbf network)
        integration_timestep_size=relativedelta(minutes=720), #integration timestep in Omo is 12 hours ()
        objective_function=Objective.no_objective,
        stored_water=11750000000.0, #initial state 11750000000.0
        evap_rates=np.loadtxt(data_directory / "reservoirs" / "evap_GIBE_III.txt"), # cm/month
        evap_rates_timestep_size=relativedelta(months=1), # TODO How does it work again?
        storage_to_minmax_rel=np.loadtxt(data_directory / "reservoirs" / "store_min_max_release_GIBE_III.txt"),#m^3/s #Yugdeep does not change the max/min actions based on storage. The file shows contant min and max value 
        storage_to_level_rel=np.loadtxt(data_directory / "reservoirs" / "store_level_rel_GIBE_III.txt"), #data for interpolating from storage to height
        storage_to_surface_rel=np.loadtxt(data_directory / "reservoirs" / "store_sur_rel_GIBE_III.txt"), #data for interpolating from storage to surface
    )

    GIBE_III_power_plant = PowerPlant(
        "GIBE_power_plant",
        Objective.scalar_identity(1),
        "hydro_power_GIBE_and_Koysha",
        efficiency=0.9,
        min_turbine_flow=0,
        max_turbine_flow=1064,
        head_start_level=9, #level of the turbine needed for power calc
        max_capacity=1870, # maximal capacity of power production in Mw
        reservoir=GIBE_III_reservoir,
        normalize_objective=1391280 * 2  #the max amount of electricity produced possible in one month based on the max capacity : 31*24*max_capacity, times 2 because it shares an objective with Koysha
    )   
    #Koysha
    KOYSHA_reservoir = Reservoir(
        "KOYSHA",
        max_capacity=6000000000.0, #m^3
        max_action=[1440], #From Yugdeep it is equal to turbine_max_flow_rate (implemented in scaling actions back)
        integration_timestep_size=relativedelta(minutes=720), #integration timestep in Omo is 12 hours
        objective_function=Objective.no_objective,
        stored_water=6000000000.0/2, #initial state
        evap_rates=np.loadtxt(data_directory / "reservoirs" / "evap_KOYSHA.txt"), # cm/month
        evap_rates_timestep_size=relativedelta(months=1),
        storage_to_minmax_rel=np.loadtxt(data_directory / "reservoirs" / "store_min_max_release_KOYSHA.txt"),
        storage_to_level_rel=np.loadtxt(data_directory / "reservoirs" / "store_level_rel_KOYSHA.txt"), #data for interpolating from storage to height
        storage_to_surface_rel=np.loadtxt(data_directory / "reservoirs" / "store_sur_rel_KOYSHA.txt") #data for interpolating from storage to surface
    )

    KOYSHA_power_plant = PowerPlant(
        "KOYSHA_power_plant",
        Objective.scalar_identity(1),
        "hydro_power_GIBE_and_Koysha",
        efficiency=0.9,
        min_turbine_flow=0,
        max_turbine_flow=1440.0,
        head_start_level=8.5, #level of the turbine needed for power calc
        max_capacity=2160.0, # maximal capacity of power production
        reservoir=GIBE_III_reservoir,
        normalize_objective= 1607040.0 * 2 #the max amount of electricity produced possible in one month based on the max capacity
    )

    #IRRIGATION DISTRICTS
    Canals_to_Kuraz_Sugar_Plantations = IrrigationDistrict(
        "Canals_to_Kuraz_Sugar_Plantations_irr",
        np.loadtxt(data_directory / "irrigation" / "irr_demand_Kuraz.txt"), #TODO what is the unit here?
        Objective.deficit_minimised,
        "Kuraz_deficit_minimised",
        normalize_objective=105.45 #simply the highest monthly demand in a year
    )

    Omorate = IrrigationDistrict(
        "Omorate_irr",
        np.loadtxt(data_directory / "irrigation" / "irr_demand_Omorate.txt"),
        Objective.deficit_minimised,
        "Omorate_deficit_minimised",
        normalize_objective=328.39 #simply the highest monthly demand in a year
    )

    # -------------------------------- Testing -------------------------------------------------------

    #KURAZ WEIR
    KURAZ_Headworks_weir = Weir(
        "KURAZ",
        max_capacity= 1440, #m^3 used for termination so its fine / observation space is given [0, 1] by default/ TODO but max capacity is used for space normalisation / Thus, Use max rate of the incoming water, for example Koysha max release rate?
        max_action=[1440], #As a max action this should be the release to one of the destinations
        integration_timestep_size=relativedelta(minutes=720), #integration timestep in Omo is 12 hours
        objective_function=Objective.no_objective,
        stored_water=0.0 #initial state - should be default inflow to the weir
    )

    #INFLOWS
    Flow_A_inflow = Inflow(
        "Flow_A_inflow",
        GIBE_III_reservoir,
        float("inf"),
        np.loadtxt(data_directory / "catchments" / "Flow_A_inflow.txt") # m^3/s
    )

    Flow_B_inflow = Inflow(
        "Flow_B_inflow",
        KOYSHA_reservoir,
        float("inf"),
        np.loadtxt(data_directory / "catchments" / "Flow_B_inflow.txt")
    )

    Flow_C_inflow = Inflow(
        "Flow_C_inflow",
        Omorate,
        float("inf"),
        np.loadtxt(data_directory / "catchments" / "Flow_C_inflow.txt")
    )
    #FLOWS

    GIBE_III_to_plant_flow = Flow("GIBE_III_to_plant_flow", [GIBE_III_reservoir], GIBE_III_power_plant, float("inf"))

    GIBE_III_Release_flow = Flow("GIBE_III_Release_flow", [GIBE_III_power_plant], KOYSHA_reservoir, float("inf"))
    
    KOYSHA_to_plant_flow = Flow("KOYSHA_to_plant_flow", [KOYSHA_reservoir], KOYSHA_power_plant, float("inf"))

    KOYSHA_Release_flow = Flow("KOYSHA_Release_flow", [KOYSHA_power_plant], KURAZ_Headworks_weir, float("inf"))

    #WEIR object - the values to destinations an be anything because thery are overwritten in the class by the Agent's Action
    KURAZ_Headworks_Weir_Release_flow = Flow("KURAZ_Headworks_Weir_Release_flow", [KURAZ_Headworks_weir], 
                                             destinations={Canals_to_Kuraz_Sugar_Plantations: "Agent's Action", Omorate: "Agent's Action"}, 
                                             max_capacity = float("inf"))


    # Create water management system. Add Facilities in the topological order (in the list).
    # deficit reward goes negative when there is a deficit. Otherwise is 0.
    water_management_system = WaterManagementSystem(
        water_systems=[
            Flow_A_inflow,
            GIBE_III_reservoir,
            GIBE_III_to_plant_flow,
            GIBE_III_power_plant,
            GIBE_III_Release_flow,
            Flow_B_inflow,
            KOYSHA_reservoir,
            KOYSHA_to_plant_flow,
            KOYSHA_power_plant,
            KOYSHA_Release_flow,
            KURAZ_Headworks_weir,
            KURAZ_Headworks_Weir_Release_flow,
            Flow_C_inflow,
            Canals_to_Kuraz_Sugar_Plantations,
            Omorate,
        ],
        rewards={
            "hydro_power_GIBE_and_Koysha": 0,
            "Kuraz_deficit_minimised": 0,
            "Omorate_deficit_minimised": 0,
        },
        start_date=datetime(2029, 1, 1),
        timestep_size=relativedelta(months=1),
        seed=42
        ,add_timestamp='m', #adds month as a percentage (x/12) to observation space
        custom_obj=custom_obj
        
    )

    water_management_system = ReshapeArrayAction(water_management_system)
    water_management_system = TimeLimit(water_management_system, max_episode_steps=144) #normally 144 for 12 years

    return water_management_system
