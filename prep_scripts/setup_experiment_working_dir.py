"""
This script sets up a working directory for an ARPS-EnKF experiment. It imports the master_config.py
file for that experiment and does the required copying and linking of needed files and directories.
"""

import os
import glob
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

# Create base experiment working directory
if not os.path.exists(config.exp_scr_dir):
    os.makedirs(config.exp_scr_dir)

# Copy/create/link needed files and directories

# For the boundary condition files, if perturb_ic is 1, then we are dealing with a deterministic
# external model where the boundary conditions need to be linked to for each ensemble member
# Do that here

boundary_dir = os.path.join(config.exp_scr_dir, 'boundary')
if not os.path.exists(boundary_dir):
    os.makedirs(boundary_dir)
boundary_files = glob.glob(config.external_icbc_dir + '/{}.*.*'.format(config.exp_name))

for boundary_file in boundary_files:
    boundary_file_name = os.path.basename(boundary_file)
    boundary_time_stamp = boundary_file_name.replace('{}'.format(config.exp_name), '')
    for member in range(1, config.num_ensemble_members + 1):
        ens_boundary_name = 'ena{:03d}{}'.format(member, boundary_time_stamp)
        ens_boundary_path = os.path.join(boundary_dir, ens_boundary_name)
        if os.path.lexists(ens_boundary_path):
            os.remove(ens_boundary_path)
        os.symlink(boundary_file, ens_boundary_path)

# STOPPED HERE!