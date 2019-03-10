#!/usr/bin/env python
#
# This script parses a bunch of NEWS-e WRF history files, generates
# a bunch of wrf2arps.input files (from a template) for each one,
# and optionally runs wrf2arps on them to generate ARPS initial and boundary condition
# files.
# Based on an older script for arpsintrp from RLT

import os
import glob
import sys
import subprocess
sys.path.append('/Users/dawson29/arpsEnKFtools/modules/')
from editNamelist import editNamelistFile


### USER SPECIFICATIONS ###
# Absolute path to directory containing NEWS-e WRF history files
basedir = "/depot/dawson29/data/VORTEXSE/model_data/newse_data/"
# Absolute path to the arpsintrp.input template file
template = "/Users/dawson29/arpsEnKFtools/EnKF_intrp/wrf2arps.input.template"
# Absolute path to where the resulting arpsintrp input files should be stored.
rinPath = "/depot/dawson29/Projects/VORTEXSE/simulations/ARPS/2016_IOP3/EnKF/wrf2arps_input/"
# Name of the experiment (used as a prefix for the output):
expPrefix = "3km153x153"
# Number of ensemble members
n_ens_members = 40
member_start = 1
member_end = 40
# Start date, end date, and interval for history files to process
start

# Start, End, Step time for history files to process
start_time = 36000.
end_time = 54000.
step_time = 300.
# Directory to save interpolated history files
outputdir = "/Volumes/depot/dawson29/data/VORTEXSE/simulations/ARPS/2016_IOP3/EnKF/3km153x153_6kmconvicbc"
# Option to run arpsintrp on the generated files
run_arpsintrp = True
run_t0 = False
run_lbc = True
# Absolute path to arpsintrp executable
arpsintrp_exe = '/Users/dawson29/arps5.4_exp/bin/arpsintrp_mpi'
# MPI executable (if desired)
mpi_exe = '/opt/openmpi/bin/mpirun'
# MPI parameters
nproc_x = 5
nproc_y = 2
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
sys.path.append('/Users/dawson29/arpsEnKFtools/modules/')
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
        dmp_out_joined=dmp_out_joined)

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
        exbcdmp=3)

if run_arpsintrp:
    for t0_interp_input_file_name, t0_interp_output_file_name, lbc_interp_input_file_name, \
            lbc_interp_output_file_name in zip(t0_interp_input_file_names, \
            t0_interp_output_file_names, lbc_interp_input_file_names, \
            lbc_interp_output_file_names):

        command='%s -np %d %s' % (mpi_exe, nproc_x*nproc_y, arpsintrp_exe)
        if run_t0:
            with open(t0_interp_input_file_name, 'r') as input, \
                 open(t0_interp_output_file_name, 'w') as output:
                print "Running %s for %s" % (arpsintrp_exe, t0_interp_input_file_name)
                subprocess.call(command, stdin=input, stdout=output, shell=True)
        if run_lbc:
            with open(lbc_interp_input_file_name, 'r') as input, \
                 open(lbc_interp_output_file_name, 'w') as output:
                print "Running %s for %s" % (arpsintrp_exe, lbc_interp_input_file_name)
                subprocess.call(command, stdin=input, stdout=output, shell=True)




