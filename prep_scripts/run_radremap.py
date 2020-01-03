"""
This script runs the radar remapper (88d2arps) to map the polar radar data onto the ARPS grid.
It takes one command-line argument,
the (python) configuration file for that experiment, from which it imports the appropriate info
"""

import os
import sys
import glob
import shutil
import subprocess
import threading
from arpsenkftools.editNamelist import editNamelistFile
from arpsenkftools.io_utils import import_all_from


def run_remapper(command_arg_list):
    """Runs the radar remapper"""
    exe_path = command_arg_list[0]
    input_file_path = command_arg_list[1]
    output_file_path = command_arg_list[2]
    input_file = open(input_file_path, 'r')
    output_file = open(output_file_path, 'w')
    p = subprocess.Popen([exe_path], stdin=input_file, stdout=output_file)
    p.wait()
    print("Job {} for {} completed, return code: {}".format(exe_path, input_file_path,
                                                            str(p.returncode)))
    input_file.close()
    output_file.close()


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

# Set the path to the radremap_88D.input namelist template file
radremap_input_template_path = os.path.join(config.template_exp_dir, 'radremap_88D.input')

# Create the radremap work directory in icbc scratch directory if it doesn't already exist.
radremap_work_dir = os.path.join(config.prep_work_dir, 'radremap_work')
if not os.path.exists(radremap_work_dir):
    os.makedirs(radremap_work_dir)

radar_list = config.radremap_param.pop('radar_list')

# Loop through radars
for radname in radar_list:
    # Get the list of level-2 radar data files
    level2_paths = glob.glob(config.radar_obs_dir + '/{}*'.format(radname))
    level2_file_names = [os.path.basename(level2_path) for level2_path in level2_paths]
    level2_file_times = []
    # Create working subdirectory for the current radar
    radar_work_dir = os.path.join(radremap_work_dir, radname)
    if not os.path.exists(radar_work_dir):
        os.makedirs(radar_work_dir)
    # Link the radarinfo.dat file
    if not os.path.lexists(os.path.join(radar_work_dir, 'radarinfo.dat')):
        os.symlink(config.template_base_dir + '/radarinfo.dat', radar_work_dir + '/radarinfo.dat')

    # create the list of radremap input and output file names
    radremap_input_file_paths = ["{}/{}.radremap_88D.input".format(radar_work_dir, level2_file_name)
                                 for level2_file_name in level2_file_names]
    radremap_output_file_paths = ["{}/{}.radremap_88D.output".format(radar_work_dir,
                                                                     level2_file_name)
                                  for level2_file_name in level2_file_names]

    # Create output directory for remapped radar files if it doesn't already exist
    if not os.path.exists(config.remapped_radar_dir):
        os.makedirs(config.remapped_radar_dir)
    # Link the radarinfo.dat file into the remapped radar directory
    radarinfo_link = os.path.join(config.remapped_radar_dir, config.radarinfo_file)
    if not os.path.exists(radarinfo_link):
        os.symlink(config.radarinfo_path, radarinfo_link)
    # Change directories to the output directory
    os.chdir(config.remapped_radar_dir)

    # Create the namelist files
    initime_stamp = config.initial_datetime.strftime('%Y-%m-%d.%H:%M:00')
    for level2_file_name, level2_path, radremap_input_file_path, radremap_output_file_path in \
            zip(level2_file_names, level2_paths, radremap_input_file_paths,
                radremap_output_file_paths):
        editNamelistFile(radremap_input_template_path, radremap_input_file_path,
                         **config.grid_param,
                         initime=initime_stamp,
                         inifile=config.external_inifile_path,
                         inigbf=config.external_inigbf_path,
                         radname=radname,
                         radfname=level2_path,
                         dirname=config.remapped_radar_dir + '/')

    # Run the radar remapper for each file
    count = 0
    commands = []
    nthreads = config.radremap_param.get('nthreads', 1)
    nfiles = len(level2_file_names)
    for i, level2_file_name, level2_path, radremap_input_file_path, radremap_output_file_path in \
            zip(range(nfiles), level2_file_names, level2_paths,
                radremap_input_file_paths, radremap_output_file_paths):
        radar_time = level2_file_name[4:19]
        radar_time_subdir = os.path.join(config.remapped_radar_dir, radar_time)
        if not os.path.exists(radar_time_subdir):
            os.makedirs(radar_time_subdir)

        if count < nthreads:
            commands.append([config.radremap_exe_path, radremap_input_file_path,
                             radremap_output_file_path])
        count += 1
        if count == nthreads or i == nfiles - 1:
            proc = [threading.Thread(target=run_remapper, kwargs={'command_arg_list': cmd})
                    for cmd in commands]
            [p.start() for p in proc]
            [p.join() for p in proc]
            print("Done with batch!")
            count = 0
            commands = []

        # with open(radremap_input_file_path, 'r') as input_file, \
        #         open(radremap_output_file_path, 'w') as output_file:
        #     print("Running {} for {}".format(config.radremap_exe_path, radremap_input_file_path))
        #     subprocess.call(config.radremap_exe_path, stdin=input_file, stdout=output_file,
        #                     shell=True)

        # Check for auxilliary files and move them into an appropriate subdirectory
        refl_files = glob.glob(config.remapped_radar_dir + '/*refl*')
        if refl_files:
            for refl_file in refl_files:
                shutil.move(refl_file, radar_time_subdir)
        tilt_files = glob.glob(config.remapped_radar_dir + '/*tilts*')
        if tilt_files:
            for tilt_files in tilt_files:
                shutil.move(tilt_files, radar_time_subdir)
