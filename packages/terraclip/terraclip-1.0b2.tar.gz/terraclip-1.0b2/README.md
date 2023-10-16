This is a python class to generate Ardupilot mission files and auxiliary files (Stats file and export files). 
The output mission file contains WP's set to 'ABSOLUTE' heights for better mission previsibility and can be imported directly in Mission Planner.  

## Beta (and use at your own risk)
- Evaluation site: https://rodrigo-nh.github.io/TerraclipTestPage/
## Features
- Configurable parameters (flight altitude, altitude tolerance, max distance between WPs, takeoff/land optional commands)
- Anti-collision check, guarantees minimal altitude above ground along all flight path
- Exports to reference KML file (and other formats) containing 3D WP's, paths and stats
- Doesn't care about your vector/DEM input files DATUM/CRS, converts accordingly
- Downloads necessary DEM scenes automatically (requires a Open Topography API key https://opentopography.org/) or loads custom user DEM.
- Outputs a stat file containing minimal flight altitude, max flight altitude, max generated inclination and suggested RTL_ALT (max DEM scene altitude plus ```<flightAlt>```)
## How it works
- Draw a path in GoogleEarth containing desired flight path. Export the path to a KML/KMZ file. Generated mission will respect the vertices from your path, converting vertices to WP's.  
   
- Check example.py about how to use it. The parameters are set by the command:  
  
  ```setparams(<flightAlt>, <tolerance>, <maxDistBetweenWPs>, Takeoff=<bool>, Land=<bool>)```  
  
  ```<flightAlt>``` => Flight altitude above ground. This will be the minimal altitude to be respected along all path  
  ```<tolerance>``` => Flight altitude tolerance (in %). Means Minimal altitude along path can reach ```<flightAlt>``` minus tolerance  
  ```<maxDistBetweenWPs>``` => Divide your original WP's into sections (creating another WP's), respecting this max distance between WP's. The lower this parameter the more a 'terrain following' effect. Set this to zero to not create any aditional WP's.  
  ```Takeoff=<bool>``` => Optional. Converts the first WP's from your file into Takeoff command  
  ```Land=<bool>``` => Optional. Converts the last WP from your file into Land command.  
## How to install
- pip install terraclip
- Requires Python > 3
- Requires gdal python bindings (Windows users can try this recipe for the python bindings https://gist.github.com/Rodrigo-NH/94d1fe07646052ad32133824c85b4221)
- Requires numpy and gdalwrap (check requirements.txt)