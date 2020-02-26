#!/usr/bin/env python2.7
## This script takes a generates soft links to radar files given a user defined time and interval.
## RLT 20110606

import os, glob
import datetime as D
import numpy as N

### USER SPECIFICATIONS ###
# Absolute path to directory where gridtilt files reside.
inDir = "/nsftor/rtanamachi/cases/26may2010/arps/realdata/250m_enkf/radout/UMWB/gridtilt.v1.20120829.arpscvs/"
startTime = D.datetime(2010,05,26,22,27,00)
endTime = D.datetime(2010,05,26,23,25,00)
# Time interval as a timedelta object
# Note that the constructor has the form timedelta(days, seconds, microseconds).
# e.g., 5 min could be given as timedelta(0,300).
# See http://docs.python.org/library/datetime.html
interval = D.timedelta(0,180)
# Turn this flag on to print out some extra output for debugging
debug = 1
### END OF USER SPECIFICATIONS ###

# Generate a list of datetime objects corresponding to the desired times.
timeList = [];
timeIter = startTime
while timeIter <= endTime:
    timeList.append(timeIter)
    timeIter = timeIter + interval;
timeList = N.array(timeList)
if debug:
    print timeList

# Generate a list of times corresponding to files in the directory.
gtFile = glob.glob(inDir+"/UMWB.*")
timeFile = [];
if debug:
    print gtFile
for i in range(len(gtFile)):
    if debug:
        print i, gtFile[i]
    timeFile.append(D.datetime(int("2"+gtFile[i][-14:-11]),int(gtFile[i][-11:-9]),int(gtFile[i][-9:-7]),
                               int(gtFile[i][-6:-4]),int(gtFile[i][-4:-2]),int(gtFile[i][-2:])))

timeFile = N.array(timeFile)
if debug:
    print timeFile

# Find the closest file time to each cycle time
if debug:
    print "Generating soft links"
for t in timeList:
    # Calculate difference between desired time and file times
    temp = abs(timeFile - t)
    # Find index where this difference is minimized.
    tind = N.min(N.nonzero(temp==N.min(temp))).squeeze()
    if debug:
        print tind
    # Now, link the closest file with the desired time
    #cmd = "ln -sf " + gtFile[tind][-20:] + " " +  gtFile[tind][-20:-15] + t.strftime("%Y%m%d.%H%M%S")
    cmd = "ln -sf " + inDir + gtFile[tind][-20:] + " " +  gtFile[tind][-20:-15] + t.strftime("%Y%m%d.%H%M%S")
    print cmd
    os.system(cmd)​
