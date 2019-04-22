# This script links lookup tables for rfopt=3 so that MPI jobs will read in the file properly
# for each processor

import os

# Absolute path to directory where lookup tables reside
basedir = "/depot/dawson29/data/Projects/VORTEXSE/simulations/ARPS/2016_IOP3/EnKF/scatt_1km453x453/S-band/"
category_names = ['RAIN', 'RIME']
moment_names = ['Zh', 'Zhv', 'Zv', 'k']
density_list = range(100, 1000, 100)
nproc_x = 15
nproc_y = 6

# Construct the list of target lookup table file names
target_filenames_by_category = []
for category in category_names:
    if category in 'RIME':
        filenames = ["{}_rho{:04d}.hdf{}000000".format(category, density, moment_name)
                     for density in density_list for moment_name in moment_names]
    else:
        filenames = ["{}.hdf{}000000".format(category, moment_name)
                     for moment_name in moment_names]
    target_filenames_by_category.append(filenames)

# Generate the link names to the targets and make the links
for target_filenames in target_filenames_by_category:
    for target_filename in target_filenames:
        file_link_names = ["{}_{:03d}{:03d}".format(target_filename, proc_x, proc_y)
                           for proc_x in range(1, nproc_x + 1) for proc_y in range(1, nproc_y + 1)]
        for file_link in file_link_names:
            cmd = "ln -sf {} {}".format(os.path.join(basedir, target_filename),
                                        os.path.join(basedir, file_link))
            print(cmd)
            os.system(cmd)
