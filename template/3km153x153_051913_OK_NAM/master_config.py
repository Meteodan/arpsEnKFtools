"""
master_config.py -- Contains parameters to configure an end-to-end ARPS-EnKF run
"""
import os
from datetime import datetime

# Define needed directories and experiment names/tags
# Base project names and directories
scratch_base_dir = '/scratch/rice/d/dawson29'
depot_base_dir = '/depot/dawson29'
arpsenkftools_base_dir = os.path.join(depot_base_dir, 'apps/Projects/arpsEnKFtools')
project_dir = 'Projects/051913_OK/ARPS'  # Note, removed redundant "simulations" subdirectory here
project_scr_dir = os.path.join(scratch_base_dir, project_dir)
project_depot_dir = os.path.join(depot_base_dir, 'data', project_dir)
IOP_name = ''  # Not needed for this experiment
IOP_scr_dir = os.path.join(project_scr_dir, IOP_name, 'EnKF')
IOP_depot_dir = os.path.join(project_depot_dir, IOP_name, 'EnKF')
prep_work_dir = os.path.join(IOP_scr_dir, 'prep_work')
ext_model_data_dir = os.path.join(depot_base_dir, 'data/Projects/051913_OK/model_data/NAM',
                                  IOP_name)
sfc_obs_dir = os.path.join(depot_base_dir, 'data/Projects/051913_OK/obsdata/sao')
radar_obs_dir = os.path.join(depot_base_dir, 'data/Projects/051913_OK/obsdata/nexrad/')
# TODO: add other obs type directories here

# Experiment name and directories
exp_name_base = '3km153x153_051913_OK'
exp_name_tag = '_NAM'
exp_name = exp_name_base + exp_name_tag
exp_scr_dir = os.path.join(IOP_scr_dir, exp_name)
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
radflag_file = '2013_0519.radflag'
radflag_path = os.path.join(template_exp_dir, radflag_file)
radarinfo_file = 'radarinfo.dat'
radarinfo_path = os.path.join(template_base_dir, radarinfo_file)
blacklist_file = 'blacklist.sfc'
blacklist_file_path = os.path.join(template_exp_dir, blacklist_file)
remapped_radar_dir = os.path.join(project_depot_dir, 'remapped_radar/{}'.format(exp_name))

# Executable file names and directories
arps_base_dir = '/home/dawson29/arps5.4_main'
arps_bin_dir = os.path.join(arps_base_dir, 'bin')
arpstrn_exe_path = os.path.join(arps_bin_dir, 'arpstrn')
arpssfc_exe_path = os.path.join(arps_bin_dir, 'arpssfc')
ext2arps_exe_path = os.path.join(arps_bin_dir, 'ext2arps')
arps_exe_path = os.path.join(arps_bin_dir, 'arps_mpi')
arpsenkf_exe_path = os.path.join(arps_bin_dir, 'arpsenkf_mpi')
arpsenkfic_exe_path = os.path.join(arps_bin_dir, 'arpsenkfic')
wrf2arps_exe_path = os.path.join(arps_bin_dir, 'wrf2arps_mpi')
arpsintrp_exe_path = os.path.join(arps_bin_dir, 'arpsintrp_mpi')
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
initial_time = '201305191900'
initial_datetime = datetime.strptime(initial_time, '%Y%m%d%H%M')
# Initial time in seconds from model start corresponding to initial_time (can be different from 0
# if ext2arps/wrf2arps/arpsintrp is run to produce IC's for several different times)
initial_time_sec = 0
perturb_ic = False
external_inifile = '{}.hdf{:06d}'.format(exp_name, initial_time_sec)
external_inigbf = '{}.hdfgrdbas'.format(exp_name)
external_inifile_path = os.path.join(external_icbc_dir, external_inifile)
external_inigbf_path = os.path.join(external_icbc_dir, external_inigbf)

# ARPS comment_lines namelist parameters
nocmnt = 2
comments = ['ARPS 5.4', 'May 19th, 2013 OK outbreak']

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
    'ctrlat': 35.3331,
    'ctrlon': -97.2775,
    'mapproj': 2,
    'trulat1': 33.0,
    'trulat2': 36.0,
    'trulon': -97.2275
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
    'terndmp': 3
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

# STOPPED HERE!

# WRF2ARPS parameters
wrf2arps_param = {
    'run_mpi': True,
    'batch': True,
    'history_interval_sec': 600,
    'history_interval': '00_00:10:00',
    'init_timestamp': initial_time,
    'end_timestamp': '2013052000',
    'subdir_template': 'wrf-s4ekm{:02d}',
    'dmp_out_joined': 1111111,
    'wrfexttrnopt': 3,
    'terndta': trndata_path,
    'ternfmt': 3,
    'extntmrg': 7,
    'dirname': external_icbc_dir
}

# ARPSINTRP parameters
arpsintrp_param = {
}

# Radar remapper parameters
radremap_param = {
    'radar_list': ['KTLX'],
    'start_timestamp': '20130519194500',
    'end_timestamp': '20130520020000',
    'interval_seconds': 300,
    'tolerance': 300
}

# EXT2ARPS parameters
ext2arps_param = {
    'initime': initial_datetime.strftime('%Y-%m-%d.%H:%M:00'),
    'tstart': float(initial_time_sec),
    'tstop': float(initial_time_sec),
    'dmp_out_joined': 1,
    'hdmpfmt': 3,
    'hdfcompr': 2,
    'exbcdmp': 3,
    'exbchdfcompr': 2,
    'extdadmp': 1,
    'qcexout': 1,
    'qrexout': 1,
    'qiexout': 1,
    'qsexout': 1,
    'qhexout': 1,
    'qgexout': 1,
    'nqexout': 1,
    'zqexout': 1,
    'dirname': external_icbc_dir,
    'ternopt': 2,
    'terndta': trndata_path,
    'ternfmt': 3,
    'extdopt': 116,
    'extdfmt': 3,
    'dir_extd': ext_model_data_dir,
    'extdname': 'nam_218',
    'nextdfil': 22,
    # Note, for now explicitly list each time string here. We can work on a more
    # compact solution later
    'extdtimes': [
        '2013-05-19.06:00:00+000:00:00',
        '2013-05-19.06:00:00+001:00:00',
        '2013-05-19.06:00:00+002:00:00',
        '2013-05-19.06:00:00+003:00:00',
        '2013-05-19.06:00:00+004:00:00',
        '2013-05-19.06:00:00+005:00:00',
        '2013-05-19.12:00:00+000:00:00',
        '2013-05-19.12:00:00+001:00:00',
        '2013-05-19.12:00:00+002:00:00',
        '2013-05-19.12:00:00+003:00:00',
        '2013-05-19.12:00:00+004:00:00',
        '2013-05-19.12:00:00+005:00:00',
        '2013-05-19.18:00:00+000:00:00',
        '2013-05-19.18:00:00+001:00:00',
        '2013-05-19.18:00:00+002:00:00',
        '2013-05-19.18:00:00+003:00:00',
        '2013-05-19.18:00:00+004:00:00',
        '2013-05-19.18:00:00+005:00:00',
        '2013-05-20.00:00:00+000:00:00',
        '2013-05-20.00:00:00+001:00:00',
        '2013-05-20.00:00:00+002:00:00',
        '2013-05-20.00:00:00+003:00:00'
    ],
    'iorder': 3,
    'intropt': 1,
    'nsmooth': 1,
    'exttrnopt': 2,
    'extntmrg': 12,
    'extsfcopt': 0,
    'ext_lbc': 1,
    'ext_vbc': 1,
    'grdbasopt': 1
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
    'tintvebd': 300.0,
    'ngbrz': 10,
    'brlxhw': 4,
    'cbcdmp': 0.00555556,
    'exbcfmt': 3,
    'tmixopt': 5,
    'trbisotp': 0,
    'tkeopt': 3,
    'trbvimp': 1,
    'cfcm4h': 5.0e-4,
    'cfcm4v': 5.0e-4,
    'cmix_opt': 1,
    'mphyopt': 15,
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
    'iniprtopt': 2,
    'iniprt_ptprt': 2,
    'iniprt_qv': 2,
    'smoothopt': 2,
    'lhor': 36000.0,
    'lver': 7200.0,
    'prtibgn': 3,
    'prtiend': grid_param['nx'] - 2,
    'prtjbgn': 3,
    'prtjend': grid_param['ny'] - 2,
    'prtkbgn': 3,
    'prtkend': grid_param['nz'] - 2,
    'prtibgnu': 3,
    'prtiendu': grid_param['nx'] - 2,
    'prtjbgnv': 3,
    'prtjendv': grid_param['ny'] - 2,
    'prtkbgnw': 3,
    'prtkendw': grid_param['nz'] - 2,
    'r0h_uv': 6000.0,
    'r0v_uv': 3000.0,
    'r0h_w': 6000.0,
    'r0v_w': 3000.0,
    'r0h_ptprt': 6000.0,
    'r0v_ptprt': 3000.0,
    'r0h_pprt': 6000.0,
    'r0v_pprt': 3000.0,
    'r0h_qv': 6000.0,
    'r0v_qv': 3000.0,
    'r0h_qli': 6000.0,
    'r0v_qli': 3000.0,
    'stdu': 2.0,
    'stdv': 2.0,
    'stdw': 0.0,
    'stdptprt': 1.0,
    'stdpprt': 0.0,
    'stdqv': 0.0006,
    'stdqrelative': 0.1,
}


# ARPSENKF parameters.
arpsenkf_param = {
    'nrdrused': 1,
    'radarname': ['KTLX', 'KFDR'],
    'ntwtype': [1, 1],
    'vcpmode': [11, 11],
    'rdrlocopt': [1, 1]
}
