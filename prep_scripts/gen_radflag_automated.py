"""
This script generates a "radflag" file for use in the EnKF cycle. It reads the "master_config.py"
file from the given experiment template directory.

TODO: make it work for multiple radar DA case
"""
import sys
import pprint
from arpsenkftools.io_utils import import_all_from
import os
import glob
from datetime import datetime, timedelta
import numpy as np
# TODO: comment out this line when actually running the script. This is just to let the python
# linter know about the various parameters in the config file
# from arpsenkftools import master_config_default as config

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

# import configuration from master_config.py file
config = import_all_from(config_file)

radflag_param = config.radflag_param
remapped_rad_dir = config.remapped_radar_dir

initial_time = datetime.strptime(
    config.initial_time, '%Y%m%d%H%M')                              # simulation initial time

# Next, we want to grab names of all the remapped radar files.
# For this, we will only look for those radar files which will be used in DA
# In other words, we will search for remapped radar files with a symlink,
# since only DA ready files will have an associated symlink geenrated through link_radremap.py script
#
# To account for all possible scenarios namely, no radar DA, single radar DA,
# and > 1  radar used in DA, we proceed in the following manner:

if len(config.radremap_param['radar_list']) < 1:
    raise ValueError('Are you trying to assimilate zero radars?')

elif len(config.radremap_param['radar_list']) == 1:
    # single radar DA is easy with no dictionary comprehensions needed
    remapped_files = [file for file in sorted(os.listdir(remapped_rad_dir)) if os.path.isfile(
        os.path.join(remapped_rad_dir, file)) if not file.endswith(".dat") if os.path.islink(glob.glob(remapped_rad_dir + '/' + file)[0]) == True]

    # access the time of each remapped file
    times = [datetime.strptime(f.split('.')[-1], '%H%M%S')
             for f in remapped_files]

    # set the correct year, month, and day
    final_times = [datetime.strptime(f.split('.')[-2] + f.split('.')
                                     [-1], '%Y%m%d%H%M%S') for f in remapped_files]

    # get the times at which radar data is available
    avail_time = [(final-initial_time).total_seconds()
                  for final in final_times]

    # Now generate the 'radar_data_flag' dictionary, where keys are assimilation times and values are
    # the radar groups that are to be assimilated for that time. You can also explicitly list the times
    # then add the radar_data_flag dictionary to the radflag_param dictionary
    # The values take the form {True:[<radar_group>], False:[<radar_group>]}. In practice,
    # the "False" key doesn't seem to be used anywhere in the run_real_data_case.py script.
    # Actually, the radar names in the radar_groups dict aren't being used either, but only the
    # length of the list (to set nrdrused, but we are already setting it above).
    # TODO: Ask Tim S. about this; refactor how this is done.

    radar_data_flag = {}

    # update radar_data_flag dictionary by setting True for the times when radar data is available
    # and False for non-available times
    for radar_group_name, radar_group in radflag_param['radar_groups'].items():
        non_avail_time = {
            element for element in radar_group[1] if element not in avail_time}
        radar_data_flag.update({
            assim_time: {True: radar_group[0], False: []} for assim_time in avail_time
        })
        radar_data_flag.update({
            assim_time: {True: [], False: radar_group[0]} for assim_time in non_avail_time
        })

else:
    # this is the multiple radar for DA scenario
    # we will use dictionary and list comprehensions for easy data manipulation
    radar_list = config.radremap_param['radar_list']
    all_rad_files = [file for file in sorted(os.listdir(remapped_rad_dir)) if os.path.isfile(os.path.join(
        remapped_rad_dir, file)) if not file.endswith(".dat") if os.path.islink(glob.glob(remapped_rad_dir + '/' + file)[0]) == True]

    # multiple key,value pair using dictionary comprehension
    # https://stackoverflow.com/questions/40079792/adding-multiple-key-value-pair-using-dictionary-comprehension
    remapped_files_multi_radars = {
        radar: [f for f in all_rad_files if radar in f] for radar in radar_list
    }

    # access the time of each remapped file for each radar
    times = {
        radar: [datetime.strptime(f.split('.')[-1], '%H%M%S')
                for f in remapped_files_multi_radars[radar]] for radar in radar_list
    }

    # set the correct year, month, and day
    final_times = {
        radar: [datetime.strptime(f.split('.')[-2] + f.split('.')
                                  [-1], '%Y%m%d%H%M%S') for f in remapped_files_multi_radars[radar]] for radar in radar_list
    }

    # get the times at which data is available for each radar
    avail_time = {
        radar: [(final-initial_time).total_seconds() for final in final_times[radar]] for radar in radar_list
    }

    # Now generate the 'radar_data_flag' dictionary, where keys are assimilation times and values are
    # the radar groups that are to be assimilated for that time. You can also explicitly list the times
    # then add the radar_data_flag dictionary to the radflag_param dictionary
    # The values take the form {True:[<radar_group>], False:[<radar_group>]}. In practice,
    # the "False" key doesn't seem to be used anywhere in the run_real_data_case.py script.
    # Actually, the radar names in the radar_groups dict aren't being used either, but only the
    # length of the list (to set nrdrused, but we are already setting it above).
    # TODO: Ask Tim S. about this; refactor how this is done.

    radar_data_flag = {}

    for radar_group_name, radar_group in radflag_param['radar_groups'].items():

        # now, we need to make a list of radars which have data available at a particular time. Those radars will be set to True.
        # Radars not available at this time will be set False
        radar_data_flag.update({
            assim_time: {True: [radar for radar in radar_list if assim_time in avail_time[radar]], False: [radar for radar in radar_list if assim_time not in avail_time[radar]]
                         } for assim_time in radar_group[1]
        })


print(config.radflag_path)

# Finally, write radar_data_flag dictionary to the radflag file
with open(config.radflag_path, 'w') as radflag_output:
    output_text = pprint.pformat(radar_data_flag, indent=4, width=120)
    radflag_output.write('radar_data_flag = {}'.format(output_text))
