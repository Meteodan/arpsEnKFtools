#!/bin/bash
# TODO: make this into a python script, too
BASEPATH='/scratch/rice/d/dawson29/Projects/VORTEXSE/simulations/ARPS/2016_IOP3/EnKF/1km453x453_033116_newse/'
JOBNAME='1km453x453_033116_newse'

# 1km 31 March 2016 (nested in NEWS-e), radar data at 15-min intervals
# Initial 1-hr spinup (1800-1900 UTC)
python run_real_data_case.py  \
    --base-path $BASEPATH  --job-name $JOBNAME --user dawson29                                    \
    --n-ens 36  --mpi-config-model 15 6 --mpi-config-dump 15 6 --mpi-config-enkf 15 6 --algorithm ensrf                                                                        \
    --ens-start 0 --ens-end 3600 --ens-step 300  --assim-step 3600  --chunk-size 3600                                   \
    --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
    --assim-radar 2016_IOP3.radflag  --initial-conditions yes --assim-prof no  --assim-surf no  --assim-sndg no                                                    \
    --covariance-inflation 0:mults=1.20,adapt=0.90 \
    --fcst-req 0:30  --init-fcst-req 0:30  --assim-on-req 2:00                                                              \
    --split-init auto --debug --save-batch --error-check --ppn 15 --save-lookup

# Then assimilate every 15 min from 1900 to 0245 UTC
python run_real_data_case.py  \
    --base-path $BASEPATH  --job-name $JOBNAME --user dawson29                                    \
    --n-ens 36  --mpi-config-model 15 6 --mpi-config-dump 15 6 --mpi-config-enkf 15 6 --algorithm ensrf                                                                        \
    --ens-start 3600 --ens-end 31500 --ens-step 300  --assim-step 900  --chunk-size 900                                   \
    --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
    --assim-radar 2016_IOP3.radflag  --initial-conditions yes --assim-prof no  --assim-surf no  --assim-sndg no                                                    \
    --covariance-inflation 0:mults=1.20,adapt=0.90 \
    --fcst-req 0:30  --init-fcst-req 0:30  --assim-on-req 2:00                                                              \
    --split-init auto --debug --save-batch --error-check --ppn 15 --restart