#!/usr/bin/env python
#
# This script parses a bunch of NEWS-e WRF history files, generates
# a bunch of wrf2arps.input files (from a template) for each one,
# and optionally runs wrf2arps on them to generate ARPS initial and boundary condition
# files.
# Based on an older script for arpsintrp from RLT

import os
import subprocess
from datetime import datetime, timedelta
from arpsenkftools.editNamelist import editNamelistFile

# USER SPECIFICATIONS ###
# Absolute path to directory containing NEWS-e WRF history files
basedir = "/depot/dawson29/data/VORTEXSE/model_data/newse_data/"
# Absolute path to the arpsintrp.input template file
template = "/depot/dawson29/apps/arpsEnKFtools/icbc_scripts/wrf2arps.input.template"
# Absolute path to where the resulting arpsintrp input files should be stored.
rinPath = "/depot/dawson29/data/VORTEXSE/simulations/ARPS/2016_IOP3/EnKF/wrf2arps_input/"
# Name of the experiment (used as a prefix for the output):
expPrefix = "3km153x153"
# Number of ensemble members
n_ens_members = 1
member_start = 1
member_end = 1
# Start date, end date, and interval for history files to process
start_year = 2016
start_month = 3
start_day = 31
start_hour = 18
start_min = 0
start_sec = 0
start_date = datetime(start_year, start_month, start_day, start_hour, start_min, start_sec)

end_year = 2016
end_month = 4
end_day = 1
end_hour = 2
end_min = 45
end_sec = 0
end_date = datetime(end_year, end_month, end_day, end_hour, end_min, end_sec)

history_interval = 900  # seconds

datetime_range = [start_date + timedelta(seconds=x) for x in
                  range(0, (end_date-start_date).seconds + history_interval, history_interval)]

# Directory to save interpolated history files
outputdir = "/depot/dawson29/data/VORTEXSE/simulations/ARPS/2016_IOP3/EnKF/3km153x153_newseicbc"
# Option to run wrf2arps on the generated files
run_wrf2arps = True
run_t0 = True
run_lbc = True
# Absolute path to wrf2arps executable
wrf2arps_exe = '/home/dawson29/arps5.4_main/bin/wrf2arps'
# MPI executable (if desired)
run_mpi = False
mpi_exe = 'mpiexec'
mpi_numproc_arg = '-n'
# MPI parameters
nproc_x = 5
nproc_y = 2
nproc_x_in = 10
nproc_y_in = 6
nproc_x_out = 1
nproc_y_out = 1
# inisplited = 0000001
dmp_out_joined = 1  # 1111111

# END OF USER SPECIFICATIONS ###

newse_timestrings = [d.strftime('%Y-%m-%d_%H:%M:%S') for d in datetime_range]
fn_timestrings = [d.strftime('%Y-%m-%d_%H_%M_%S') for d in datetime_range]
ens_member_list = range(member_start, member_end + 1)
ens_member_names = ["ena%03d" % m for m in ens_member_list]

# Create a list of dictionaries to store the input/output file names as well as the NEWS-e
# output file associated with it.

wrf2arps_dict_list = []
for newse_timestring, fn_timestring in zip(newse_timestrings, fn_timestrings):
    for ens_member, ens_member_name in zip(ens_member_list, ens_member_names):

        t0_input_file_name = "{}/{}_{}.wrf2arps_t0.input".format(rinPath, ens_member_name,
                                                                 fn_timestring)
        t0_output_file_name = "{}/{}_{}.wrf2arps_t0.output".format(rinPath, ens_member_name,
                                                                   fn_timestring)
        lbc_input_file_name = "{}/{}_{}.wrf2arps_lbc.input".format(rinPath, ens_member_name,
                                                                   fn_timestring)
        lbc_output_file_name = "{}/{}_{}.wrf2arps_lbc.output".format(rinPath, ens_member_name,
                                                                     fn_timestring)
        wrfout_file_name = "wrfout_d01_{}_{:d}".format(newse_timestring, ens_member)
        wrf2arps_dict = dict(t0_input_file_name=t0_input_file_name,
                             t0_output_file_name=t0_output_file_name,
                             lbc_input_file_name=lbc_input_file_name,
                             lbc_output_file_name=lbc_output_file_name,
                             ens_member_name=ens_member_name,
                             ens_member=ens_member,
                             wrfout_file_name=wrfout_file_name,
                             newse_timestring=newse_timestring)
        wrf2arps_dict_list.append(wrf2arps_dict)

for wrf2arps_dict in wrf2arps_dict_list:

    t0_input_file_name = wrf2arps_dict['t0_input_file_name']
    t0_output_file_name = wrf2arps_dict['t0_output_file_name']
    lbc_input_file_name = wrf2arps_dict['lbc_input_file_name']
    lbc_output_file_name = wrf2arps_dict['lbc_output_file_name']
    ens_member_name = wrf2arps_dict['ens_member_name']
    newse_timestring = wrf2arps_dict['newse_timestring']
    ens_member = wrf2arps_dict['ens_member']

    # Initial conditions
    editNamelistFile("{}".format(template),
                     t0_input_file_name,
                     dir_extd=basedir,
                     runname="%s" % ens_member_name,
                     init_time_str=newse_timestring[0],
                     start_time_str=newse_timestring,
                     end_time_str=newse_timestring,
                     dirname=outputdir,
                     dmp_out_joined=dmp_out_joined,
                     hdmpfmt=3,
                     exbcdmp=0)

    # Boundary conditions
    editNamelistFile("{}".format(template),
                     lbc_input_file_name,
                     dir_extd=basedir,
                     runname="%s" % ens_member_name,
                     init_time_str=newse_timestring[0],
                     start_time_str=newse_timestring,
                     end_time_str=newse_timestring,
                     dirname=outputdir,
                     dmp_out_joined=dmp_out_joined,
                     hdmpfmt=0,
                     exbcdmp=3)

    if run_wrf2arps:

        # Need to make a temporary softlink to the correct wrfout file but removing the ensemble
        # member from the end, because this is what wrf2arps is expecting
        wrfout_file_name = wrf2arps_dict['wrfout_file_name']
        wrfout_file_link_name = "wrfout_d01_{}".format(newse_timestring)
        wrfout_file_path = os.path.join(basedir, wrfout_file_name)
        wrfout_file_link_path = os.path.join(basedir, wrfout_file_link_name)

        command = 'ln -sf {} {}'.format(wrfout_file_path, wrfout_file_link_path)
        print("Linking {} to {}".format(wrfout_file_link_path, wrfout_file_path))
        subprocess.call(command, shell=True)

        if run_mpi:
            command = '{} {} {:d} {}'.format(mpi_exe, mpi_numproc_arg, nproc_x*nproc_y,
                                             wrf2arps_exe)
        else:
            command = '{}'.format(wrf2arps_exe)
        if run_t0:
            with open(t0_input_file_name, 'r') as input, \
                 open(t0_output_file_name, 'w') as output:
                print("Running %s for %s" % (wrf2arps_exe, t0_input_file_name))
                subprocess.call(command, stdin=input, stdout=output, shell=True)
        if run_lbc:
            with open(lbc_input_file_name, 'r') as input, \
                 open(lbc_output_file_name, 'w') as output:
                print("Running %s for %s" % (wrf2arps_exe, lbc_input_file_name))
                subprocess.call(command, stdin=input, stdout=output, shell=True)

        # Now remove the softlink
        command = 'unlink {}'.format(wrfout_file_link_path)
        subprocess.call(command, shell=True)
