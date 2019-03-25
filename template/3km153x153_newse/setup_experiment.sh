#!/bin/bash

# Define needed directories, files, etc.
SCRATCHBASE="/scratch/rice/d/dawson29/"
DEPOTBASE="/depot/dawson29/"
BASEDIR="${SCRATCHBASE}VORTEXSE/simulations/ARPS/2016_IOP3/EnKF/"
RUNNAME="3km153x153_newse"
TEMPLATEDIR="${DEPOTBASE}apps/arpsEnKFtools/template/"
SFCDATA="${DEPOTBASE}data/VORTEXSE/simulations/ARPS/sfcdata/3km153x153.sfcdata"
TRNDATA="${DEPOTBASE}data/VORTEXSE/simulations/ARPS/trndata/3km153x153.trndata"
BOUNDARYDIR="${DEPOTBASE}data/VORTEXSE/simulations/ARPS/2016_IOP3/EnKF/3km153x153_newseicbc/"
RADARDIR="${DEPOTBASE}data/VORTEXSE/simulations/ARPS/2016_IOP3/processed_radar/"
SCATTDIR="/home/dawson29/arps5.4_main/data/scatt/"
ARPSEXE="/home/dawson29/arps5.4_main/bin/arps_mpi"
ARPSENKFICEXE="/home/dawson29/arps5.4_main/bin/arpsenkfic"
ARPSENKFEXE="/home/dawson29/arps5.4_main/bin/arpsenkf_mpi"
RADFLAG="2016_IOP3.radflag"
PERTURBIC=0
INIFILE="3km033116NAM107x107bgandbc.hdf010800"
INIBASE="3km033116NAM107x107bgandbc.hdfgrdbas"


#Create base experiment directory and change directories to it
EXPDIR=${BASEDIR}${RUNNAME}
mkdir -p ${EXPDIR} || exit 1
cd ${EXPDIR}

#Copy/link in needed files and directories
ln -sf ${SFCDATA} .
ln -sf ${TRNDATA} .
ln -sf ${BOUNDARYDIR} boundary
if [ "${PERTURBIC}" -eq 1 ]
then
  ln -sf boundary/${INIBASE} .
  ln -sf boundary/${INIFILE} .
fi
ln -sf ${ARPSEXE} arps
ln -sf ${ARPSENKFICEXE} arpsenkfic
ln -sf ${ARPSENKFEXE} arpsenkf
ln -sf ${RADARDIR} nexrad
ln -sf ${SCATTDIR} scatt
cp ${TEMPLATEDIR}/run_real_data_case.py .
cp ${TEMPLATEDIR}/run_real_data_case.csh .
cp ${TEMPLATEDIR}/${RADFLAG} .
mkdir -p inputfiletemplates
cp ${TEMPLATEDIR}/arps.input inputfiletemplates/
cp ${TEMPLATEDIR}/arpsenkfic.input inputfiletemplates/
cp ${TEMPLATEDIR}/arpsenkf.input inputfiletemplates/