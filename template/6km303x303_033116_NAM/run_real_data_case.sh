#!/bin/bash
# TODO: make this into a python script, too
BASEPATH='/scratch/rice/s/sbeverid/Projects/VORTEXSE/simulations/ARPS/2016_IOP3/EnKF/6km303x303_033116_NAM/'
JOBNAME='6km303x303_033116_NAM'

# Force unload xalt module due to python bug
# EDIT: do we need to do this anymore?
module --force unload xalt
# Startup anaconda environment
. /depot/dawson29/etc/startup_anaconda
conda activate arpsEnKFtools

# 6-km 31 March 2016 surface data only

# Initial 6-hr spinup from 1200-1800 UTC 31 March 2016
python run_real_data_case.py  \
    --base-path $BASEPATH  --job-name $JOBNAME --user sbeverid --queue-name standby                                       \
    --restart --n-ens 40  --mpi-config-model 10 6 --mpi-config-dump 10 6 --mpi-config-enkf 10 6 --algorithm ensrf                                                                        \
    --ens-start 0  --ens-end 21600  --ens-step 300  --assim-step 21600  --chunk-size 21600                                   \
    --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
    --assim-radar no  --assim-prof no  --assim-surf yes  --assim-sndg no                                                    \
    --covariance-inflation 0:mults=1.20,adapt=0.90 \
    --fcst-req 0:45  --init-fcst-req 2:45  --assim-on-req 0:45                                                              \
    --split-init auto --debug --save-batch --error-check

# every 15 minutes from 1800 UTC to 0300 UTC
#python run_real_data_case.py  \
#     --base-path $BASEPATH  --job-name $JOBNAME  --user sbeverid                                      \
#     --restart --n-ens 40  --mpi-config-model 10 6 --mpi-config-dump 10 6 --mpi-config-enkf 10 6 --algorithm ensrf                                                                        \
#     --ens-start 53100  --ens-end 54000  --ens-step 300  --assim-step 900  --chunk-size 900                                   \
#     --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
#     --assim-radar no  --assim-prof no  --assim-surf yes  --assim-sndg no                                                    \
#     --covariance-inflation 0:mults=1.20,adapt=0.90 \
#     --fcst-req 0:45  --init-fcst-req 2:45  --assim-on-req 0:45                                                              \
#     --split-init auto --debug --save-batch --error-check --restart
