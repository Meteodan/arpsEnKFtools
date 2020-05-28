#!/bin/bash
# TODO: make this into a python script, too
BASEPATH='/scratch/rice/d/dawson29/Projects/051913_OK/ARPS/EnKF/3km153x153_051913_OK_NAM/'
JOBNAME='3km153x153_051913_OK_NAM'

# Force unload xalt module due to python bug
# EDIT: do we need to do this anymore?
module --force unload xalt
# Startup anaconda environment
. ./startup_anaconda
conda activate arpsEnKFtools

# 3-km 19 May 2013 radar data

# Initial 105-min spinup from 1800-1945 UTC 19 May 2013
python run_real_data_case.py  \
    --base-path $BASEPATH  --job-name $JOBNAME                                       \
    --n-ens 40  --mpi-config-model 3 5 --mpi-config-dump 3 5 --mpi-config-enkf 3 5 --algorithm ensrf                                                                        \
    --ens-start 0 --ens-end 6300  --ens-step 300  --assim-step 6300  --chunk-size 6300                                   \
    --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
    --assim-radar 2013_0519.radflag  --assim-prof no  --assim-surf no  --assim-sndg no                                                    \
    --covariance-inflation 0:mults=1.20,adapt=0.90 \
    --fcst-req 0:30  --init-fcst-req 0:30 --assim-on-req 0:30                                                              \
    --split-init auto --debug --save-batch --error-check --save-lookup

# Then, 15-min cycle assimilating radar obs until 0200 UTC 13 May 2013
python run_real_data_case.py  \
    --base-path $BASEPATH  --job-name $JOBNAME                                        \
    --n-ens 40  --mpi-config-model 3 5 --mpi-config-dump 3 5 --mpi-config-enkf 3 5 --algorithm ensrf                                                                        \
    --ens-start 6300  --ens-end 28800  --ens-step 300  --assim-step 900  --chunk-size 900                                   \
    --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
    --assim-radar 2013_0519.radflag  --assim-prof no  --assim-surf no  --assim-sndg no                                                    \
    --covariance-inflation 0:mults=1.20,adapt=0.90 \
    --fcst-req 0:15  --init-fcst-req 0:15  --assim-on-req 0:30                                                              \
    --split-init auto --debug --save-batch --error-check --restart
