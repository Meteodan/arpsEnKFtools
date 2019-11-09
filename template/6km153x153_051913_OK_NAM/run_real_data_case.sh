#!/bin/bash
# TODO: make this into a python script, too
BASEPATH='/scratch/rice/d/dawson29/Projects/051913_OK/ARPS/EnKF/6km153x153_051913_OK_NAM'
JOBNAME='6km153x153_051913_OK_NAM'

# Force unload xalt module due to python bug
# EDIT: do we need to do this anymore?
module --force unload xalt
# Startup anaconda environment
. ./startup_anaconda
conda activate arpsEnKFtools

# 6-km 19 May 2013 surface data only

# Initial 6-hr spinup from 0600-1200 UTC 19 May 2013
# 5-member ensemble just for testing
python run_real_data_case.py  \
    --base-path $BASEPATH  --job-name $JOBNAME                                        \
    --n-ens 5  --mpi-config-model 3 5 --mpi-config-dump 3 5 --mpi-config-enkf 3 5 --algorithm ensrf                                                                        \
    --ens-start 0  --ens-end 21600  --ens-step 300  --assim-step 21600  --chunk-size 21600                                   \
    --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
    --assim-radar no  --assim-prof no  --assim-surf yes  --assim-sndg no                                                    \
    --covariance-inflation 0:mults=1.20,adapt=0.90 \
    --fcst-req 0:45  --init-fcst-req 1:15  --assim-on-req 0:45                                                              \
    --split-init auto --debug --save-batch --error-check
