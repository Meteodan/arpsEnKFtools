#!/usr/bin/env python2.7
## This script takes a generates soft links to radar files given a user defined time and interval.
## RLT 20110606

import os, glob
from datetime import datetime, timedelta
import numpy as np

# From https://stackoverflow.com/questions/10688006/generate-a-list-of-datetimes-between-an-interval
def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

# import the experiment configuration file given by the first command-line argument
if len(sys.argv) > 1:   # Try to import user-defined config file
    config_file = sys.argv[1]
    print("Config file is " + config_file)
    try:
        config = import_all_from(config_file)
        print("Successfully imported experiment configuration.")
    except Exception:
        print("Unable to import experiment configuration. Exiting!")
else:
    print("Please provide an experiment configuration file on the command line! Exiting!")



### USER SPECIFICATIONS ###
# Absolute path to directory where gridtilt files reside.
basedir = "/depot/dawson29/data/users/sharm261/processed_radar/"
radnames = ['KTLX']
startTime = D.datetime(2013, 5, 19, 20, 00, 00)
endTime = D.datetime(2013, 5, 19, 23, 00, 00)
# Time interval as a timedelta object
# Note that the constructor has the form timedelta(days, seconds, microseconds).
# e.g., 5 min could be given as timedelta(0,300).
# See http://docs.python.org/library/datetime.html
interval = D.timedelta(0, 300)
# Turn this flag on to print out some extra output for debugging
debug = 0
### END OF USER SPECIFICATIONS ###

# Generate a list of datetime objects corresponding to the desired times.
start_datetime = datetime.strptime(config.radremap_param['start_timestamp'], '%Y%m%d%H%M')
end_datetime = datetime.strptime(config.radremap_param['end_timestamp'], '%Y%m%d%H%M')
interval = timedelta(seconds=config.radremap_param['interval_seconds'])
timeList = list(perdelta(start_datetime, end_datetime + interval, interval))
# timeList = [];
# timeIter = startTime
# while timeIter <= endTime:
#     timeList.append(timeIter)
#     timeIter = timeIter + interval;
# timeList = N.array(timeList)
if debug:
    print(timeList)

# STOPPED HERE!

# Outer loop through radars
for radname in config.radremap_param['radar_list']:
    inDir = os.path.join(basedir, radname+"_153x153/")

    # Generate a list of times corresponding to files in the directory.
    gtFile = glob.glob(inDir+"/"+radname+".*")

    # Get rid of softlinks (TODO: may just want to ignore the soft links)
    for i in range(len(gtFile)):
        if os.path.islink(gtFile[i]):
            os.unlink(gtFile[i])

    gtFile = glob.glob(inDir+"/"+radname+".*")

    timeFile = []
    if debug:
        print(gtFile)
    for i in range(len(gtFile)):
        gtFilename = os.path.split(gtFile[i])[1]
        if debug:
            print(i, gtFile[i],gtFilename)
        timeFile.append(D.datetime(int(gtFilename[5:9]),int(gtFilename[9:11]),
                        int(gtFilename[11:13]),int(gtFilename[14:16]),int(gtFilename[16:18]),int(gtFilename[18:20])))
    #     timeFile.append(D.datetime(int("2"+gtFile[i][-14:-11]),int(gtFile[i][-11:-9]),int(gtFile[i][-9:-7]),
    #                                int(gtFile[i][-6:-4]),int(gtFile[i][-4:-2]),int(gtFile[i][-2:])))

    timeFile = N.array(timeFile)
    if debug:
        print(timeFile)

    # Find the closest file time to each cycle time
    if debug:
        print("Generating soft links")
    for t in timeList:
        # Calculate difference between desired time and file times
        temp = abs(timeFile - t)
        # Find index where this difference is minimized.
        tind = N.min(N.nonzero(temp==N.min(temp))).squeeze()
        gtFilename = os.path.split(gtFile[tind])[1]
        if debug:
            print(tind)
            print(gtFilename)
        # Now, link the closest file with the desired time
        #cmd = "ln -sf " + gtFile[tind][-20:] + " " +  gtFile[tind][-20:-15] + t.strftime("%Y%m%d.%H%M%S")
        #cmd = "ln -sf " + inDir + gtFile[tind][-20:] + " " +  gtFile[tind][-20:-15] + t.strftime("%Y%m%d.%H%M%S")
        cmd = "ln -sf " + gtFile[tind] + " " + os.path.join(basedir, gtFilename[:4] + "." + t.strftime("%Y%m%d.%H%M%S"))
        #cmd = "rm " + gtFilename[:4] + "." + t.strftime("%Y%m%d.%H%M%S")
        print(cmd)
        os.system(cmd)
