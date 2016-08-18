import arcpy
import os
import time
import shutil

# Specify the input workspaces
RGBI_path = arcpy.GetParameterAsText(0)
RGB_outpath = arcpy.GetParameterAsText(1)
CIR_outpath = arcpy.GetParameterAsText(2)

arcpy.env.compression = 'NONE'


def makePath(root, new):
	if not os.path.exists(os.path.join(root,new)):
		os.makedirs(os.path.join(root,new))

def doRGBI(RGBI_path, RGB_outpath, CIR_outpath):
	outWorkspace = RGB_outpath
	
	try:
		makePath(RGB_outpath, "temp")
		arcpy.env.workspace = RGBI_path
		RGBIrasters = arcpy.ListRasters("", "TIF")
		rastCount = len(RGBIrasters)
		arcpy.AddMessage("Reconfiguring " + str(rastCount) + " rasters.")
		current = 1
		for RGBIraster in RGBIrasters:
			arcpy.env.workspace = RGBI_path
			# Get Bands for RGBI
			redin = RGBIraster + "\Band_1"
			red = os.path.join(RGB_outpath, "temp", RGBIraster[:-4] + "_red.tif")
			arcpy.CopyRaster_management(redin,red)
			greenin = RGBIraster + "\Band_2"
			green= os.path.join(RGB_outpath, "temp", RGBIraster[:-4] + "_green.tif")
			arcpy.CopyRaster_management(greenin,green)
			bluein = RGBIraster + "\Band_3"
			blue = os.path.join(RGB_outpath, "temp", RGBIraster[:-4] + "_blue.tif")
			arcpy.CopyRaster_management(bluein,blue)
			IRin = RGBIraster + "\Band_4"
			IR = os.path.join(RGB_outpath, "temp", RGBIraster[:-4] + "_ir.tif")
			arcpy.CopyRaster_management(IRin,IR)
			
			outRaster = RGBIraster[:-4] + ".tif"
			start = time.clock()
			arcpy.AddMessage("Reconfiguring file " + str(current) + " of " + str(rastCount) + ": " + RGBIraster)
			
			arcpy.CompositeBands_management('"' + red + ";" + green + ";" + blue + '"', os.path.join(RGB_outpath, os.path.basename(RGBIraster[:-4]+".tif")))
			arcpy.AddMessage("Successfully reconfigured: " + RGBIraster + " to " + RGB_outpath)
			arcpy.CompositeBands_management('"' + IR + ";" + red + ";" + green + '"', os.path.join(CIR_outpath, os.path.basename(RGBIraster[:-4]+".tif")))
			elapsed = (time.clock() - start)
			arcpy.AddMessage("Execution time: " + str(elapsed / 60)[:4] + " minutes.")
			current = current + 1
			print arcpy.GetMessage(0)
	except Exception as e:
		arcpy.AddMessage("Reconfiguration attempt failed.")
		arcpy.AddError(e.message)
	
doRGBI(RGBI_path, RGB_outpath, CIR_outpath)

try:
	shutil.rmtree(os.path.join(RGB_outpath, "temp"))
except Exception as e:
	arcpy.AddError(e.message)
	arcpy.AddMessage("Temporary file deletion failed. Please delete temporary files manually")