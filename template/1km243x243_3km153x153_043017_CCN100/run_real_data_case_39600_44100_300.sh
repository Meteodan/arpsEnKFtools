#!/bin/bash
# TODO: make this into a python script, too
BASEPATH='/scratch/rice/c/cbelak/Projects/VORTEXSE/simulations/ARPS/2017_IOP4C/EnKF/1km243x243_3km153x153_043017_CCN100/'
JOBNAME='5_min_CCN_100_1km243x243_3km153x153_043017_NAM'

# Force unload xalt module due to python bug
# EDIT: do we need to do this anymore?
module --force unload xalt
# Startup anaconda environment
. ./startup_anaconda
conda activate arpsEnKFtools

# 3-km 30 April 2017 radar data
# 5-min cycle assimilating radar obs from 1700-1815 UTC 30 April 2017 with 5 minute output and Z_updtime.uv set to 75000
python run_real_data_case.py  \
    --restart --base-path $BASEPATH  --job-name $JOBNAME --user cbelak                                        \
    --n-ens 40  --mpi-config-model 6 6 --mpi-config-dump 6 6 --mpi-config-enkf 6 6 --algorithm ensrf                                                                        \
    --ens-start 40500  --ens-end 44100  --ens-step 300  --assim-step 300  --chunk-size 300                                   \
    --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf_5.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
    --assim-radar 2017_IOP4C.radflag  --assim-prof no  --assim-surf no  --assim-sndg no                                                    \
    --covariance-inflation 0:mults=1.20,adapt=0.90 \
    --fcst-req 0:15  --init-fcst-req 0:15  --assim-on-req 1:30 --init-time-string 20170430060000 --check-radar-files                                                             \
    --split-init auto --debug --save-batch --error-check --initial-conditions yes --ppn 18 --save-lookup
