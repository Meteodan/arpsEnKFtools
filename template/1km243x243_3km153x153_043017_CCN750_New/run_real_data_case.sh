#!/bin/bash
# TODO: make this into a python script, too
BASEPATH='/scratch/rice/c/cbelak/Projects/VORTEXSE/simulations/ARPS/2017_IOP4C/EnKF/1km243x243_3km153x153_043017_CCN750_New/'
JOBNAME='CCN_750_1km243x243_3km153x153_043017_NAM'

# Force unload xalt module due to python bug
# EDIT: do we need to do this anymore?
module --force unload xalt
# Startup anaconda environment
module use /depot/dawson29/etc/modules
module load arpsEnKFtools

# 3-km 30 April 2017 radar data
# 15-min cycle assimilating radar obs from 1700-2200 UTC 30 April 2017
python run_real_data_case.py  \
    --base-path $BASEPATH  --job-name $JOBNAME --user cbelak                                        \
    --n-ens 40  --mpi-config-model 6 6 --mpi-config-dump 6 6 --mpi-config-enkf 6 6 --algorithm ensrf                                                                        \
    --ens-start 28800  --ens-end 36000  --ens-step 300  --assim-step 7200  --chunk-size 7200                                   \
    --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
    --assim-radar 2017_IOP4C.radflag  --assim-prof no  --assim-surf yes  --assim-sndg no                                                    \
    --covariance-inflation 0:multd=1.05,mults=1.20,adapt=0.90 \
    --fcst-req 0:08  --init-fcst-req 2:00  --assim-on-req 1:15 --init-time-string 20170430060000 --check-radar-files                                                             \
    --split-init auto --debug --save-batch --error-check --initial-conditions yes --ppn 18 --save-lookup
