#Modified DSLR cameras often replace the Blue band in the RGB capture with
#Infrared. Generally, false color infrared is rendered as Infrared-Red-Green.
#This Arcpy script reorders the bands to create a proper CIR image.
#Turn Red, Green, Infrared into Infrared, Red, Green

import arcpy
import os
import time
import shutil

# Specify the input workspace
inPath = arcpy.GetParameterAsText(0)

# Specify the output workspace
outPath = arcpy.GetParameterAsText(1)

arcpy.env.compression = 'NONE'
arcpy.env.pyramid = 'NONE'


def makePath(root, new):
	if not os.path.exists(os.path.join(root,new)):
		os.makedirs(os.path.join(root,new))

def makeCIR(inWS, outWS):
	try:
		makePath(outWS,"temp")
		arcpy.env.workspace = inWS
		rasters = arcpy.ListRasters("","")
		rastCount = len(rasters)
		arcpy.AddMessage("Converting " + str(rastCount) + " images to CIR.")
		i = 1
		for raster in rasters:
			arcpy.AddMessage("Reconfiguring file " + str(i) + " of " + str(rastCount) + ": " + raster)
			start = time.clock()
			redIn = raster + "\Band_1"
			red = os.path.join(outWS, "temp", raster[:-4] + "_red.tif")
			arcpy.CopyRaster_management(redIn,red)
			greenIn = raster + "\Band_2"
			green = os.path.join(outWS, "temp", raster[:-4] + "_green.tif")
			arcpy.CopyRaster_management(greenIn,green)
			irIn = raster + "\Band_3"
			ir = os.path.join(outWS, "temp", raster[:-4] + "_ir.tif")
			arcpy.CopyRaster_management(irIn,ir)
			
			outRaster = raster[:-4] + ".tif"
			arcpy.CompositeBands_management('"' + ir + ";" + red + ";" + green + '"', os.path.join(outWS, os.path.basename(raster[:-4]+".tif")))
			
			os.remove(os.path.join(outWS,raster[:-4] + ".tfw"))
			os.remove(os.path.join(outWS,raster[:-4] + ".tif.aux.xml"))
			os.remove(os.path.join(outWS,raster[:-4] + ".tif.xml"))
			
			arcpy.AddMessage("Successfully reconfigured: " + raster + " to " + outWS)
			elapsed = (time.clock() - start)
			arcpy.AddMessage("Execution time: " + str(elapsed / 60)[:4] + " minutes.")
			i += 1
			print arcpy.GetMessage(0)
	
	except Exception as e:
		arcpy.AddMessage("Reconfiguration attempt failed.")
		arcpy.AddError(e.message)

makeCIR(inPath, outPath)

try:
	shutil.rmtree(os.path.join(outPath, "temp"))
except Exception as e:
	arcpy.AddError(e.message)
	arcpy.AddMessage("Temporary file deletion failed. Please delete temporary files from" + os.path.join(outPath, "temp"))