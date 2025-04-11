## Creating a Simulation
<!-- start creating a sim - needed files -->
To create a new river simulation from scratch within morl4watwer package, it is necessary to create two new scripts and add the required data files related to reservoirs and other potential facilities. The needed files are as follows: 


1. **`[project name]_simulation.py`**  
This is where the river components (facilites like reservoirs, flows etc.) are defined as objects of classes and later installed in a list to form the whole river system for the simulation. The order ofcomponents is important and should follow the river flow. This file should be located in `morl4water/examples` directory.

2. **Data files (.txt)**  
The specific data files needed for creating a simulation depend on the number and type of facilities used in the river simulation. Please refer to explanations and the code of picked facilites to learn what data files are needed in your case. The data files should be located in `morl4water/examples/data/[project name]` directory. 

The precise explanations of the aforementioned scripts should be located in Structure section of this documentation. To illustrate how the list of all needed files could look like, the list of files for Nile river simulation is presented below. 
<!-- end creating a sim - needed files -->
### Nile Case
<!-- start creating sim - Nile case -->
Below one can see how the necessary scripts and data files were structured for the Nile river case. Only parts of the whole morl4water package containing the necessary scripts and files (green names) are presented.
- `morl4water/`: Root directory of the morl4water package.
    - **<span style="color: green;">`nile_example.py`</span>**: The main file where the environment is initialised.
    - `examples/`: Contains source code for the project.
      - **<span style="color: green;">`nile_river_simulation.py`</span>**: Defining river's components and ordering them with the river flow.
      - `data/`:
        - `nile_river/`:
          - `catchments/`: All data regarding water inflows to the river. To simplify only files related to Blue Nile inflow are shown here.
            - **<span style="color: green;">`InflowBlueNile.txt`</span>**: Data file with water flows of Blue Nile inflow.
          - `irrigation/`: All data regarding water demands for irrigation districts. To simplify only files related to Egypt district are shown here.
            - **<span style="color: green;">`irr_demand_Egypt.txt`</span>**: Data file with demands for Egypt district.
          - `reservoirs/`: All data regarding reservoirs. To simplify only files related to GERD reservoir are shown here.
            - **<span style="color: green;">`evap_GERD.txt`</span>**: Reservoir evaporation data.
            - **<span style="color: green;">`store_level_rel_GERD.txt`</span>**: Data relating reservoir's level(height) to reservoir's volume.
            - **<span style="color: green;">`store_min_max_release_GERD.txt`</span>**: Data relating max and min releases to reservoir's volume.
            - **<span style="color: green;">`store_sur_rel_GERD.txt`</span>**: Data relating reservoir's water surface to reservoir's volume.
<!-- end creating sim - Nile case -->
          
