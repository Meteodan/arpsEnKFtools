#!/bin/bash
# TODO: make this into a python script, too
BASEPATH='/scratch/rice/c/cbelak/Projects/VORTEXSE/simulations/ARPS/2017_IOP4C/EnKF/6km303x303_043017_NAM_CCN1500'
JOBNAME='6km303x303_043017_NAM_CCN1500'

# Force unload xalt module due to python bug
# EDIT: do we need to do this anymore?
module --force unload xalt
# Startup anaconda environment
. /depot/dawson29/etc/startup_anaconda
conda activate arpsEnKFtools

# 6-km 30 April 2017 surface data only

# Initial 6-hr spinup from 0600-1200 UTC 30 April 2017
python run_real_data_case.py  \
    --base-path $BASEPATH  --job-name $JOBNAME --user cbelak                                        \
    --n-ens 40  --mpi-config-model 10 6 --mpi-config-dump 10 6 --mpi-config-enkf 10 6 --algorithm ensrf                                                                        \
    --ens-start 0  --ens-end 21600  --ens-step 300  --assim-step 21600  --chunk-size 21600                                   \
    --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
    --assim-radar no  --assim-prof no  --assim-surf yes  --assim-sndg no                                                    \
    --covariance-inflation 0:mults=1.20,adapt=0.90 \
    --fcst-req 0:45  --init-fcst-req 2:15  --assim-on-req 0:45                                                              \
    --split-init auto --debug --save-batch --error-check 

# every 15 minutes from 12 UTC to 23 UTC
#python run_real_data_case.py  \
#     --base-path $BASEPATH  --job-name $JOBNAME  --user cbelak                                      \
#     --n-ens 40  --mpi-config-model 10 6 --mpi-config-dump 10 6 --mpi-config-enkf 10 6 --algorithm ensrf                                                                        \
#     --ens-start 21600  --ens-end 61200  --ens-step 300  --assim-step 900  --chunk-size 900                                   \
#     --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
#     --assim-radar no  --assim-prof no  --assim-surf yes  --assim-sndg no                                                    \
#     --covariance-inflation 0:mults=1.20,adapt=0.90 \
#     --fcst-req 0:45  --init-fcst-req 2:15  --assim-on-req 0:45                                                              \
#     --split-init auto --debug --save-batch --error-check --restart
