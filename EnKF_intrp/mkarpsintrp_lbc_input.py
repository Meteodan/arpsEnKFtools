#!/usr/bin/env python
#

# This script parses all the ARPS history dumps in a user-specified
# directory and produces arpsintrp.input files for each of them.
# RLT 20110912

### USER SPECIFICATIONS ###
# Absolute path to directory containing ARPS history files
HDFDir = "/nsftor/rtanamachi/cases/26may2010/arps/realdata/from_sooner/3km_KCYS_KPUX/3km_enkf/ena/"
# Absolute path to the arpsintrp.input template file
template = "/nsftor/rtanamachi/cases/26may2010/arps/realdata/1km_enkf/input/arpsintrp_lbc.input.template"
# Absolute path to where the resulting radremap_88D.input files should be stored.
rinPath = "/nsftor/rtanamachi/cases/26may2010/arps/realdata/1km_enkf/input/arpsintrp_lbc_input"
# Name of the experiment (used as a prefix for the output):
expPrefix = "1km26may2010"
### END OF USER SPECIFICATIONS ###

import os, glob

# Generate a list of all the files.
HDFFiles = glob.glob(HDFDir+"/*")

for h in HDFFiles:
    # Read in the "template" version of arpsintrp.input which contains your
    # changes. (The default version is in $arpsroot/input.)
    tin = open(template,"r")
    tlines = tin.readlines()
    tin.close()

    # Debug file name parsing
    print h
    theExpName = h[-6:]
    print "theExpName = ", theExpName
    thePrefix = h[-6:-3]
    theSuffix = h[-3:]
    # Modify the lines for radar name and input file
    for i in range(len(tlines)):
        if(tlines[i].find("hdmpfheader =") > 0):
            tlines[i] = tlines[i].replace("ena001",theExpName)
        if(tlines[i].find("grdbasfn =") > 0):
            tlines[i] = tlines[i].replace("ena001",theExpName)
        if(tlines[i].find("hisfile(1) =") > 0):
            tlines[i] = tlines[i].replace("ena001",theExpName)
	if(tlines[i].find("name_grd(1) =") > 0):
            tlines[i] = tlines[i].replace("001",theSuffix)

    # Write out modified arpsinterp.input file
    fout = open(rinPath+"/arpintrp_lbc."+theExpName+".input","w")
    fout.writelines(tlines)
    fout.flush()
    fout.close()
