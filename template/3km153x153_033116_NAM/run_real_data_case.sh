#!/bin/bash
# TODO: make this into a python script, too
BASEPATH='/scratch/rice/s/sharm261/Projects/033116_AL/ARPS/2016_IOP3/EnKF/3km153x153_033116_NAM/'
JOBNAME='3km153x153_033116_NAM'

# Force unload xalt module due to python bug
# EDIT: do we need to do this anymore?
module --force unload xalt
# Startup anaconda environment
. ./startup_anaconda
conda activate arpsEnKFtools

# 3km 31 March 2016 (NAM), radar data at 15-min intervals
# Initial 1hr 45 min spinup (1800-1945 UTC)

python run_real_data_case.py  \
    --base-path $BASEPATH  --job-name $JOBNAME --user-name sharm261                                       \
    --n-ens 40  --mpi-config-model 3 5 --mpi-config-dump 3 5 --mpi-config-enkf 3 5 --algorithm ensrf                                                                        \
    --ens-start 0 --ens-end 6300  --ens-step 300  --assim-step 6300  --chunk-size 6300                                   \
    --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
    --assim-radar no  --assim-prof no  --assim-surf yes  --assim-sndg no                                                    \
    --covariance-inflation 0:mults=1.20,adapt=0.90 \
    --fcst-req 0:45  --init-fcst-req 1:15 --assim-on-req 0:45                                                              \
    --split-init auto --debug --save-batch --error-check --save-lookup

# Then, 15-min cycle assimilating radar obs until 0200 UTC 13 May 2013
python run_real_data_case.py  \
    --base-path $BASEPATH  --job-name $JOBNAME --user-name sharm261                                        \
    --n-ens 40  --mpi-config-model 3 5 --mpi-config-dump 3 5 --mpi-config-enkf 3 5 --algorithm ensrf                                                                        \
    --ens-start 6300  --ens-end 28800  --ens-step 300  --assim-step 900  --chunk-size 900                                   \
    --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
    --assim-radar 2016_IOP3.radflag  --assim-prof no  --assim-surf yes  --assim-sndg no                                                    \
    --covariance-inflation 0:mults=1.20,adapt=0.90 \
    --fcst-req 0:45  --init-fcst-req 1:15  --assim-on-req 0:45                                                              \
    --split-init auto --debug --save-batch --error-check --restart

