#!/bin/bash
# TODO: make this into a python script, too
BASEPATH='/scratch/rice/s/sbeverid/Projects/VORTEXSE/simulations/ARPS/2016_IOP3/EnKF/1km243x243_3km153x153_6km303x303_033116_NAM'
JOBNAME='1km243x243_3km153x153_6km303x303_033116_NAM'

# Force unload xalt module due to python bug
# EDIT: do we need to do this anymore?
module --force unload xalt
# Startup anaconda environment
module use /depot/dawson29/etc/modules
module load arpsEnKFtools

# 3-km 30 April 2017 radar data
# 15-min cycle assimilating radar obs from 1700-2200 UTC 30 April 2017
python run_real_data_case.py  \
    --base-path $BASEPATH  --job-name $JOBNAME --user sbeverid                                        \
    --n-ens 40  --mpi-config-model 6 6 --mpi-config-dump 6 6 --mpi-config-enkf 6 6 --algorithm ensrf                                                                        \
    --ens-start 21600  --ens-end 54000  --ens-step 300  --assim-step 300  --chunk-size 300                                   \
    --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
    --assim-radar 2016_IOP3.radflag  --assim-prof no  --assim-surf no  --assim-sndg no                                                    \
    --covariance-inflation 0:mults=1.20,adapt=0.90 \
    --fcst-req 0:30  --init-fcst-req 1:15  --assim-on-req 1:30                                                              \
    --split-init auto --debug --save-batch --error-check --initial-conditions yes --save-lookup
