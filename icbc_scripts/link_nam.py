# link_nam.py -- creates softlinks to nam grb files with file names that ext2arps is expecting

import os
import glob
import subprocess

model_data_dir = '/depot/dawson29/data/Projects/VORTEXSE/model_data/nam_data/2017_IOP4C'
target_dir = model_data_dir

files = glob.glob(model_data_dir + "/nam_218_*")
filenames = [os.path.split(x)[1] for x in files]

datestamps = [x[8:16] for x in filenames]
hours = [x[17:19] for x in filenames]
forecasthours = [x[23:25] for x in filenames]

newfilenames = ['nam_218.'+datestamp+hour+'f'+forecasthour for datestamp, hour, forecasthour in
                zip(datestamps, hours, forecasthours)]

for oldf, newf in zip(files, newfilenames):
    newpath = os.path.join(target_dir, newf)
    subprocess.call(['ln', '-sf', oldf, newpath])
