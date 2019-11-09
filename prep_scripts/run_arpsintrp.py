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

# STOPPED HERE!

### USER SPECIFICATIONS ###
# Absolute path to directory containing ARPS history files
basedir = "/scratch/rice/d/dawson29/VORTEXSE/simulations/ARPS/2016_IOP3/EnKF/6kmconv/6kmconv"
# Absolute path to the arpsintrp.input template file
template = "/depot/dawson29/apps/arpsEnKFtools/EnKF_intrp/arpsintrp.input.template"
# Absolute path to where the resulting arpsintrp input files should be stored.
rinPath = "/home/dawson29/Projects/VORTEXSE/simulations/ARPS/2016_IOP3/EnKF/arpsintrp_input"
# Name of the experiment (used as a prefix for the output):
expPrefix = "3km153x153"
# Location of terrain data file
trndata = "/depot/dawson29/data/VORTEXSE/simulations/ARPS/trndata/"
# Number of ensemble members
n_ens_members = 40
member_start = 40
member_end = 40
# Start, End, Step time for history files to process
start_time = 36000.
end_time = 54000.
step_time = 300.
# Directory to save interpolated history files
outputdir = "/depot/dawson29/data/VORTEXSE/simulations/ARPS/2016_IOP3/EnKF/3km153x153_6kmconvicbc"
# Option to run arpsintrp on the generated files
run_arpsintrp = True
run_t0 = False
run_lbc = True
# Absolute path to arpsintrp executable
arpsintrp_exe = '/home/dawson29/arps5.4/bin/arpsintrp_mpi'
# MPI executable (if desired)
mpi_exe = 'mpiexec'
mpi_nproc_flag = '-n'
# MPI parameters
nproc_x = 10
nproc_y = 6
nproc_x_in = 10
nproc_y_in = 6
nproc_x_out = 1
nproc_y_out = 1
inisplited = 0000001
dmp_out_joined = 1111111

### END OF USER SPECIFICATIONS ###

import os
import glob
import sys
import subprocess
sys.path.append('/depot/dawson29/apps/arpsEnKFtools/modules/')
from editNamelist import editNamelistFile

ens_member_list = xrange(member_start, member_end + 1)
ens_member_names = ["ena%03d" % m for m in ens_member_list]
t0_interp_input_file_names = ["%s/%s.arpsintrp_t0.input" % (rinPath, ens_member_name)
                           for ens_member_name in ens_member_names]
t0_interp_output_file_names = ["%s/%s.arpsintrp_t0.output" % (rinPath, ens_member_name)
                            for ens_member_name in ens_member_names]
lbc_interp_input_file_names = ["%s/%s.arpsintrp_lbc.input" % (rinPath, ens_member_name)
                           for ens_member_name in ens_member_names]
lbc_interp_output_file_names = ["%s/%s.arpsintrp_lbc.output" % (rinPath, ens_member_name)
                            for ens_member_name in ens_member_names]
member_paths = ["%s/EN%03d/%s" % (basedir, m, ens_member_name) for m, ens_member_name in
                zip(ens_member_list, ens_member_names)]

for ens_member_name, t0_interp_input_file_name, lbc_interp_input_file_name, member_path in \
        zip(ens_member_names, t0_interp_input_file_names, lbc_interp_input_file_names, \
        member_paths):

    # Initial conditions
    editNamelistFile("%s" % template, t0_interp_input_file_name,
        runname="%s" % ens_member_name,
        hdmpfheader=member_path,
        dirname=outputdir,
        tbgn_dmpin=start_time,
        tend_dmpin=start_time,
        tintv_dmpin=step_time,
        nproc_x=nproc_x,
        nproc_y=nproc_y,
        nproc_x_in=nproc_x_in,
        nproc_y_in=nproc_y_in,
        nproc_x_out=nproc_x_out,
        nproc_y_out=nproc_y_out,
        inisplited=inisplited,
        dmp_out_joined=dmp_out_joined,
        terndta1="%s/%s.trndata" % (trndata, expPrefix))

    # Boundary conditions
    editNamelistFile("%s" % template, lbc_interp_input_file_name,
        runname="%s" % ens_member_name,
        hdmpfheader=member_path,
        dirname=outputdir,
        tbgn_dmpin=start_time,
        tend_dmpin=end_time,
        tintv_dmpin=step_time,
        nproc_x=nproc_x,
        nproc_y=nproc_y,
        nproc_x_in=nproc_x_in,
        nproc_y_in=nproc_y_in,
        nproc_x_out=nproc_x_out,
        nproc_y_out=nproc_y_out,
        inisplited=inisplited,
        dmp_out_joined=dmp_out_joined,
        hdmpfmt=0,
        exbcdmp=3,
        terndta1="%s/%s.trndata" % (trndata, expPrefix))

if run_arpsintrp:
    for t0_interp_input_file_name, t0_interp_output_file_name, lbc_interp_input_file_name, \
            lbc_interp_output_file_name in zip(t0_interp_input_file_names, \
            t0_interp_output_file_names, lbc_interp_input_file_names, \
            lbc_interp_output_file_names):

        #command='exec %s %s %d %s' % (mpi_exe, mpi_nproc_flag, nproc_x*nproc_y, arpsintrp_exe)
        command=[mpi_exe, mpi_nproc_flag, str(nproc_x*nproc_y), arpsintrp_exe]

        if run_t0:
            with open(t0_interp_input_file_name, 'r') as inputfile, \
                 open(t0_interp_output_file_name, 'w') as outputfile:
                print "Running %s for %s" % (arpsintrp_exe, t0_interp_input_file_name)
                job = subprocess.call(command, stdin=inputfile, stdout=outputfile)
                print "Job status = ",job
        if run_lbc:
            with open(lbc_interp_input_file_name, 'r') as inputfile, \
                 open(lbc_interp_output_file_name, 'w') as outputfile:
                print "Running %s for %s" % (arpsintrp_exe, lbc_interp_input_file_name)
                job = subprocess.call(command, stdin=inputfile, stdout=outputfile)
                print "Job status = ",job



