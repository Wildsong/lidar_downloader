# -*- coding: utf-8 -*-
#
#   Walk through the folders in the "base" folder
#   and check for tile index shapefiles
#   Build new feature classes that have only tiles in our county.
#   Download the tiles
#
import os
from glob import glob
import arcpy
from util import download_file

def select_tiles(boundary_fc):
    """ Use the county boundary to create feature classes that contain only the interesting tiles. """
    l = []

    for folder in glob('*'):
        if os.path.isdir(folder):
            for pathname in glob(os.path.join(folder, "*.shp")):
                [path,filename] = os.path.split(pathname)
                [name,ext] = os.path.splitext(filename)
                selection_layer = name
                try:
                    arcpy.management.MakeFeatureLayer(pathname, selection_layer)
                except Exception as e:
                    print(e)
                    continue
                selection = arcpy.management.SelectLayerByLocation(
                    selection_layer, "INTERSECT", boundary_fc)

                try:
                    outfc = arcpy.ValidateTableName(selection_layer) # It does not like names that start with a numeral
                    l.append((path, outfc))
                    if not arcpy.Exists(outfc):
                        arcpy.management.CopyFeatures(selection_layer, outfc)
                        print("Wrote to %s" % outfc)
                except Exception as e:
                    print(e)
                    continue
                pass
    return l

if __name__ == '__main__':

    base = "F:/surface"
    os.chdir(base)
    boundary_fc = "K:/ORMAP_CONVERSION/Clatsop_WinAuth.sde/Clatsop.DBO.county_boundary"

    # list of all known urlfields
    urls = ["URL"]

    arcpy.env.overwriteOutput = False
    with arcpy.EnvManager(
            scratchWorkspace=r"F:\surface\contour_builder\contour_builder.gdb", 
            workspace=r"F:\surface\contour_builder\contour_builder.gdb"):

        mylist = select_tiles(boundary_fc)


        # Build a list with every URL in it.
        everything = []

        for (folder,fc) in mylist:
            d = arcpy.Describe(fc)
            urlfield = "" # there is no known url field
            for f in d.fields:
                print(f.name)
                if f.name in urls:
                    urlfield = f.name

            fields = [urlfield]
            cursor = arcpy.da.SearchCursor(fc, fields)
            row = cursor.next()
            while row:
                try:
                    #print(row)
                    url = row[0].strip()
                    #print(url)
                    everything.append((folder, url))
                except Exception as e:
                    print("Something's wrong with %s; error: %s" % (url, e))
                try:
                    row = cursor.next()
                except StopIteration:
                    row = False # I don't know why I need this today
            del row
                    
        # Download everything
        count = 0
        total = len(everything)
        success = 0
        fail = 0
        already_in_stock = 0
        print("Files to download: %d" % total)

        for (folder, url) in everything:
            outputfolder = os.path.join(base, "Lidar", folder)
            parts = url.split('/')
            fname = parts[-1]

            if not os.path.exists(outputfolder):
                os.makedirs(outputfolder)

            os.chdir(outputfolder)
            count += 1

            if os.path.exists(os.path.join(outputfolder,fname)):
                print("Already have \"%s\" / \"%s\"" % folder, fname)
                already_in_stock += 1
                continue

            print("Downloading %d/%d %s.." % (count, total, fname), end="")
            try:
                success += download_file(url, fname)
            except Exception as e:
                print(".. failed, %s" % e)
                fail += 1
            print()

    print("Downloaded %d, failed to download %d, already had %d" % (success, fail, already_in_stock))
    exit(0)
