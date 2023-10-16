import os
import configparser
from terraclip import Terraclip

# USe configparser to retrieve my OpenTopography API key so I don't need to care about my API key being public after git push:
cf = os.path.join(os.getcwd(),"OTAPI.ini")
configParser = configparser.RawConfigParser()
configFilePath = cf
configParser.read(configFilePath)
MyOpenTopographyAPIkey = configParser.get("OTAPI", "api")

# Input file. Can be KML/KMZ, SHP, GPKG and possibly other formats supported by GDAL driver
tr = Terraclip(r'D:\srtm\ita.kml')
# Get a list of supported DEMs by Open Topography
dems = tr.listOTsources()
print(dems)

useMyownDEM = False
if useMyownDEM is False:
    # Set output folder to store downloaded DEMs (in the case of using Open Topography) and set the DEM source to be used
    tr.setdem(r'D:\srtm\DEM', OTsource='SRTMGL1', OTapi=MyOpenTopographyAPIkey)
else:
    # Or use your own DEM. Formats supported by GDAL driver
    tr.setdem(r'D:\srtm\DEM\mydem.tif')

# Set your output parameters. Sntax 'setparams(<flightAltitude>, <toleranceIn%>, <maxDistBetweenWPs>, Takeoff=<bool>, Land=<bool>)'
# Takeoff and Land are optional and defaults to 'False'
tr.setparams(120, 0, 500, Takeoff=False, Land=True)
# execute calculations
tr.execute()
# Print some stats
print(tr.rtlalt())
print(tr.maxterrain())
print(tr.minterrain())
print(tr.maxinc())
# Save results to a KML file
tr.savemission(r'D:\srtm\MP\mymission.kmz')
# Save results to a Ardupilot mission file and create a stats file
tr.savemission(r'D:\srtm\MP\mymission.txt')
# Save results to a shapefile. Or .gpkg, .pdf, or other files supported by GDAL driver
tr.savemission(r'D:\srtm\MP\mymission.shp')
tr.savemission(r'D:\srtm\MP\mymission.gpkg')
# Run again using different parameters
tr.setparams(120, 10, 200)
tr.execute()
tr.savemission(r'D:\srtm\MP\mymission2.kml')
tr.savemission(r'D:\srtm\MP\mymission2.txt')