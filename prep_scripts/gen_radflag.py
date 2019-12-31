"""
This script generates a "radflag" file for use in the EnKF cycle. It reads the "master_config.py"
file from the given experiment template directory.
"""
import sys
import pprint
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

radflag_param = config.radflag_param

# Now generate the 'radar_data_flag' dictionary, where keys are assimilation times and values are
# the radar groups that are to be assimilated for that time. You can also explicitly list the times
# then add the radar_data_flag dictionary to the radflag_param dictionary
# The values take the form {True:[<radar_group>], False:[<radar_group>]}. In practice,
# the "False" key doesn't seem to be used anywhere in the run_real_data_case.py script.
# Actually, the radar names in the radar_groups dict aren't being used either, but only the
# length of the list (to set nrdrused, but we are already setting it above).
# TODO: Ask Tim S. about this; refactor how this is done.

radar_data_flag = {}

for radar_group_name, radar_group in radflag_param['radar_groups'].items():
    radar_data_flag.update({
        assim_time: {True: radar_group[0], False: []} for assim_time in radar_group[1]
    })

with open(config.radflag_path, 'w') as radflag_output:
    output_text = pprint.pformat(radar_data_flag, indent=4)
    radflag_output.write('radar_data_flag = {}'.format(output_text))

