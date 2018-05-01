#!/bin/bash

# Define needed directories, files, etc.
SCRATCHBASE="/scratch/rice/d/dawson29/"
DEPOTBASE="/depot/dawson29/"
BASEDIR="${SCRATCHBASE}VORTEXSE/simulations/2016_IOP3/ARPS/EnKF/"
RUNNAME="3kmtest"
TEMPLATEDIR="${DEPOTBASE}apps/EnKF_template/"
SFCDATA="${DEPOTBASE}data/VORTEXSE/simulations/sfcdata/3km107x107.sfcdata"
TRNDATA="${DEPOTBASE}data/VORTEXSE/simulations/trndata/3km107x107.trndata"
BOUNDARYDIR="${DEPOTBASE}data/VORTEXSE/simulations/2016_IOP3/EnKF/3km033116NAM107x107bgandbc/"
RADARDIR="${DEPOTBASE}data/VORTEXSE/simulations/2016_IOP3/processed_radar/"
ARPSEXE="/home/dawson29/arps5.4_exp/bin/arps_mpi"
ARPSENKFICEXE="/home/dawson29/arps5.4_exp/bin/arpsenkfic"
ARPSENKFEXE="/home/dawson29/arps5.4_exp/bin/arpsenkf_mpi"
INIFILE="3km033116NAM107x107bgandbc.hdf010800"
INIBASE="3km033116NAM107x107bgandbc.hdfgrdbas"


#Create base experiment directory and change directories to it
EXPDIR=${BASEDIR}${RUNNAME}
mkdir ${EXPDIR}
cd ${EXPDIR}

#Copy/link in needed files and directories
ln -s ${SFCDATA} .
ln -s ${TRNDATA} .
ln -s ${BOUNDARYDIR} boundary
ln -s boundary/${INIBASE} .
ln -s boundary/${INIFILE} .
ln -s ${ARPSEXE} arps
ln -s ${ARPSENKFICEXE} arpsenkfic
ln -s ${ARPSENKFEXE} arpsenkf
ln -s ${RADARDIR} nexrad
cp ${TEMPLATEDIR}/run_real_data_case.py .
cp ${TEMPLATEDIR}/run_real_data_case.csh .
cp ${TEMPLATEDIR}/template.radflag .
mkdir inputfiletemplates
cp ${TEMPLATEDIR}/arps.input inputfiletemplates/
cp ${TEMPLATEDIR}/arpsenkfic.input inputfiletemplates/
cp ${TEMPLATEDIR}/arpsenkf.input inputfiletemplates/
