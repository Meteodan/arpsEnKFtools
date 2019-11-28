"""
link_nam.py -- creates softlinks to nam grb files with file names that ext2arps is expecting
"""

import os
import sys
import glob
import subprocess
from arpsenkftools.io_utils import import_all_from

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

target_dir = config.ext_model_data_dir

files = glob.glob(config.ext_model_data_dir + "/nam_218_*")
filenames = [os.path.split(x)[1] for x in files]

datestamps = [x[8:16] for x in filenames]
hours = [x[17:19] for x in filenames]
forecasthours = [x[23:25] for x in filenames]

newfilenames = ['nam_218.'+datestamp+hour+'f'+forecasthour for datestamp, hour, forecasthour in
                zip(datestamps, hours, forecasthours)]

for oldf, newf in zip(files, newfilenames):
    newpath = os.path.join(target_dir, newf)
    subprocess.call(['ln', '-sf', oldf, newpath])
