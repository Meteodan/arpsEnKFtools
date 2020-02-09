"""
This script runs ext2arps for a given experiment configuration. It takes one command-line argument,
the (python) configuration file for that experiment, from which it imports the appropriate info
"""

import os
import sys
import subprocess
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

# Set the path to the ext2arps.input namelist template file
ext2arps_input_template_path = os.path.join(config.template_exp_dir, 'ext2arps.input')

# Create the ext2arps work directory in icbc scratch directory if it doesn't already exist.
ext2arps_work_dir = os.path.join(config.prep_work_dir, 'ext2arps_work')
if not os.path.exists(ext2arps_work_dir):
    os.makedirs(ext2arps_work_dir)
ext2arps_input_t0_exp_path = os.path.join(ext2arps_work_dir,
                                          'ext2arps_{}_t0.input'.format(config.exp_name))
ext2arps_output_t0_exp_path = os.path.join(ext2arps_work_dir,
                                           'ext2arps_{}_t0.output'.format(config.exp_name))
ext2arps_input_lbc_exp_path = os.path.join(ext2arps_work_dir,
                                           'ext2arps_{}_lbc.input'.format(config.exp_name))
ext2arps_output_lbc_exp_path = os.path.join(ext2arps_work_dir,
                                            'ext2arps_{}_lbc.output'.format(config.exp_name))

# Copy the ext2arps namelist template file to the working directory
# shutil.copy(ext2arps_input_template_path, ext2arps_work_dir)

# Edit the namelist files
ext2arps_param = config.ext2arps_param.copy()
# Pop the t0 and lbc run flags from the dictionary
run_t0 = ext2arps_param.pop('run_t0', True)
run_lbc = ext2arps_param.pop('run_lbc', True)
extdtimes = ext2arps_param.pop('extdtimes')
# Now loop through the times in the "extdtimes" list from the master_config.py and create
# the appropriate key-value pairs for passing to the editNamelistFile function below

for i in range(1, ext2arps_param['nextdfil'] + 1):
    ext2arps_param['extdtime({:d})'.format(i)] = extdtimes[i-1]

# Additional parameters for initial condition (t0) run

if run_t0:
    extdfile_t0_args = ext2arps_param.copy()
    new_args = {
        'hdmpopt': 1,
        'exbcdmp': 0,
        'nextdfil': 1
    }
    extdfile_t0_args.update(new_args)

    # Create namelist file for t0 run
    editNamelistFile(ext2arps_input_template_path,
                     ext2arps_input_t0_exp_path,
                     runname=config.exp_name,
                     **config.grid_param,
                     **extdfile_t0_args)

# Additional parameters for lateral boundary condition (lbc) run

if run_lbc:
    extdfile_lbc_args = ext2arps_param.copy()
    new_args = {
        'hdmpfmt': 0
    }
    extdfile_lbc_args.update(new_args)
    # Create namelist file for lbc run
    editNamelistFile(ext2arps_input_template_path,
                     ext2arps_input_lbc_exp_path,
                     runname=config.exp_name,
                     **config.grid_param,
                     **extdfile_lbc_args)
# # Run ext2arps

# Make sure the target output directory exists
if not os.path.exists(ext2arps_param['dirname']):
    os.makedirs(ext2arps_param['dirname'])

if run_t0:
    with open(ext2arps_input_t0_exp_path, 'r') as input_file, \
            open(ext2arps_output_t0_exp_path, 'w') as output_file:
        print("Running {} for {}".format(config.ext2arps_exe_path, ext2arps_input_t0_exp_path))
        subprocess.call(config.ext2arps_exe_path, stdin=input_file, stdout=output_file, shell=True)

if run_lbc:
    with open(ext2arps_input_lbc_exp_path, 'r') as input_file, \
            open(ext2arps_output_lbc_exp_path, 'w') as output_file:
        print("Running {} for {}".format(config.ext2arps_exe_path, ext2arps_input_lbc_exp_path))
        subprocess.call(config.ext2arps_exe_path, stdin=input_file, stdout=output_file, shell=True)
