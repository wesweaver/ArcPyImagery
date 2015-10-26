# Description: 	This tool is designed to cut tiles from an ArcGIS Mosaic Dataset.
#				Using the Mosaic Dataset and a shapefile as inputs, it will loop
#				through the rows in the shapefile's attribute table and extract the
#				imagery to the geometry of each polygon in the shapefile. This script
#				will output a .tif image with associated .tfw, .ovr, .tif.aux and
#				.tif (xml) files.
#
#				A name field is required in the shapefile that identifies unique polygons.
#				This field serves two functions: 1) it directs the script to select the cut
#				polygon by name and 2) the output images will be assigned the name of the
#				cut polygon ([NAME].tif).
#
# Environment: ArcGIS
# Written by: Wes Weaver
# Date: February 25, 2014

import arcpy
import os
import time

#Specify input mosaic dataset
mosaic = arcpy.GetParameterAsText(0)

#Specify extraction feature set
extract = arcpy.GetParameterAsText(1)

#Specify name field
name = arcpy.GetParameterAsText(2)

#Specify output workspace
outWorkspace = arcpy.GetParameterAsText(3)

# Set compression type and level
arcpy.env.compression = arcpy.GetParameterAsText(4)

# Set Output Coordinate System
arcpy.env.outputCoordinateSystem = arcpy.GetParameterAsText(5)

# Check out Spatial Analyst extension
arcpy.CheckOutExtension("Spatial")

# Allow overwrite
arcpy.env.overwriteOutput = True

arcpy.env.nodata = "MAP_UP"

cursor = arcpy.SearchCursor(extract)

for row in cursor:
	 #row = cursor.next() #activate this line to skip every other row and start at 2 for processing on two machines
	 start = time.clock()
	 arcpy.MakeFeatureLayer_management(extract, "selectfrom")
	 selectby = row.getValue(name)
	 arcpy.SelectLayerByAttribute_management("selectfrom", "NEW_SELECTION", '"NAME" = ' + "'" + selectby + "'")
	 arcpy.CopyFeatures_management ("selectfrom", "selectlayer")
	 arcpy.AddMessage("Extracting: " + mosaic + " to " + selectby)
	 arcpy.Clip_management(mosaic, "#", os.path.join(outWorkspace, selectby + ".tif"), "selectlayer", "ClippingGeometry")
	 arcpy.AddMessage("Successfully clipped: " + mosaic + " to " + outWorkspace)
	 arcpy.Delete_management("selectlayer")
	 elapsed = (time.clock() - start)
	 arcpy.AddMessage("Execution time: " + str(elapsed / 60)[:4] + " minutes.")
	 #row = cursor.next() #activate this line to skip every other row and start at 1 for processing on two machines
	 