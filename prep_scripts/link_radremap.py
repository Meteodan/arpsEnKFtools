# This script takes a generates soft links to radar files given a user defined time and interval.
# RLT 20110606

import os
import sys
import glob
from datetime import datetime, timedelta
import numpy as np
from arpsenkftools.io_utils import import_all_from


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

# Turn this flag on to print out some extra output for debugging
debug = 0

# Generate a list of datetime objects corresponding to the desired times.
start_datetime = datetime.strptime(config.radremap_param['start_timestamp'], '%Y%m%d%H%M%S')
end_datetime = datetime.strptime(config.radremap_param['end_timestamp'], '%Y%m%d%H%M%S')
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

radar_list = config.radremap_param.pop('radar_list')
print(radar_list)
print(config.remapped_radar_dir)

# Outer loop through radars
for radname in radar_list:
    # Get list of remapped radar files
    remapped_file_paths = glob.glob(config.remapped_radar_dir + '/{}.*.*'.format(radname))
    remapped_file_names = [os.path.basename(remapped_file_path) for remapped_file_path in
                           remapped_file_paths]
    # Extract the time stamps from the file names
    file_times = [remapped_file_name.replace('{}.'.format(radname), '') for remapped_file_name in
                  remapped_file_names]
    # Create datetime objects out of the timestamps
    file_datetimes = [datetime.strptime(file_time, '%Y%m%d.%H%M%S') for file_time in file_times]

    # For each time in the desired range, find the closest matching remapped file and create the
    # link

    for t in timeList:
        diff = np.array([np.abs((file_dt - t).total_seconds()) for file_dt in file_datetimes])
        closest = diff.min()
        # Only do the linking if the time difference is greater than zero and less than the
        # desired tolerance (if the difference is zero, then just use the file itself,
        # silly)
        if closest <= config.radremap_param['tolerance'] and closest > 0:
            closest_index = diff.argmin()
            closest_file_path = remapped_file_paths[closest_index]
            print(t, closest_file_path)
            link_name = t.strftime('{}.%Y%m%d.%H%M%S'.format(radname))
            link_path = os.path.join(config.remapped_radar_dir, link_name)
            # Remove existing link
            if os.path.lexists(link_path):
                os.remove(link_path)
            os.symlink(remapped_file_paths[closest_index], link_path)
        elif closest > config.radremap_param['tolerance']:
            print('For time ', t)
            print('No time within tolerance ({:d} s)'.format(config.radremap_param['tolerance']))
            print('Closest is {:d} s'.format(int(closest)))
