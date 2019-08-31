#!/bin/csh

conda activate arpsEnKFtools

python run_real_data_case.py  \
    --base-path /scratch/rice/s/sharm261/2013_0519_EnKF/3km153x153_OK/  --job-name 3km153x153_OK --user-name sharm261  \
    --n-ens 40  --mpi-config-model 3 5 --mpi-config-dump 3 5 --mpi-config-enkf 3 5 --algorithm ensrf  \
    --ens-start 0 --ens-end 7200 --ens-step 300  --assim-step 7200  --chunk-size 7200  \
    --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input  \
    --assim-radar 2013_0519.radflag  --assim-prof no  --assim-surf no  --assim-sndg no                                                    \
    --covariance-inflation 0:multd=1.05 \
    --fcst-req 0:20  --init-fcst-req 4:00  --assim-on-req 0:45                                                              \
    --split-init auto --debug --save-batch --ppn 15 --error-check
