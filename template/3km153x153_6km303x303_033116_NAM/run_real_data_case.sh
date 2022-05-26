#!/bin/bash
# TODO: make this into a python script, too
BASEPATH='/scratch/bell/dawson29/Projects/VORTEXSE/simulations/ARPS/2016_IOP3/EnKF/3km153x153_6km303x303_033116_NAM/'
JOBNAME='3km153x153_6km303x303_033116_NAM'

# Force unload xalt module due to python bug
# EDIT: do we need to do this anymore?
module --force unload xalt
# Startup anaconda environment
. ./startup_anaconda
conda activate arpsEnKFtools

# 3-km 31 March 2016
# 15-min cycle assimilating radar obs from 1200 31 March 2016 to 0300 UTC 1 April 2016
python run_real_data_case.py  \
    --base-path $BASEPATH  --job-name $JOBNAME --user dawson29                                        \
    --n-ens 40  --mpi-config-model 3 5 --mpi-config-dump 3 5 --mpi-config-enkf 3 5 --algorithm ensrf                                                                        \
    --ens-start 21600  --ens-end 75600  --ens-step 300  --assim-step 900  --chunk-size 900                                   \
    --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
    --assim-radar 2016_IOP3.radflag  --assim-prof no  --assim-surf no  --assim-sndg no                                                    \
    --covariance-inflation 0:mults=1.20,adapt=0.90 \
    --fcst-req 0:45  --init-fcst-req 1:15  --assim-on-req 0:45                                                              \
    --split-init auto --debug --save-batch --error-check --initial-conditions yes --save-lookup
