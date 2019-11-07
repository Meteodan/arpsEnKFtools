"""
This script runs arpssfc for a given experiment configuration. It takes one command-line argument,
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
from arpsenkftools import master_config_default as config

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
arpssfc_work_dir = os.path.join(config.icbc_scr_dir, 'arpssfc_work')
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
                 nstyp=config.nstyp,
                 sfcdmp=config.sfcdmp,
                 schmopt=config.schmopt,
                 sdatopt=config.sdatopt,
                 fstypfl=config.fstypfl,
                 bstypfl=config.bstypfl,
                 vdatopt=config.vdatopt,
                 fvtypfl=config.fvtypfl,
                 bvtypfl=config.bvtypfl,
                 ndatopt=config.ndatopt,
                 fndvifl=config.fndvifl,
                 bndvifl=config.bndvifl,
                 vfrcopt=config.vfrcopt,
                 vfrcdr=config.vfrcdr,
                 nsmthsl=config.nsmthsl,
                 stypout=config.stypout,
                 vtypout=config.vtypout,
                 laiout=config.laiout,
                 rfnsout=config.rfnsout,
                 vegout=config.vegout,
                 ndviout=config.ndviout,
                 dirname=config.arpssfc_output_dir)

# Run arpssfc

with open(arpssfc_input_exp_path, 'r') as input, \
     open(arpssfc_output_exp_path, 'w') as output:
    print("Running {} for {}".format(config.arpssfc_exe_path, arpssfc_input_exp_path))
    subprocess.call(config.arpssfc_exe_path, stdin=input, stdout=output, shell=True)
