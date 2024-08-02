#!/bin/bash
# TODO: make this into a python script, too
BASEPATH='/scratch/bell/dawson29/Projects/PERiLS/simulations/ARPS/2022_IOP2/EnKF/6km303x303_033022_0600_NAM'
JOBNAME='6km303x303_033022_0600_NAM'

# Force unload xalt module due to python bug
# EDIT: do we need to do this anymore?
module --force unload xalt

# Uncomment the following lines if you want to use the intel stack
module load intel
module unload hdf
export HDF_HOME="/depot/dawson29/apps/libraries/hdf4-4.2.15_bell_intel"

# Startup anaconda environment
. ./startup_anaconda
conda activate arpsEnKFtools

# 6-km 30 Mar 2022 surface data only

# Initial 6-h spinup from 0600 to 1200 UTC 30 March 2022

# python run_real_data_case.py  \
#     --base-path $BASEPATH  --job-name $JOBNAME                                        \
#     --n-ens 40  --mpi-config-model 10 6 --mpi-config-dump 10 6 --mpi-config-enkf 10 6 --algorithm ensrf                                                                        \
#     --ens-start 0  --ens-end 21600  --ens-step 300  --assim-step 21600  --chunk-size 21600                                   \
#     --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
#     --assim-radar no  --assim-prof no  --assim-surf yes  --assim-sndg no                                                    \
#     --covariance-inflation 0:multd=1.05,mults=1.20,adapt=0.90 \
#     --fcst-req 0:45  --init-fcst-req 1:15  --assim-on-req 0:45                                                              \
#     --split-init auto --debug --save-batch --error-check --ppn 64


# 15-min cycle assimilating ASOS 5-min obs from 1200 UTC 31 March 2016 until 0300 UTC 4 Apr 2016
python run_real_data_case.py  \
    --base-path $BASEPATH  --job-name $JOBNAME                                        \
    --n-ens 40  --mpi-config-model 10 6 --mpi-config-dump 10 6 --mpi-config-enkf 10 6 --algorithm ensrf                                                                        \
    --ens-start 21600  --ens-end 75600  --ens-step 300  --assim-step 900  --chunk-size 900                                   \
    --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
    --assim-radar no  --assim-prof no  --assim-surf yes  --assim-sndg no                                                    \
    --covariance-inflation 0:multd=1.05,mults=1.20,adapt=0.90 \
    --fcst-req 0:45  --init-fcst-req 1:15  --assim-on-req 0:45                                                              \
    --split-init auto --debug --save-batch --error-check --ppn 64 --restart
