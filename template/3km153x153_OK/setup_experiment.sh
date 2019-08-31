#!/bin/bash

# Define needed directories, files, etc.
SCRATCHBASE="/scratch/rice/s/sharm261/"
DEPOTBASE="/depot/dawson29/"
BASEDIR="${SCRATCHBASE}2013_0519_EnKF/"
RUNNAMEBASE="3km153x153"
RUNNAMETAG="_OK"
RUNNAME=${RUNNAMEBASE}${RUNNAMETAG}
TEMPLATEBASEDIR="/home/sharm261/arpsEnKFtools/template/"
TEMPLATEDIR="${TEMPLATEBASEDIR}${RUNNAME}"
SFCDATA="/home/sharm261/arpsenkf_trial/arpssfc_work/${RUNNAMEBASE}.sfcdata"
TRNDATA="/home/sharm261/arpsenkf_trial/arpstrn_work/${RUNNAMEBASE}.trndata"
BOUNDARYDIR="${DEPOTBASE}data/users/sharm261/3km051913NAM153x153bgandbc/"
RADARDIR="${DEPOTBASE}data/users/sharm261/processed_radar/"
SCATTDIR="${DEPOTBASE}data/users/sharm261/scatt_3km153x153/"
ARPSEXE="/home/sharm261/arps5.4/bin/arps_mpi"
ARPSENKFICEXE="/home/sharm261/arps5.4/bin/arpsenkfic"
ARPSENKFEXE="/home/sharm261/arps5.4/bin/arpsenkf_mpi"
RADFLAG="2013_0519.radflag"
PERTURBIC=1
# The following are only needed when running arpsenkfic
INIFILE="3km051913NAM153x153bgandbc.hdf000000"
INIBASE="3km051913NAM153x153bgandbc.hdfgrdbas"


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
cp ${TEMPLATEBASEDIR}/run_real_data_case.py .
cp ${TEMPLATEDIR}/run_real_data_case.csh .
cp ${TEMPLATEDIR}/${RADFLAG} .
mkdir -p inputfiletemplates
cp ${TEMPLATEDIR}/arps.input inputfiletemplates/
cp ${TEMPLATEDIR}/arpsenkfic.input inputfiletemplates/
cp ${TEMPLATEDIR}/arpsenkf.input inputfiletemplates/
