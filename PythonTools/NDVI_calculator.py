#Calculate NDVI from 4-band imagery

import arcpy, string, os

from arcpy import env
from arcpy.sa import *

#Check out the Spatial Analyst extension
arcpy.CheckOutExtension("spatial")

#Input workspace
env.workspace = arcpy.GetParameterAsText(0)

#Output workspace
outworkspace = arcpy.GetParameterAsText(1)

if not os.path.exists(os.path.join(outworkspace,"temp")):
	os.makedirs(os.path.join(outworkspace, "temp"))

try:
	rasters = arcpy.ListRasters("", "TIF")
	for raster in rasters:
		#set the input raster
		input = raster
		#Create raster directory and specify inputs
		result = "NDVI_" + raster
		NIR = input + "\Band_4"
		Red = input + "\Band_1"
		
		#Define outputs – Note:  These will need to be deleted if you need to run this script again
		NIR_out = os.path.join(outworkspace, "temp", raster +"_NIR.tif")
		Red_out = os.path.join(outworkspace, "temp", raster +"_Red.tif")

		#Copy raster and map algebra – makes new rasters of Red and NearIR
		arcpy.CopyRaster_management(NIR, NIR_out)
		arcpy.AddMessage("Copied NIR band as raster")
		arcpy.CopyRaster_management(Red, Red_out)
		arcpy.AddMessage("Copied Red band as raster")

		#Create Numerator and Denominator rasters as variables and NDVI output (note that arcpy.sa.Float returns a floating point raster)
		try:
			Numer = Float(Raster(NIR_out)) - Float(Raster(Red_out))
			Denom = Float(Raster(NIR_out)) + Float(Raster(Red_out))
			NIR_eq = arcpy.sa.Divide(Numer, Denom)
			arcpy.AddMessage("Dividing")
		except Exception as e:
			arcpy.AddMessage("wtf")
			arcpy.AddError(e)
		#Saving output to result output you specified above
		NIR_eq.save(result)
		arcpy.AddMessage("Successful")
except Exception as e:
    arcpy.AddMessage("NDVI calculation attempt failed.")
    arcpy.AddError(e)