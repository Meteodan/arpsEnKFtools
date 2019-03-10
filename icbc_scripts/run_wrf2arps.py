#!/usr/bin/env python
#
# This script parses a bunch of NEWS-e WRF history files, generates
# a bunch of wrf2arps.input files (from a template) for each one,
# and optionally runs wrf2arps on them to generate ARPS initial and boundary condition
# files.
# Based on an older script for arpsintrp from RLT

import subprocess
from datetime import datetime, timedelta
from arpsenkftools.editNamelist import editNamelistFile

### USER SPECIFICATIONS ###
# Absolute path to directory containing NEWS-e WRF history files
basedir = "/depot/dawson29/data/VORTEXSE/model_data/newse_data/"
# Absolute path to the arpsintrp.input template file
template = "/depot/dawson29/apps/arpsEnKFtools/icbc_scripts/wrf2arps.input.template"
# Absolute path to where the resulting arpsintrp input files should be stored.
rinPath = "/depot/dawson29/data/VORTEXSE/simulations/ARPS/2016_IOP3/EnKF/wrf2arps_input/"
# Name of the experiment (used as a prefix for the output):
expPrefix = "3km153x153"
# Number of ensemble members
n_ens_members = 40
member_start = 1
member_end = 40
# Start date, end date, and interval for history files to process
start_year = 2016
start_month = 3
start_day = 31
start_hour = 18
start_min = 0
start_sec = 0
start_date = datetime(start_year, start_month, start_day, start_hour, start_min, start_sec)

end_year = 2016
end_month = 3
end_day = 31
end_hour = 18
end_min = 0
end_sec = 0
end_date = datetime(end_year, end_month, end_day, end_hour, end_min, end_sec)

history_interval = 900  # seconds

datetime_range = [start_date + timedelta(seconds=x) for x in
                  range(0, (end_date-start_date).seconds + history_interval, history_interval)]

# Directory to save interpolated history files
outputdir = "/depot/dawson29/data/VORTEXSE/simulations/ARPS/2016_IOP3/EnKF/3km153x153_newseicbc"
# Option to run wrf2arps on the generated files
run_wrf2arps = False
run_t0 = False
run_lbc = False
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

### END OF USER SPECIFICATIONS ###

ens_member_list = range(member_start, member_end + 1)
ens_member_names = ["ena%03d" % m for m in ens_member_list]
t0_interp_input_file_names = ["%s/%s.wrf2arps_t0.input" % (rinPath, ens_member_name)
                              for ens_member_name in ens_member_names]
t0_interp_output_file_names = ["%s/%s.wrf2arps_t0.output" % (rinPath, ens_member_name)
                               for ens_member_name in ens_member_names]
lbc_interp_input_file_names = ["%s/%s.wrf2arps_lbc.input" % (rinPath, ens_member_name)
                               for ens_member_name in ens_member_names]
lbc_interp_output_file_names = ["%s/%s.wrf2arps_lbc.output" % (rinPath, ens_member_name)
                                for ens_member_name in ens_member_names]
newse_timestrings = [d.strftime('%Y-%m-%d_%H:%M:%S') for d in datetime_range]

for ens_member_name, t0_interp_input_file_name, lbc_interp_input_file_name, newse_timestring in \
        zip(ens_member_names, t0_interp_input_file_names, lbc_interp_input_file_names,
            newse_timestrings):

    # Initial conditions
    editNamelistFile("{}".format(template), t0_interp_input_file_name,
                     dir_extd=basedir,
                     runname="%s" % ens_member_name,
                     init_time_str=newse_timestring,
                     start_time_str=newse_timestring,
                     end_time_str=newse_timestring,
                     dirname=outputdir,
                     dmp_out_joined=dmp_out_joined,
                     hdmpfmt=3,
                     exbcdmp=0)

    # Boundary conditions
    editNamelistFile("{}".format(template), lbc_interp_input_file_name,
                     dir_extd=basedir,
                     runname="%s" % ens_member_name,
                     init_time_str=newse_timestring,
                     start_time_str=newse_timestring,
                     end_time_str=newse_timestring,
                     dirname=outputdir,
                     dmp_out_joined=dmp_out_joined,
                     hdmpfmt=0,
                     exbcdmp=3)

if run_wrf2arps:
    for t0_interp_input_file_name, t0_interp_output_file_name, lbc_interp_input_file_name, \
            lbc_interp_output_file_name in zip(t0_interp_input_file_names,
                                               t0_interp_output_file_names,
                                               lbc_interp_input_file_names,
                                               lbc_interp_output_file_names):
        if run_mpi:
            command = '{} {} {:d} {}'.format(mpi_exe, mpi_numproc_arg, nproc_x*nproc_y,
                                             wrf2arps_exe)
        else:
            command = '{}'.format(wrf2arps_exe)
        if run_t0:
            with open(t0_interp_input_file_name, 'r') as input, \
                 open(t0_interp_output_file_name, 'w') as output:
                print("Running %s for %s" % (wrf2arps_exe, t0_interp_input_file_name))
                subprocess.call(command, stdin=input, stdout=output, shell=True)
        if run_lbc:
            with open(lbc_interp_input_file_name, 'r') as input, \
                 open(lbc_interp_output_file_name, 'w') as output:
                print("Running %s for %s" % (wrf2arps_exe, lbc_interp_input_file_name))
                subprocess.call(command, stdin=input, stdout=output, shell=True)
