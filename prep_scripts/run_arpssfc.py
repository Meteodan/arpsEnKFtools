"""
This script runs arpssfc for a given experiment configuration. It takes one command-line argument,
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

# Set the path to the arpssfc.input namelist template file
arpssfc_input_template_path = os.path.join(config.template_exp_dir, 'arpssfc.input')

# Create the arpssfc work directory in icbc scratch directory if it doesn't already exist.
arpssfc_work_dir = os.path.join(config.prep_work_dir, 'arpssfc_work')
if not os.path.exists(arpssfc_work_dir):
    os.makedirs(arpssfc_work_dir)
arpssfc_input_exp_path = os.path.join(arpssfc_work_dir,
                                      'arpssfc_{}.input'.format(config.exp_name))
arpssfc_output_exp_path = os.path.join(arpssfc_work_dir,
                                       'arpssfc_{}.output'.format(config.exp_name))

# Copy the arpssfc namelist template file to the working directory
# shutil.copy(arpssfc_input_template_path, arpssfc_work_dir)

# Edit the namelist file
editNamelistFile(arpssfc_input_template_path,
                 arpssfc_input_exp_path,
                 runname=config.exp_name,
                 **config.grid_param,
                 **config.arpssfc_param)

# Create the output directory if it doesn't already exist
if not os.path.exists(config.sfcdata_dir):
    os.makedirs(config.sfcdata_dir)

# Run arpssfc
with open(arpssfc_input_exp_path, 'r') as input_file, \
     open(arpssfc_output_exp_path, 'w') as output_file:
    print("Running {} for {}".format(config.arpssfc_exe_path, arpssfc_input_exp_path))
    subprocess.call(config.arpssfc_exe_path, stdin=input_file, stdout=output_file, shell=True)
