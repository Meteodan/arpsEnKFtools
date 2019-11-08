"""
This script runs ext2arps for a given experiment configuration. It takes one command-line argument,
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

# Set the path to the ext2arps.input namelist template file
ext2arps_input_template_path = os.path.join(config.template_exp_dir, 'ext2arps.input')

# Create the ext2arps work directory in icbc scratch directory if it doesn't already exist.
ext2arps_work_dir = os.path.join(config.icbc_scr_dir, 'ext2arps_work')
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
extdfile_args = {
    'initime': config.ext2arps_initime,
    'ternopt': config.ternopt,
    'terndta': config.terndta,
    'ternfmt': config.ternfmt,
    'extdopt': config.extdopt,
    'extdfmt': config.extdfmt,
    'dir_extd': config.dir_extd,
    'extdname': config.extdname,
    'iorder': config.iorder,
    'intropt': config.intropt,
    'nsmooth': config.nsmooth,
    'exttrnopt': config.exttrnopt,
    'extntmrg': config.extntmrg,
    'extsfcopt': config.extsfcopt,
    'ext_lbc': config.ext_lbc,
    'ext_vbc': config.ext_vbc,
    'grdbasopt': config.grdbasopt,
    'dmp_out_joined': config.dmp_out_joined,
    'dirname': config.ext2arps_output_dir
}

# Now loop through the times in the "extdtimes" list from the master_config.py and create
# the appropriate key-value pairs for passing to the editNamelistFile function below

for i in range(1, config.nextdfil + 1):
    extdfile_args['extdtime({:d})'.format(i)] = config.extdtimes[i-1]

# Additional parameters for initial condition (t0) run

extdfile_t0_args = extdfile_args.copy()
new_args = {
    'hdmpopt': 1,
    'hdmpfmt': config.hdmpfmt,
    'hdfcompr': config.hdfcompr,
    'exbcdmp': 0,
    'nextdfil': 1
}
extdfile_t0_args.update(new_args)

# Create namelist file for t0 run
editNamelistFile(ext2arps_input_template_path,
                 ext2arps_input_t0_exp_path,
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
                 **extdfile_t0_args)

# Additional parameters for lateral boundary condition (lbc) run

extdfile_lbc_args = extdfile_args.copy()
new_args = {
    'hdmpfmt': 0,
    'exbcdmp': config.exbcdmp,
    'exbchdfcompr': config.exbchdfcompr,
    'extdadmp': config.extdadmp,
    'qcexout': config.qcexout,
    'qrexout': config.qrexout,
    'qiexout': config.qiexout,
    'qsexout': config.qsexout,
    'qhexout': config.qhexout,
    'qgexout': config.qgexout,
    'nqexout': config.nqexout,
    'zqexout': config.zqexout,
    'nextdfil': config.nextdfil
}
extdfile_lbc_args.update(new_args)

# Create namelist file for lbc run
editNamelistFile(ext2arps_input_template_path,
                 ext2arps_input_lbc_exp_path,
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
                 **extdfile_lbc_args)

# # Run ext2arps

# Make sure the target output directory exists
if not os.path.exists(config.ext2arps_output_dir):
    os.makedirs(config.ext2arps_output_dir)

# with open(ext2arps_input_t0_exp_path, 'r') as input_file, \
#      open(ext2arps_output_t0_exp_path, 'w') as output_file:
#     print("Running {} for {}".format(config.ext2arps_exe_path, ext2arps_input_t0_exp_path))
#     subprocess.call(config.ext2arps_exe_path, stdin=input_file, stdout=output_file, shell=True)

with open(ext2arps_input_lbc_exp_path, 'r') as input_file, \
     open(ext2arps_output_lbc_exp_path, 'w') as output_file:
    print("Running {} for {}".format(config.ext2arps_exe_path, ext2arps_input_lbc_exp_path))
    subprocess.call(config.ext2arps_exe_path, stdin=input_file, stdout=output_file, shell=True)
