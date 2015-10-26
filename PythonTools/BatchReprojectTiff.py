# Description: This script is used to batch reproject TIFF images to a user-specified
#              coordinate system while preserving the bit depth of the original image.
#              The delivered TIFF will have the selected projection.

import arcpy
import os
import time

# Specify the input workspace
arcpy.env.workspace = arcpy.GetParameterAsText(0)

# Specify the output workspace
outWorkspace = arcpy.GetParameterAsText(1)

# Set compression type and level
arcpy.env.compression = 'NONE'

# Set Output Coordinate System
arcpy.env.outputCoordinateSystem = arcpy.GetParameterAsText(2)
outCoor = arcpy.env.outputCoordinateSystem


try:
	rasters = arcpy.ListRasters("", "TIF")
	rastCount = len(rasters)
	arcpy.AddMessage("Reprojecting " + str(rastCount) + " rasters to " + outWorkspace)
	current = 1
	for raster in rasters:
		 outRaster = raster[:-4] + ".tif"
		 start = time.clock()
		 arcpy.AddMessage("Reprojecting file " + str(current) + " of " + str(rastCount) + ": " + raster)
		 arcpy.ProjectRaster_management(raster, os.path.join(outWorkspace, outRaster), outCoor)
		 arcpy.AddMessage("Successfully reprojected: " + raster + " to " + outWorkspace)
		 elapsed = (time.clock() - start)
		 arcpy.AddMessage("Execution time: " + str(elapsed / 60)[:4] + " minutes.")
		 current = current + 1
		 print arcpy.GetMessage(0)
except Exception as e:
	arcpy.AddMessage("Reproject attempt failed.")
	arcpy.AddError(e.message)