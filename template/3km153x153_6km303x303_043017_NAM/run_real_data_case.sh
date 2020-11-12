#!/bin/bash
# TODO: make this into a python script, too
BASEPATH='/scratch/rice/c/cbelak/Projects/VORTEXSE/simulations/ARPS/2017_IOP4C/EnKF/3km153x153_6km303x303_043017_NAM/'
JOBNAME='3km153x153_6km303x303_043017_NAM'

# Force unload xalt module due to python bug
# EDIT: do we need to do this anymore?
module --force unload xalt
# Startup anaconda environment
. ./startup_anaconda
conda activate arpsEnKFtools

# 3-km 30 April 2017 radar data
# 15-min cycle assimilating radar obs from 1700-2200 UTC 30 April 2017
python run_real_data_case.py  \
    --base-path $BASEPATH  --job-name $JOBNAME --user cbelak                                        \
    --n-ens 40  --mpi-config-model 3 5 --mpi-config-dump 3 5 --mpi-config-enkf 3 5 --algorithm ensrf                                                                        \
    --ens-start 39600  --ens-end 57600  --ens-step 300  --assim-step 300  --chunk-size 300                                   \
    --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
    --assim-radar 2017_IOP4C.radflag --assim-prof no  --assim-surf no  --assim-sndg no                                                    \
    --covariance-inflation 0:mults=1.20,adapt=0.90 \
    --fcst-req 0:45  --init-fcst-req 1:15  --assim-on-req 0:45 --init-time-string 20170430060000 --check-radar-files                                                             \
    --split-init auto --debug --save-batch --error-check --initial-conditions yes  --save-lookup
