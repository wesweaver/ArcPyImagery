# Description: This script is used to batch clip TIFF images to a user-specified polygon
#              while preserving the bit depth of the original image.
#              The delivered TIFF will have no compression.
#
# Environment: ArcGIS
# Written by: Wes Weaver
# Date: December 20, 2013
# Changelog: 12/23/13 (added elapsed time)
#			1/8/14 (added output Coordinate System)

import arcpy
import os
import time

# Specify the input workspace
arcpy.env.workspace = arcpy.GetParameterAsText(0)

# Specify the clip feature
clipShape = arcpy.GetParameterAsText(1)

# Specify the output workspace
outWorkspace = arcpy.GetParameterAsText(2)

# Set compression type and level
arcpy.env.compression = 'NONE'

# Set Output Coordinate System
arcpy.env.outputCoordinateSystem = arcpy.GetParameterAsText(3)


try:
	rasters = arcpy.ListRasters("", "TIF")
	rastCount = len(rasters)
	arcpy.AddMessage("Clipping " + str(rastCount) + " rasters to " + os.path.basename(clipShape))
	current = 1
	for raster in rasters:
		 outRaster = raster[:-4] + ".tif"
		 start = time.clock()
		 arcpy.AddMessage("Clipping file " + str(current) + " of " + str(rastCount) + ": " + raster + " to " + os.path.basename(clipShape))
		 arcpy.Clip_management(raster, "#", os.path.join(outWorkspace, outRaster), clipShape, "0", "ClippingGeometry")
		 arcpy.AddMessage("Successfully clipped: " + raster + " to " + outWorkspace)
		 elapsed = (time.clock() - start)
		 arcpy.AddMessage("Execution time: " + str(elapsed / 60)[:4] + " minutes.")
		 current = current + 1
		 print arcpy.GetMessage(0)
except Exception as e:
	arcpy.AddMessage("Clip attempt failed.")
	arcpy.AddError(e.message)