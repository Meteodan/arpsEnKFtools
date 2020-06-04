"""
This script runs wrf2arps for a given experiment configuration. It takes one command-line argument,
the (python) configuration file for that experiment, from which it imports the appropriate info.
Based on an older script for arpsintrp from RLT
"""

import os
import sys
import subprocess
from datetime import datetime, timedelta
from arpsenkftools.editNamelist import editNamelistFile
from arpsenkftools.io_utils import import_all_from

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

# Pop the nproc_x, nproc_y from the grid_param dictionary, since we want to use the ones
# in the wrf2arps_param dictionary
config.grid_param.pop('nproc_x')
config.grid_param.pop('nproc_y')

# Set the path to the wrf2arps.input namelist template file
wrf2arps_input_template_path = os.path.join(config.template_exp_dir, 'wrf2arps.input')

# Create the wrf2arps work directory in icbc scratch directory if it doesn't already exist.
wrf2arps_work_dir = os.path.join(config.prep_work_dir, 'wrf2arps_work')
if not os.path.exists(wrf2arps_work_dir):
    os.makedirs(wrf2arps_work_dir)

# Also create the output icbc dir if it doesn't already exist:
if not os.path.exists(config.external_icbc_dir):
    os.makedirs(config.external_icbc_dir)

start_timestamp = config.wrf2arps_param.pop('init_timestamp')
end_timestamp = config.wrf2arps_param.pop('end_timestamp')
start_datetime = datetime.strptime(start_timestamp, '%Y%m%d%H%M')
end_datetime = datetime.strptime(end_timestamp, '%Y%m%d%H%M')
history_interval_sec = config.wrf2arps_param.pop('history_interval_sec')

datetime_range = [start_datetime + timedelta(seconds=x) for x in
                  range(0, (end_datetime-start_datetime).seconds + history_interval_sec,
                        history_interval_sec)]
wrf_timestrings = [d.strftime('%Y-%m-%d_%H:%M:%S') for d in datetime_range]

# ens_member_list = range(1, config.num_ensemble_members + 1)
config.num_ensemble_members = 1
ens_member_list = [29]
subdir_template = config.wrf2arps_param.pop('subdir_template', None)
ens_member_names = ["ena{:03d}".format(m) for m in ens_member_list]

if subdir_template:
    ens_member_dirs = [os.path.join(config.ext_model_data_dir, subdir_template.format(ens_member))
                       for ens_member in ens_member_list]
else:
    ens_member_dirs = [config.ext_model_data_dir] * config.num_ensemble_members

# Create a list of dictionaries to store the input/output file names as well as the wrf
# output file associated with it.
wrf2arps_dict_list = []
for wrf_timestring in wrf_timestrings:
    for ens_member, ens_member_name in zip(ens_member_list, ens_member_names):
        t0_input_file_name = "{}/{}_{}.wrf2arps_t0.input".format(wrf2arps_work_dir, ens_member_name,
                                                                 wrf_timestring)
        t0_output_file_name = "{}/{}_{}.wrf2arps_t0.output".format(wrf2arps_work_dir,
                                                                   ens_member_name,
                                                                   wrf_timestring)
        lbc_input_file_name = "{}/{}_{}.wrf2arps_lbc.input".format(wrf2arps_work_dir,
                                                                   ens_member_name,
                                                                   wrf_timestring)
        lbc_output_file_name = "{}/{}_{}.wrf2arps_lbc.output".format(wrf2arps_work_dir,
                                                                     ens_member_name,
                                                                     wrf_timestring)
        if subdir_template is None:
            wrfout_file_name = "wrfout_d01_{}_{:d}".format(wrf_timestring, ens_member)
        else:
            wrfout_file_name = "wrfout_d01_{}".format(wrf_timestring)
        wrf2arps_dict = dict(t0_input_file_name=t0_input_file_name,
                             t0_output_file_name=t0_output_file_name,
                             lbc_input_file_name=lbc_input_file_name,
                             lbc_output_file_name=lbc_output_file_name,
                             ens_member_name=ens_member_name,
                             ens_member=ens_member,
                             wrfout_file_name=wrfout_file_name,
                             wrf_timestring=wrf_timestring)
        wrf2arps_dict_list.append(wrf2arps_dict)

for i, wrf2arps_dict in enumerate(wrf2arps_dict_list):

    t0_input_file_name = wrf2arps_dict['t0_input_file_name']
    t0_output_file_name = wrf2arps_dict['t0_output_file_name']
    lbc_input_file_name = wrf2arps_dict['lbc_input_file_name']
    lbc_output_file_name = wrf2arps_dict['lbc_output_file_name']
    ens_member_name = wrf2arps_dict['ens_member_name']
    wrf_timestring = wrf2arps_dict['wrf_timestring']
    ens_member = wrf2arps_dict['ens_member']
    dirname = config.wrf2arps_param['dirname']

    # Initial conditions
    editNamelistFile("{}".format(wrf2arps_input_template_path),
                     t0_input_file_name,
                     dir_extd=ens_member_dirs[i],
                     runname=ens_member_name,
                     init_time_str=wrf_timestrings[0],
                     start_time_str=wrf_timestring,
                     end_time_str=wrf_timestring,
                     **config.wrf2arps_param,
                     **config.grid_param)

    # Boundary conditions
#    editNamelistFile("{}".format(wrf2arps_input_template_path),
#                     lbc_input_file_name,
#                     dir_extd=ens_member_dirs[i],
#                     runname=ens_member_name,
#                     init_time_str=wrf_timestrings[0],
#                     start_time_str=wrf_timestring,
#                     end_time_str=wrf_timestring,
#                     hdmpfmt=0,
#                     exbcdmp=3,
#                     **config.wrf2arps_param,
#                     **config.grid_param)

    # If wrfout files are not in separate subdirectories for each ensemble member, we need to make a
    # temporary softlink to the correct wrfout file but removing the ensemble member from the end,
    # because this is what wrf2arps is expecting
    wrfout_file_name = wrf2arps_dict['wrfout_file_name']
    wrfout_file_path = os.path.join(ens_member_dirs[i], wrfout_file_name)
    if subdir_template is None:
        wrfout_file_link_name = "wrfout_d01_{}".format(wrf_timestring)
        wrfout_file_link_path = os.path.join(ens_member_dirs[i], wrfout_file_link_name)
        command = 'ln -sf {} {}'.format(wrfout_file_path, wrfout_file_link_path)
        print("Linking {} to {}".format(wrfout_file_link_path, wrfout_file_path))
        subprocess.call(command, shell=True)
    else:
        wrfout_file_link_name = wrfout_file_name
        wrfout_file_link_path = wrfout_file_path

    if config.wrf2arps_param['run_mpi']:
        wrf2arps_exe_path = config.wrf2arps_exe_path
        command = '{} {} {:d} {}'.format(config.mpi_exe, config.mpi_nproc_flag,
                                         config.wrf2arps_param['nproc_x'] *
                                         config.wrf2arps_param['nproc_y'],
                                         wrf2arps_exe_path)
    else:
        # Get rid of "_mpi" from exe file if it is there
        wrf2arps_exe = os.path.basename(config.wrf2arps_exe_path).replace("_mpi", "")
        wrf2arps_exe_path = os.path.join(os.path.dirname(config.wrf2arps_exe_path), wrf2arps_exe)
        command = '{}'.format(wrf2arps_exe_path)

    with open(t0_input_file_name, 'r') as inputfile, \
            open(t0_output_file_name, 'w') as outputfile:
        print("Running {} for {}".format(wrf2arps_exe_path, t0_input_file_name))
        subprocess.call(command, stdin=inputfile, stdout=outputfile, shell=True)
    # with open(lbc_input_file_name, 'r') as inputfile, \
    #         open(lbc_output_file_name, 'w') as outputfile:
    #     print("Running {} for {}".format(config.wrf2arps_exe_path, lbc_input_file_name))
    #     subprocess.call(command, stdin=inputfile, stdout=outputfile, shell=True)

    # Now remove the softlink if needed
    if subdir_template is None:
        command = 'unlink {}'.format(wrfout_file_link_path)
        subprocess.call(command, shell=True)
