#!/bin/bash
# TODO: make this into a python script, too
BASEPATH='/scratch/rice/c/cbelak/Projects/VORTEXSE/simulations/ARPS/2017_IOP4C/EnKF/1km243x243_3km153x153_043017_CCN300_New/'
JOBNAME='CCN_300_1km243x243_3km153x153_043017_NAM'

# Force unload xalt module due to python bug
# EDIT: do we need to do this anymore?
module --force unload xalt
# Startup anaconda environment
module use /depot/dawson29/etc/modules
module load arpsEnKFtools

# 1-km 30 April 2017 radar data
# spin up from 1400-1600 UTC
# 5-min cycle assimilating radar data and sfc obs from 1600-2200 UTC 30 April 2017 with radar reflectivity threshold of 0 dBZ
python run_real_data_case.py  \
    --base-path $BASEPATH  --job-name $JOBNAME --user cbelak                                        \
    --n-ens 40  --mpi-config-model 6 6 --mpi-config-dump 6 6 --mpi-config-enkf 6 6 --algorithm ensrf                                                                        \
    --ens-start 28800  --ens-end 36000  --ens-step 300  --assim-step 7200  --chunk-size 7200                                   \
    --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
    --assim-radar 2017_IOP4C.radflag  --assim-prof no  --assim-surf yes  --assim-sndg no                                                    \
    --covariance-inflation 0:multd=1.05,mults=1.20,adapt=0.90 \
    --fcst-req 0:08  --init-fcst-req 1:15  --assim-on-req 1:15 --init-time-string 20170430060000 --check-radar-files                                                             \
    --split-init auto --debug --save-batch --error-check --initial-conditions yes --ppn 18 --save-lookup
