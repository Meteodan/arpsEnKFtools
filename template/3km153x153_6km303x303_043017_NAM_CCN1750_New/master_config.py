"""
master_config.py -- Contains parameters to configure an end-to-end ARPS-EnKF run
"""
import os
from datetime import datetime

# Define needed directories and experiment names/tags
# Base project names and directories
scratch_base_dir = '/scratch/rice/c/cbelak'
depot_base_dir = '/depot/dawson29'
arpsenkftools_base_dir = '/home/cbelak/arpsEnKFtools'
project_dir = 'Projects/VORTEXSE/simulations/ARPS'
project_scr_dir = os.path.join(scratch_base_dir, project_dir)
project_depot_dir = os.path.join(depot_base_dir, 'data', project_dir)
IOP_name = '2017_IOP4C'
IOP_scr_dir = os.path.join(project_scr_dir, IOP_name, 'EnKF')
IOP_depot_dir = os.path.join(project_depot_dir, IOP_name, 'EnKF')
ext_model_data_dir = os.path.join(IOP_scr_dir, '6km303x303_043017_NAM_CCN1750/CCN1750_6km303x303_043017_NAM/')
sfc_obs_dir = os.path.join(depot_base_dir, 'data/Projects/VORTEXSE/obsdata/2017/sao/IOP4C')
radar_obs_dir = os.path.join(depot_base_dir, 'data/Projects/VORTEXSE/obsdata/2017/NEXRAD/IOP_4C/level2/')
# TODO: add other obs type directories here

# Experiment name and directories
exp_name_base = '3km153x153_6km303x303_043017'
exp_name_tag = '_NAM_CCN1750_New'
exp_name = exp_name_base + exp_name_tag
exp_scr_dir = os.path.join(IOP_scr_dir, exp_name)
prep_work_dir = os.path.join(exp_scr_dir, '{}_prep_work'.format(exp_name))
exp_depot_dir = os.path.join(IOP_depot_dir, exp_name)
template_base_dir = os.path.join(arpsenkftools_base_dir, 'template')
template_exp_dir = os.path.join(template_base_dir, exp_name)
external_icbc_dir = os.path.join(IOP_depot_dir, exp_name+'_icbc')
sfcdata_dir = os.path.join(project_depot_dir, 'sfcdata')
sfcdata_file = '{}.sfcdata'.format(exp_name)
sfcdata_path = os.path.join(sfcdata_dir, sfcdata_file)
trndata_dir = os.path.join(project_depot_dir, 'trndata')
trndata_file = '{}.trndata'.format(exp_name)
trndata_path = os.path.join(trndata_dir, trndata_file)
radflag_file = '2017_IOP4C.radflag'
radflag_path = os.path.join(template_exp_dir, radflag_file)
radarinfo_file = 'radarinfo.dat'
radarinfo_path = os.path.join(template_base_dir, radarinfo_file)
blacklist_file = 'blacklist.sfc'
blacklist_file_path = os.path.join(template_exp_dir, blacklist_file)
remapped_radar_dir = os.path.join(project_depot_dir, '{}/remapped_radar/{}'.format(IOP_name, exp_name))

# Executable file names and directories
arps_base_dir = '/home/cbelak/arps5.4'
arps_bin_dir = os.path.join(arps_base_dir, 'bin')
arpstrn_exe_path = os.path.join(arps_bin_dir, 'arpstrn')
arpssfc_exe_path = os.path.join(arps_bin_dir, 'arpssfc')
ext2arps_exe_path = os.path.join(arps_bin_dir, 'ext2arps')
arps_exe_path = os.path.join(arps_bin_dir, 'arps_mpi')
arpsenkf_exe_path = os.path.join(arps_bin_dir, 'arpsenkf_mpi')
arpsenkfic_exe_path = os.path.join(arps_bin_dir, 'arpsenkfic')
wrf2arps_exe_path = os.path.join(arps_bin_dir, 'wrf2arps_mpi')
arpsintrp_exe_path = os.path.join(arps_bin_dir, 'arpsintrp')
radremap_exe_path = os.path.join(arps_bin_dir, '88d2arps')
mpi_exe = 'mpiexec'
mpi_nproc_flag = '-n'

# Experiment parameters (many of these are namelist parameters that will be inserted in the
# appropriate namelist input files for the various ARPS programs used in an experiment). See the
# documentation in the various namelist input files for details on their meanings.

# Basic experiment parameters
num_ensemble_members = 40
# Initial time of entire experiment. Note, for nested ARPS runs this must be consistent with the
# initial time of the original parent experiment!
initial_time = '201704300600'
initial_datetime = datetime.strptime(initial_time, '%Y%m%d%H%M')
# Initial time in seconds from model start corresponding to initial_time (can be different from 0
# if ext2arps/wrf2arps/arpsintrp is run to produce IC's for several different times)
initial_time_sec = 21600 # 1700 UTC
perturb_ic = False
if perturb_ic:
    external_inifile = '{}.hdf{:06d}'.format(exp_name, initial_time_sec)
    external_inigbf = '{}.hdfgrdbas'.format(exp_name)
else:
    external_inifile = 'ena001.hdf{:06d}'.format(initial_time_sec)
    external_inigbf = 'ena001.hdfgrdbas'
external_inifile_path = os.path.join(external_icbc_dir, external_inifile)
external_inigbf_path = os.path.join(external_icbc_dir, external_inigbf)

# ARPS comment_lines namelist parameters
nocmnt = 2
comments = ['ARPS 5.4', 'April 30th, 2017 VORTEX-SE IOP4C']

# Grid and map projection parameters
grid_param = {
    'nx': 153,
    'ny': 153,
    'nz': 53,
    'nproc_x': 3,
    'nproc_y': 5,
    'dx': 3000.0,
    'dy': 3000.0,
    'dz': 400.0,
    'strhopt': 1,
    'dzmin': 20.0,
    'zrefsfc': 0.0,
    'dlayer1': 0.0,
    'dlayer2': 1.0e5,
    'strhtune': 0.2,
    'zflat': 1.0e5,
    'ctrlat': 34.20,
    'ctrlon': -87.68,
    'mapproj': 2,
    'trulat1': 33.0,
    'trulat2': 36.0,
    'trulon': -87.68,
}

# ARPSTRN parameters (note that this is set to use the 30-s terrain data. Will add hooks
# for the other terrain data source options later)
arpstrn_param = {
    'trndataopt': 3,
    'dir_trndata': os.path.join(depot_base_dir, 'data/arpstopo30.data'),
    'nsmth': 2,
    'lat_sample': 90,
    'lon_sample': 90,
    'trnanxopt': 2,
    'dirname': trndata_dir,
    'terndmp': 3,
    'mapfile(1)': os.path.join(arps_base_dir, 'data/arpsplt/us_state.mapdata'),
    'mapfile(2)': os.path.join(arps_base_dir, 'data/arpsplt/world_us_country.mapdata'),
}

# ARPSSFC parameters
arpssfc_param = {
    'nstyp': 3,
    'sfcdmp': 3,
    'schmopt': 3,
    'sdatopt': 1,
    'fstypfl': os.path.join(depot_base_dir, 'data/arpssfc.data/soil_1km.data'),
    'bstypfl': os.path.join(depot_base_dir, 'data/arpssfc.data/whsoil_1deg.data'),
    'vdatopt': 1,
    'fvtypfl': os.path.join(depot_base_dir, 'data/arpssfc.data/naoge1_01l_1km.img'),
    'bvtypfl': os.path.join(depot_base_dir, 'data/arpssfc.data/owe14d_10min.data'),
    'ndatopt': 1,
    'fndvifl': os.path.join(depot_base_dir, 'data/arpssfc.data/namay92ndl_1km.img'),
    'bndvifl': os.path.join(depot_base_dir, 'data/arpssfc.data/ndvi9005_10min.data'),
    'vfrcopt': 1,
    'vfrcdr': os.path.join(depot_base_dir, 'data/arpssfc.data/'),
    'nsmthsl': 3,
    'stypout': 1,
    'vtypout': 1,
    'laiout': 1,
    'rfnsout': 1,
    'vegout': 1,
    'ndviout': 1,
    'dirname': sfcdata_dir
}

# ARPSINTRP parameters
arpsintrp_param = {
    'nproc_x': 10,
    'nproc_y': 6,
    'nproc_x_in': 10,
    'nproc_y_in': 6,
    'nproc_x_out': 1,
    'nproc_y_out': 1,
    'inisplited': 1,
    'dmp_out_joined': 1111111,
    'dirname': external_icbc_dir,
    'terndta1': trndata_path,
    'xy_or_ll': 2,
    'ctrlat1': grid_param['ctrlat'],
    'ctrlon1': grid_param['ctrlon'],
    'dx1': grid_param['dx'],
    'dy1': grid_param['dy'],
    'dz1': grid_param['dz'],
    'strhopt1': grid_param['strhopt'],
    'dzmin1': grid_param['dzmin'],
    'zrefsfc1': grid_param['zrefsfc'],
    'dlayer11': grid_param['dlayer1'],
    'dlayer21': grid_param['dlayer2'],
    'strhtune1': grid_param['strhtune'],
    'zflat1': grid_param['zflat'],
    'nstyp1': arpssfc_param['nstyp'],
    # Following are not used in the namelist, but by the run_arpsintrp.py program
    # They will be "popped" from the dictionary before it is passed to editNamelistFile
    # They determine the history dumps from the outer ARPS grid that are processed
    'use_mpi': False,
    'start_time': 21600.0,
    'end_time': 57600.0,
    'step_time': 300.0
}

# Radar remapper parameters
radremap_param = {
    'radar_list': ['KBMX', 'KGWX', 'KHTX', 'KNQA', 'KOHX', 'KDGX'],
    'start_timestamp': '20170430120000',
    'end_timestamp': '20170430220000',
    'interval_seconds': 300,
    'tolerance': 900,
    'closest_before': True,
    'nthreads': 10
}

# EXT2ARPS parameters
ext2arps_param = {
}

# ARPS parameters
# Note that these include the comment, grid and map projection parameters already defined above
# Also many of the parameters are shared with EXT2ARPS. So these are ones that are specific
# to just the ARPS forward model component of the workflow. Parameters that aren't likely
# to be changed very often but that are present in the namelist aren't included here, but can be
# added as needed.

arps_param = {
    # Inifile and inigbf are only needed here for the arpsenkfic step. They are changed on the fly
    # during the actual ensemble integration to the appropriate ensemble member names
    'nocmnt': nocmnt,
    'cmnt(1)': comments[0],
    'cmnt(2)': comments[1],
    'runname': exp_name,
    'initime': initial_datetime.strftime('%Y-%m-%d.%H:%M:00'),
    'inifile': './{}'.format(external_inifile),
    'inigbf': './{}'.format(external_inigbf),
    'dtbig': 4.0,
    'tstart': float(initial_time_sec),
    'tstop': float(initial_time_sec),
    'dtsml': 1.0,
    'tintegopt': 1,
    'tintvebd': 300,
    'ngbrz': 10,
    'brlxhw': 4,
    'cbcdmp': 0.05,
    'exbcfmt': 3,
    'tmixopt': 4,
    'trbisotp': 0,
    'tkeopt': 3,
    'trbvimp': 1,
    'cfcm4h': 5.0e-4,
    'cfcm4v': 5.0e-4,
    'cmix_opt': 1,
    'mphyopt': 15,
    'ntcloud': 1.75e9,
    'sfcdtfl': sfcdata_file,
    'sfcfmt': 3,
    'dtsfc': 4.0,
    'hdmpfmt': 103,
    'thisdmp': 300.0,
    'rfopt': 3,
    'sv_lkup_tble': 1
}

# ARPSENKFIC parameters
arpsenkfic_param = {
}

# ARPSENKF parameters.
arpsenkf_param = {
    'nrdrused': 6,
    'radarname': ['KBMX', 'KGWX', 'KHTX', 'KNQA', 'KOHX', 'KDGX'],
    'ntwtype': [1, 1, 1, 1, 1, 1],
    'vcpmode': [11, 11, 11, 11, 11, 11],
    'rdrlocopt': [1, 1, 1, 1, 1, 1]
}
