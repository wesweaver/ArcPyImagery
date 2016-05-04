import arcpy, os
from arcpy.sa import *

# Calculate luminance from an RGB digital image. It is highly recommended to obtain some calibrated data values to plug into the K (calibration constant)
# Based on papers that can be found here:
# https://www.framos.com/fileadmin/media/pdf/press-releases/The_usage_of_digital_cameras_as_luminance_meters_EI_2007_6502_29.pdf
# http://www.ee.ryerson.ca/~phiscock/astronomy/light-pollution/luminance-notes-2.pdf

#Specify inputs
raster = arcpy.GetParameterAsText(0)
outWorkspace = arcpy.GetParameterAsText(1)
red = raster + "\Band_1"
green = raster + "\Band_2"
blue = raster + "\Band_3"

#calculate statistics
arcpy.CalculateStatistics_management(raster)

#Define output bands
redband = os.path.join(outWorkspace, "redband.tif")
greenband = os.path.join(outWorkspace, "greenband.tif")
blueband = os.path.join(outWorkspace, "blueband.tif")

#Split bands to individual rasters
arcpy.CopyRaster_management(red, redband)
arcpy.CopyRaster_management(green, greenband)
arcpy.CopyRaster_management(blue, blueband)

#Define ouput tiff
result = "LumenGrid.tif"

#Do the math and save luminosity grid
Equation = (Float(Raster(redband)) * 0.2163) + (Float(Raster(greenband)) * 0.7152) + (Float(Raster(blueband)) * 0.0722)

#Do rest of math – this won’t work right until you plug in calibration data
# f (aperture/F-stop), t (shutter time in seconds), S (ISO), and K (calibration constant)
f = 5.6
t = 0.015625
S = 200
K = 50.425714286

Final = Divide((Float(Equation) * (f * f)), (t * S * K))
Final.save(os.path.join(outWorkspace, result))
