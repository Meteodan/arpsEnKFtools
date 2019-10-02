# link_nam.py -- creates softlinks to nam grb files with file names that ext2arps is expecting

import os
import glob
import subprocess

model_data_dir = '/depot/dawson29/data/Projects/VORTEXSE/model_data/nam_data/2017_IOP4C'

files = glob.glob(datadir+"/nam_218_*")
filenames = [os.path.split(x)[1] for x in files]

print(filenames)