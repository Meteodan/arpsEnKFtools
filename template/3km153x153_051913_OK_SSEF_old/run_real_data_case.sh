#!/bin/bash
# TODO: make this into a python script, too
BASEPATH='/scratch/rice/d/dawson29/Projects/051913_OK/ARPS/EnKF/3km153x153_6km153x153_051913_OK_NAM/'
JOBNAME='3km153x153_6km153x153_051913_OK_NAM'

# Force unload xalt module due to python bug
# EDIT: do we need to do this anymore?
module --force unload xalt
# Startup anaconda environment
. ./startup_anaconda
conda activate arpsEnKFtools

# 3-km 19 May 2013 radar data

# Initial 105-min spinup from 1800-1945 UTC 19 May 2013
python run_real_data_case.py  \
    --base-path $BASEPATH  --job-name $JOBNAME                                        \
    --n-ens 40  --mpi-config-model 3 5 --mpi-config-dump 3 5 --mpi-config-enkf 3 5 --algorithm ensrf                                                                        \
    --ens-start 43200 --ens-end 49500  --ens-step 300  --assim-step 6300  --chunk-size 6300                                   \
    --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
    --assim-radar 2013_0519.radflag  --assim-prof no  --assim-surf no  --assim-sndg no                                                    \
    --covariance-inflation 0:mults=1.20,adapt=0.90 \
    --fcst-req 0:45  --init-fcst-req 1:15  --assim-on-req 0:45                                                              \
    --split-init auto --debug --save-batch --error-check --initial-conditions yes --save-lookup

# Then, 15-min cycle assimilating radar obs until 0200 UTC 13 May 2013
python run_real_data_case.py  \
    --base-path $BASEPATH  --job-name $JOBNAME                                        \
    --n-ens 40  --mpi-config-model 3 5 --mpi-config-dump 3 5 --mpi-config-enkf 3 5 --algorithm ensrf                                                                        \
    --ens-start 49500  --ens-end 72000  --ens-step 300  --assim-step 900  --chunk-size 900                                   \
    --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
    --assim-radar 2013_0519.radflag  --assim-prof no  --assim-surf no  --assim-sndg no                                                    \
    --covariance-inflation 0:mults=1.20,adapt=0.90 \
    --fcst-req 0:45  --init-fcst-req 1:15  --assim-on-req 0:45                                                              \
    --split-init auto --debug --save-batch --error-check --restart