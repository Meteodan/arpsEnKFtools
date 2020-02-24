"""
This script runs arpsintrp to create initial and boundary conditions from a coarser-res ARPS-EnKF
experiment. It takes one command-line argument,
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

# Determine whether we are using MPI
use_mpi = config.arpsintrp_param.get('use_mpi', False)

# Set the path to the arpsintrp.input namelist template file
arpsintrp_input_template_path = os.path.join(config.template_exp_dir, 'arpsintrp.input')

# Create the arpsintrp work directory in icbc scratch directory if it doesn't already exist.
arpsintrp_work_dir = os.path.join(config.prep_work_dir, 'arpsintrp_work')
if not os.path.exists(arpsintrp_work_dir):
    os.makedirs(arpsintrp_work_dir)
arpsintrp_input_t0_exp_path = os.path.join(arpsintrp_work_dir,
                                           'arpsintrp_{}_t0.input'.format(config.exp_name))
arpsintrp_output_t0_exp_path = os.path.join(arpsintrp_work_dir,
                                            'arpsintrp_{}_t0.output'.format(config.exp_name))
arpsintrp_input_lbc_exp_path = os.path.join(arpsintrp_work_dir,
                                            'arpsintrp_{}_lbc.input'.format(config.exp_name))
arpsintrp_output_lbc_exp_path = os.path.join(arpsintrp_work_dir,
                                             'arpsintrp_{}_lbc.output'.format(config.exp_name))

ens_member_list = range(1, config.num_ensemble_members + 1)
ens_member_names = ["ena%03d" % m for m in ens_member_list]
t0_interp_input_file_names = ["{}/{}.arpsintrp_t0.input".format(arpsintrp_work_dir, ens_member_name)
                              for ens_member_name in ens_member_names]
t0_interp_output_file_names = ["{}/{}.arpsintrp_t0.output".format(arpsintrp_work_dir,
                                                                  ens_member_name)
                               for ens_member_name in ens_member_names]
lbc_interp_input_file_names = ["{}/{}.arpsintrp_lbc.input".format(arpsintrp_work_dir,
                                                                  ens_member_name)
                               for ens_member_name in ens_member_names]
lbc_interp_output_file_names = ["{}/{}.arpsintrp_lbc.output".format(arpsintrp_work_dir,
                                                                    ens_member_name)
                                for ens_member_name in ens_member_names]
member_paths = ["{}/EN{:03d}/{}".format(config.ext_model_data_dir, m, ens_member_name)
                for m, ens_member_name in zip(ens_member_list, ens_member_names)]

# Pop some needed values from the arpsintrp_param dictionary imported from the config file
start_time = config.arpsintrp_param.pop('start_time')
end_time = config.arpsintrp_param.pop('end_time')
step_time = config.arpsintrp_param.pop('step_time')

for ens_member_name, t0_interp_input_file_name, lbc_interp_input_file_name, member_path in \
        zip(ens_member_names, t0_interp_input_file_names, lbc_interp_input_file_names,
            member_paths):

    # Initial conditions
    editNamelistFile(arpsintrp_input_template_path, t0_interp_input_file_name,
                     runname=ens_member_name,
                     hdmpfheader=member_path,
                     hdmpfmt=3,
                     exbcdmp=0,
                     tbgn_dmpin=start_time,
                     tend_dmpin=start_time,
                     tintv_dmpin=step_time,
                     **config.arpsintrp_param)

    # Boundary conditions
    editNamelistFile(arpsintrp_input_template_path, lbc_interp_input_file_name,
                     runname=ens_member_name,
                     hdmpfheader=member_path,
                     hdmpfmt=0,
                     exbcdmp=3,
                     tbgn_dmpin=start_time,
                     tend_dmpin=end_time,
                     tintv_dmpin=step_time,
                     **config.arpsintrp_param)

# Now run arpsintrp for all the members
# Make sure the target output directory exists
if not os.path.exists(config.arpsintrp_param['dirname']):
    os.makedirs(config.arpsintrp_param['dirname'])

for t0_interp_input_file_name, t0_interp_output_file_name, lbc_interp_input_file_name, \
        lbc_interp_output_file_name in zip(t0_interp_input_file_names,
                                           t0_interp_output_file_names,
                                           lbc_interp_input_file_names,
                                           lbc_interp_output_file_names):

    if use_mpi:
        command = [config.mpi_exe, config.mpi_nproc_flag,
                str(config.grid_param['nproc_x']*config.grid_param['nproc_y']),
                config.arpsintrp_exe_path]
    else:
        command = [config.arpsintrp_exe_path]

    with open(t0_interp_input_file_name, 'r') as inputfile, \
            open(t0_interp_output_file_name, 'w') as outputfile:
        print("Running {} for {}".format(config.arpsintrp_exe_path, t0_interp_input_file_name))
        job = subprocess.call(command, stdin=inputfile, stdout=outputfile)
        print("Job status = ", job)
    with open(lbc_interp_input_file_name, 'r') as inputfile, \
            open(lbc_interp_output_file_name, 'w') as outputfile:
        print("Running {} for {}".format(config.arpsintrp_exe_path, lbc_interp_input_file_name))
        job = subprocess.call(command, stdin=inputfile, stdout=outputfile)
        print("Job status = ", job)
