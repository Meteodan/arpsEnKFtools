"""
This script sets up a working directory for an ARPS-EnKF experiment. It imports the master_config.py
file for that experiment and does the required copying and linking of needed files and directories.
"""

import os
import glob
import sys
import shutil
from arpsenkftools.editNamelist import editNamelistFile
from arpsenkftools.io_utils import import_all_from


# Function definitions
def generate_namelist_input_file_template(namelist_input_path, target_dir, config_dict_list):
    """Generates initial namelist input file template for a new experiment

    Parameters
    ----------
    namelist_input_path : str
        Path to original namelist input file
    target_dir : str
        Target directory for the new namelist input file template
    config_dict_list : list of dicts
        List of configuration dictionaries from master_config.py containing the
        namelist parameters that need modified for the new namelist input template file
    """
    namelist_args = {}
    for config_dict in config_dict_list:
        namelist_args.update(config_dict)
    namelist_input_target = os.path.join(target_dir, os.path.basename(namelist_input_path))
    editNamelistFile(namelist_input_path,
                     namelist_input_target,
                     **namelist_args)


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
        sys.exit()
else:
    print("Please provide an experiment configuration file on the command line! Exiting!")

# Create base experiment working directory
print("Creating experiment working directory: {}".format(config.exp_scr_dir))
if not os.path.exists(config.exp_scr_dir):
    os.makedirs(config.exp_scr_dir)

# Copy/create/link needed files and directories

# For the boundary condition files, if perturb_ic is 1, then we are dealing with a deterministic
# external model where the boundary conditions need to be linked to for each ensemble member
# Do that here

print("Linking initial and boundary condition files...")
boundary_dir = os.path.join(config.exp_scr_dir, 'boundary')
if not os.path.exists(boundary_dir):
    os.makedirs(boundary_dir)
if config.perturb_ic:
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
    # Link initial condition files to root of working directory
    target_inifile = os.path.join(config.exp_scr_dir, config.external_inifile)
    target_inigbf = os.path.join(config.exp_scr_dir, config.external_inigbf)
    if os.path.lexists(target_inifile):
        os.remove(target_inifile)
    if os.path.lexists(target_inigbf):
        os.remove(target_inigbf)
    os.symlink(config.external_inifile_path, target_inifile)
    os.symlink(config.external_inigbf_path, target_inigbf)
else:
    all_icbc_paths = glob.glob(config.external_icbc_dir + '/*')
    for icbc_path in all_icbc_paths:
        icbc_file = os.path.basename(icbc_path)
        target_path = os.path.join(boundary_dir, icbc_file)
        if os.path.lexists(target_path):
            os.remove(target_path)
        os.symlink(icbc_path, target_path)

# Link terrain and surface characteristic files
print("Linking terrain and surface characteristic files...")
target_trndata_path = os.path.join(config.exp_scr_dir, config.trndata_file)
target_sfcdata_path = os.path.join(config.exp_scr_dir, config.sfcdata_file)
if os.path.lexists(target_trndata_path):
    os.remove(target_trndata_path)
if os.path.lexists(target_sfcdata_path):
    os.remove(target_sfcdata_path)
os.symlink(config.trndata_path, target_trndata_path)
os.symlink(config.sfcdata_path, target_sfcdata_path)

# Link executable files
print("Linking executable files...")
arps_exe_target = os.path.join(config.exp_scr_dir, 'arps')
arpsenkfic_exe_target = os.path.join(config.exp_scr_dir, 'arpsenkfic')
arpsenkf_exe_target = os.path.join(config.exp_scr_dir, 'arpsenkf')
if os.path.lexists(arps_exe_target):
    os.remove(arps_exe_target)
if os.path.lexists(arpsenkfic_exe_target):
    os.remove(arpsenkfic_exe_target)
if os.path.lexists(arpsenkf_exe_target):
    os.remove(arpsenkf_exe_target)
os.symlink(config.arps_exe_path, arps_exe_target)
os.symlink(config.arpsenkfic_exe_path, arpsenkfic_exe_target)
os.symlink(config.arpsenkf_exe_path, arpsenkf_exe_target)

# Link conventional observations
print("Linking conventional observation files...")
obs_dir = os.path.join(config.exp_scr_dir, 'obs')
if not os.path.exists(obs_dir):
    os.makedirs(obs_dir)

# Look at lso files for each obs type and create links to them. For now only asos5min,
# but will add others soon.
# TODO: refactor into function
try:
    asos5min_paths = glob.glob(config.sfc_obs_dir + '/asos5min*lso')
    asos5min_files = [os.path.basename(asos5min_path) for asos5min_path in asos5min_paths]
    target_files = [asos5min_file.replace('asos5min', '') for asos5min_file in asos5min_files]
    # Lame. We need to add an additional "00" for the seconds field.
    target_files = [target_file.replace('.lso', '00.lso') for target_file in target_files]
    target_paths = [os.path.join(obs_dir, target_file) for target_file in target_files]

    for asos5min_path, asos5min_target_path in zip(asos5min_paths, target_paths):
        if os.path.lexists(asos5min_target_path):
            os.remove(asos5min_target_path)
        os.symlink(asos5min_path, asos5min_target_path)
except:
    print("Linking surface observations failed!")

# Now create links to sounding files
try:
    snd_paths = glob.glob(config.ua_obs_dir + '/raob*snd')
    snd_files = [os.path.basename(snd_path) for snd_path in snd_paths]
    target_files = [snd_file.replace('raob', '') for snd_file in snd_files]
    # Lame. We need to add an additional "00" for the seconds field.
    # target_files = [target_file.replace('.snd', '00.snd') for target_file in target_files]
    target_paths = [os.path.join(obs_dir, target_file) for target_file in target_files]

    for snd_path, snd_target_path in zip(snd_paths, target_paths):
        if os.path.lexists(snd_target_path):
            os.remove(snd_target_path)
        os.symlink(snd_path, snd_target_path)
except:
    print("Linking upper air observations failed!")

# Generate namelist input templates
print("Generating and copying namelist input template files...")
namelist_input_template_dir = os.path.join(config.exp_scr_dir, 'inputfiletemplates')
if not os.path.exists(namelist_input_template_dir):
    os.makedirs(namelist_input_template_dir)
arps_input_path = os.path.join(config.template_exp_dir, 'arps.input')
arpsenkfic_input_path = os.path.join(config.template_exp_dir, 'arpsenkfic.input')
arpsenkf_input_path = os.path.join(config.template_exp_dir, 'arpsenkf.input')

generate_namelist_input_file_template(arps_input_path, namelist_input_template_dir,
                                      [config.grid_param, config.arps_param])
generate_namelist_input_file_template(arpsenkfic_input_path, namelist_input_template_dir,
                                      [config.grid_param, config.arpsenkfic_param])
generate_namelist_input_file_template(arpsenkf_input_path, namelist_input_template_dir,
                                      [config.grid_param, config.arpsenkf_param])

# Link scattering amplitude lookup tables
print("Linking scattering amplitude lookup tables...")
scatt_dir = os.path.join(config.exp_scr_dir, 'scatt')
if not os.path.exists(scatt_dir):
    os.makedirs(scatt_dir)
scatt_subdirs = glob.glob(config.arps_base_dir + '/data/scatt/*')
for scatt_subdir in scatt_subdirs:
    scatt_subdir_basename = os.path.basename(scatt_subdir)
    scatt_subdir_target = os.path.join(scatt_dir, scatt_subdir_basename)
    if not os.path.exists(scatt_subdir_target):
        os.makedirs(scatt_subdir_target)
    scatt_paths = glob.glob(scatt_subdir + '/*')
    for scatt_path in scatt_paths:
        scatt_file = os.path.basename(scatt_path)
        scatt_target_path = os.path.join(scatt_subdir_target, scatt_file)
        if os.path.lexists(scatt_target_path):
            os.remove(scatt_target_path)
        os.symlink(scatt_path, scatt_target_path)

# Link remapped radar data files
# For now just link the entire directory. ARPSENKF will just read the needed files from there.
# Assumes the remapped radar files have already been created with run_radremap.py and links have
# been made to the times that ARPSENKF is expecting (with link_radremap.py).
try:
    print("Linking remapped radar files...")
    radar_dir = os.path.join(config.exp_scr_dir, 'nexrad')
    if os.path.lexists(radar_dir):
        os.remove(radar_dir)
    os.symlink(config.remapped_radar_dir, radar_dir)
except:
    print("Linking remapped radar files failed!")

# Copy some miscellaneous files
print("Copying miscellaneous auxilliary files...")
shutil.copy(config.radflag_path, config.exp_scr_dir)
shutil.copy(config.blacklist_file_path, config.exp_scr_dir)
shutil.copy(config.template_base_dir + '/startup_anaconda', config.exp_scr_dir)
shutil.copy(config.radarinfo_path, config.exp_scr_dir)

# Finally copy the run_real_data_case.py and run_real_data_case.csh scripts
print("Copying run scripts...")

shutil.copy(os.path.join(config.template_base_dir, 'run_real_data_case.py'), config.exp_scr_dir)
run_real_data_case_shell_scripts = glob.glob(config.template_exp_dir + '/run_real_data_case*sh')
for run_script in run_real_data_case_shell_scripts:
    shutil.copy(run_script, config.exp_scr_dir)

print("Successfully set up experiment working directory for {}".format(config.exp_name))
print("Just wanted to let you know: Good luck, we're all counting on you!")
