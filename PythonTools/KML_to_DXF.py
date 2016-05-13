import arcpy
import os

# KML TO DXF
# For vector KMLs only

inKML = arcpy.GetParameterAsText(0)
outLocation = arcpy.GetParameterAsText(1)

arcpy.env.overwriteOutput = True

#arcpy.ExportCAD_conversion(os.path.join(outLocation, os.path.basename(inKML)[:-4] + ".lyr"), 'DXF_R2013',os.path.join(outLocation,os.path.basename(inKML)[:-4] + ".dxf"))
if outLocation == r"~\Desktop":
	outLocation = os.path.expanduser("~\Desktop")
	arcpy.AddMessage("Output Location: " + str(outLocation))
	arcpy.env.workspace = os.path.expanduser("~\Desktop")
else:
	arcpy.env.workspace = outLocation
	arcpy.AddMessage("Output Location: " + str(outLocation))
	
newLayer = arcpy.KMLToLayer_conversion(inKML, outLocation)

fgdbs = arcpy.ListWorkspaces(os.path.basename(inKML)[:-4] + '*', 'FileGDB')
arcpy.AddMessage("Workspaces: " + str(fgdbs))

if os.path.exists(os.path.join(outLocation, os.path.basename(inKML)[:-4] + ".dxf")):
	os.remove(os.path.join(outLocation, os.path.basename(inKML)[:-4] + ".dxf"))
	try:
		os.remove(os.path.join(outLocation, os.path.basename(inKML)[:-4] + ".dxf.xml"))
	except:
		pass

for fgdb in fgdbs:
	arcpy.env.workspace = fgdb
	for dataset in arcpy.ListDatasets():
		featureClasses = arcpy.ListFeatureClasses('','',dataset)
		arcpy.AddMessage(str(featureClasses))
		for fc in featureClasses:
			arcpy.ExportCAD_conversion(fc, 'DXF_R2013',os.path.join(outLocation, os.path.basename(inKML)[:-4] + ".dxf"), 'IGNORE_FILENAMES_IN_TABLES', 'APPEND_TO_EXISTING_FILES')
	#TO DO: Make these things work. ArcGIS locks up everything it touches, like some kind of masochistic judge
	#arcpy.Delete_management(fgdb)
#del featureClasses, fgdbs, fgdb, newLayer, fc
