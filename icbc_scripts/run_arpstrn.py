"""
This script runs arpstrn for a given experiment configuration. It takes one command-line argument,
the (python) configuration file for that experiment, from which it imports the appropriate info
"""

import os
import sys
import shutil
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

# Set the path to the arpstrn.input namelist template file
arpstrn_input_template_path = os.path.join(config.template_exp_dir, 'arpstrn.input')

# Create the arpstrn work directory in icbc scratch directory if it doesn't already exist.
arpstrn_work_dir = os.path.join(config.icbc_scr_dir, 'arpstrn_work')
if not os.path.exists(arpstrn_work_dir):
    os.makedirs(arpstrn_work_dir)
arpstrn_input_exp_path = os.path.join(arpstrn_work_dir,
                                      'arpstrn_{}.input'.format(config.exp_name))
arpstrn_output_exp_path = os.path.join(arpstrn_work_dir,
                                       'arpstrn_{}.output'.format(config.exp_name))

# Copy the arpstrn namelist template file to the working directory
# shutil.copy(arpstrn_input_template_path, arpstrn_work_dir)

# Edit the namelist file
editNamelistFile(arpstrn_input_template_path,
                 arpstrn_input_exp_path,
                 runname=config.exp_name,
                 nx=config.nx,
                 ny=config.ny,
                 nz=config.nz,
                 dx=config.dx,
                 dy=config.dy,
                 ctrlat=config.ctrlat,
                 ctrlon=config.ctrlon,
                 mapproj=config.mapproj,
                 trulat1=config.trulat1,
                 trulat2=config.trulat2,
                 trndataopt=config.trndataopt,
                 dir_trndata=config.dir_trndata,
                 nsmth=config.nsmth,
                 lat_sample=config.lat_sample,
                 lon_sample=config.lon_sample,
                 trnanxopt=config.trnanxopt,
                 dirname=config.arpstrn_output_dir,
                 terndmp=config.terndmp)

# Run arpstrn

with open(arpstrn_input_exp_path, 'r') as input, \
     open(arpstrn_output_exp_path, 'w') as output:
    print("Running {} for {}".format(config.arpstrn_exe_path, arpstrn_input_exp_path))
    subprocess.call(config.arpstrn_exe_path, stdin=input, stdout=output, shell=True)
