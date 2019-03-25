#!/bin/csh

#### 3km run, ALL THE 88D's!
# python run_real_data_case.py  \
#      --base-path /scratch/01479/tsupine/24May2011/  --job-name 3km-3d-esnd-MPAR-only                                        \
#      --n-ens 40  --mpi-config 2 15  --algorithm ensrf                                                                        \
#      --ens-start 0  --ens-end 10800  --ens-step 3600  --assim-step 3600  --chunk-size 1800                                   \
#      --arps-template arps.3km.input  --arpsenkf-template arpsenkf.3km.input  --arpsenkfic-template arpsenkfic.3km.input      \
#      --assim-radar 3kmelreno.radflag  --assim-prof no  --assim-surf yes                                                      \
#      --covariance-inflation 0:multd=1.05 10800:mults=1.20,adapt=0.90                                                         \
#      --fcst-req 0:25  --init-fcst-req 0:50  --assim-on-req 1:30                                                              \
#      --debug

# 6km 31 March 2016 surface data only

# python run_real_data_case.py  \
#     --base-path /scratch/rice/d/dawson29/VORTEXSE/simulations/ARPS/2016_IOP3/EnKF/6kmconv/  --job-name 6kmconv                                        \
#     --n-ens 40  --mpi-config-model 10 6 --mpi-config-dump 10 6 --mpi-config-enkf 10 6 --algorithm ensrf                                                                        \
#     --ens-start 14400  --ens-end 54000  --ens-step 300  --assim-step 3600  --chunk-size 3600                                   \
#     --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
#     --assim-radar no  --assim-prof no  --assim-surf yes  --assim-sndg no                                                    \
#     --covariance-inflation 0:multd=1.05 \
#     --fcst-req 0:45  --init-fcst-req 1:15  --assim-on-req 0:45                                                              \
#     --split-init auto --restart --debug

# 3km 31 March 2016 (nested in NEWS-e), radar data at 15-min intervals

python run_real_data_case.py  \
    --base-path /scratch/rice/d/dawson29/VORTEXSE/simulations/ARPS/2016_IOP3/EnKF/1km453x453_newse/  --job-name 1km453x453                                        \
    --n-ens 36  --mpi-config-model 15 8 --mpi-config-dump 5 4 --mpi-config-enkf 5 4 --algorithm ensrf                                                                        \
    --ens-start 0 --ens-end 900 --ens-step 300  --assim-step 900  --chunk-size 900                                   \
    --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
    --assim-radar 2016_IOP3.radflag  --initial-conditions yes --assim-prof no  --assim-surf no  --assim-sndg no                                                    \
    --covariance-inflation 0:multd=1.05 \
    --fcst-req 0:30  --init-fcst-req 0:30  --assim-on-req 1:00                                                              \
    --split-init auto --debug --save-batch --restart

# python run_real_data_case.py  \
#     --base-path /scratch/rice/d/dawson29/VORTEXSE/simulations/ARPS/2016_IOP3/EnKF/3km153x153/  --job-name 3km153x153                                        \
#     --n-ens 40  --mpi-config-model 6 5 --mpi-config-dump 6 5 --mpi-config-enkf 6 5 --algorithm ensrf                                                                        \
#     --ens-start 40500  --ens-end 54000  --ens-step 300  --assim-step 900  --chunk-size 900                                   \
#     --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
#     --assim-radar 2016_IOP3.radflag  --initial-conditions yes --assim-prof no  --assim-surf no  --assim-sndg no                                                    \
#     --covariance-inflation 0:multd=1.05 \
#     --fcst-req 0:20  --init-fcst-req 0:20  --assim-on-req 0:45                                                              \
#     --split-init auto --debug --save-batch --restart

#    python run_real_data_case.py  \
#         --base-path /scratch/rice/d/dawson29/may0399/EnKF/0417runs/3kmtest2/  --job-name 3kmtest2                                        \
#         --n-ens 40  --mpi-config 2 2  --algorithm ensrf                                                                        \
#         --ens-start 600  --ens-end 6600  --ens-step 300  --assim-step 300  --chunk-size 6600                                   \
#         --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
#         --assim-radar may0399.radflag  --assim-prof no  --assim-surf no  --assim-sndg no                                                      \
#         --covariance-inflation 0:multd=1.05 10800:mults=1.20,adapt=0.90                                                         \
#         --fcst-req 0:10  --init-fcst-req 0:10  --assim-on-req 0:10                                                              \
#         --join-files --restart --debug

#   python run_real_data_case.py  \
#        --base-path /scratch/rice/d/dawson29/may0399/EnKF/0417runs/3kmtest/  --job-name 3kmtest                                        \
#        --n-ens 40  --mpi-config 2 2  --algorithm ensrf                                                                        \
#        --ens-start 6000  --ens-end 6600  --ens-step 300  --assim-step 300  --chunk-size 6600                                   \
#        --arps-template inputfiletemplates/arps.input  --arpsenkf-template inputfiletemplates/arpsenkf.input  --arpsenkfic-template inputfiletemplates/arpsenkfic.input      \
#        --assim-radar may0399.radflag  --assim-prof no  --assim-surf no  --assim-sndg no                                                      \
#        --covariance-inflation 0:multd=1.05 10800:mults=1.20,adapt=0.90                                                         \
#        --fcst-req 0:10  --init-fcst-req 0:10  --assim-on-req 0:10                                                              \
#        --join-files --restart --debug

# python run_real_data_case.py \
#      --base-path /scratch/rice/d/dawson29/may0399/EnKF/0417runs/3kmtest/  --job-name 3kmtest                               \
#      --n-ens 40  --mpi-config 2 2                                                                     \
#      --ens-start 6600  --ens-end 21600  --ens-step 300  --assim-step 300  --chunk-size 3600           \
#      --arps-template inputfiletemplates/arps.input                                                                    \
#      --free-forecast  --join-files --debug  --restart

#python run_real_data_case.py \
#      --base-path /scratch/01479/tsupine/24May2011/  --job-name 3km-3d-early-MPAR-only                                        \
#      --n-ens 40  --mpi-config 2 15  --algorithm ensrf                                                                        \
#      --ens-start 10800  --ens-end 14400  --ens-step 300  --assim-step 300  --chunk-size 300                                  \
#      --arps-template arps.3km.input  --arpsenkf-template arpsenkf.3km.input  --arpsenkfic-template arpsenkfic.3km.input      \
#      --assim-radar 3kmelreno.radflag  --assim-prof no                                                                        \
#      --covariance-inflation 10800:mults=1.20,adapt=0.90                                                                      \
#      --fcst-req 0:20  --init-fcst-req 0:40  --assim-off-req 1:15  --assim-on-req 1:30                                        \
#      --debug  --restart

#python run_real_data_case.py \
#      --base-path /scratch/01479/tsupine/24May2011/  --job-name 3km-3d-MPAR-only                                              \
#      --n-ens 40  --mpi-config 2 15  --algorithm ensrf                                                                        \
#      --ens-start 14400  --ens-end 18000  --ens-step 300  --assim-step 300  --chunk-size 300                                  \
#      --arps-template arps.3km.input  --arpsenkf-template arpsenkf.3km.input  --arpsenkfic-template arpsenkfic.3km.input      \
#      --assim-radar 3kmelreno.radflag  --assim-prof no                                                                        \
#      --covariance-inflation 10800:mults=1.20,adapt=0.90                                                                      \
#      --fcst-req 0:20  --init-fcst-req 0:40  --assim-off-req 1:15  --assim-on-req 1:30                                        \
#      --debug  --restart

#### 3km forecasts
#python run_real_data_case.py \
#     --base-path /lustre/scratch/tsupinie/24May2011/  --job-name 3km-88d                               \
#     --n-ens 40  --mpi-config 2 15                                                                     \
#     --ens-start 10800  --ens-end 14400  --ens-step 300  --assim-step 300  --chunk-size 1800           \
#     --arps-template arps.3km.input                                                                    \
#     --free-forecast  --debug  --restart
