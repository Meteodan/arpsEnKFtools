#!/usr/bin/env python2.7
## This script takes a generates soft links to radar files given a user defined time and interval.
## RLT 20110606

import os, glob
import datetime as D
import numpy as N

# From https://stackoverflow.com/questions/10688006/generate-a-list-of-datetimes-between-an-interval
def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

### USER SPECIFICATIONS ###
# Absolute path to directory where gridtilt files reside.
basedir = "/depot/dawson29/data/VORTEXSE/simulations/ARPS/2016_IOP3/processed_radar/"
radnames = ['KBMX', 'KGWX', 'KHPX', 'KHTX', 'KNQA', 'KOHX', 'KPAH']
startTime = D.datetime(2016,03,31,18,00,00)
endTime = D.datetime(2016,04,01,03,00,00)
# Time interval as a timedelta object
# Note that the constructor has the form timedelta(days, seconds, microseconds).
# e.g., 5 min could be given as timedelta(0,300).
# See http://docs.python.org/library/datetime.html
interval = D.timedelta(0,300)
# Turn this flag on to print out some extra output for debugging
debug = 0
### END OF USER SPECIFICATIONS ###

# Generate a list of datetime objects corresponding to the desired times.
timeList = list(perdelta(startTime, endTime+interval, interval))
# timeList = [];
# timeIter = startTime
# while timeIter <= endTime:
#     timeList.append(timeIter)
#     timeIter = timeIter + interval;
# timeList = N.array(timeList)
if debug:
    print timeList

# Outer loop through radars
for radname in radnames:
    inDir = os.path.join(basedir, radname+"_153x153/")

    # Generate a list of times corresponding to files in the directory.
    gtFile = glob.glob(inDir+"/"+radname+".*")

    # Get rid of softlinks (TODO: may just want to ignore the soft links)
    for i in xrange(len(gtFile)):
        if os.path.islink(gtFile[i]):
            os.unlink(gtFile[i])

    gtFile = glob.glob(inDir+"/"+radname+".*")

    timeFile = []
    if debug:
        print gtFile
    for i in range(len(gtFile)):
        gtFilename = os.path.split(gtFile[i])[1]
        if debug:
            print i, gtFile[i],gtFilename
        timeFile.append(D.datetime(int(gtFilename[5:9]),int(gtFilename[9:11]),
                        int(gtFilename[11:13]),int(gtFilename[14:16]),int(gtFilename[16:18]),int(gtFilename[18:20])))
    #     timeFile.append(D.datetime(int("2"+gtFile[i][-14:-11]),int(gtFile[i][-11:-9]),int(gtFile[i][-9:-7]),
    #                                int(gtFile[i][-6:-4]),int(gtFile[i][-4:-2]),int(gtFile[i][-2:])))

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
        gtFilename = os.path.split(gtFile[tind])[1]
        if debug:
            print tind
            print gtFilename
        # Now, link the closest file with the desired time
        #cmd = "ln -sf " + gtFile[tind][-20:] + " " +  gtFile[tind][-20:-15] + t.strftime("%Y%m%d.%H%M%S")
        #cmd = "ln -sf " + inDir + gtFile[tind][-20:] + " " +  gtFile[tind][-20:-15] + t.strftime("%Y%m%d.%H%M%S")
        cmd = "ln -sf " + gtFile[tind] + " " + os.path.join(basedir, gtFilename[:4] + "." + t.strftime("%Y%m%d.%H%M%S"))
        #cmd = "rm " + gtFilename[:4] + "." + t.strftime("%Y%m%d.%H%M%S")
        print cmd
        os.system(cmd)
