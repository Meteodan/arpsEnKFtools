#!/bin/bash

# Define needed directories, files, etc.
SCRATCHBASE="/scratch/rice/d/dawson29/"
DEPOTBASE="/depot/dawson29/"
BASEDIR="${SCRATCHBASE}Projects/VORTEXSE/simulations/ARPS/2017_IOP4C/EnKF/"
RUNNAMEBASE="6km303x303_043017"
RUNNAMETAG="_NAM"
RUNNAME=${RUNNAMEBASE}${RUNNAMETAG}
TEMPLATEBASEDIR="${DEPOTBASE}apps/Projects/arpsEnKFtools/template/"
TEMPLATEDIR="${TEMPLATEBASEDIR}${RUNNAME}"
SFCDATA="${DEPOTBASE}data/Projects/VORTEXSE/simulations/ARPS/sfcdata/6km303x303.sfcdata"
TRNDATA="${DEPOTBASE}data/Projects/VORTEXSE/simulations/ARPS/trndata/6km303x303.trndata"
BOUNDARYDIR="${DEPOTBASE}data/Projects/VORTEXSE/simulations/ARPS/2017_IOP4C/EnKF/6km033116NAM303x303bgandbc/"
RADARDIR="${DEPOTBASE}data/Projects/VORTEXSE/simulations/ARPS/2017_IOP4C/processed_radar/"
CONVDATADIR="${DEPOTBASE}data/Projects/VORTEXSE/simulations/ARPS/2017_IOP4C/convobsdata/"
SCATTDIR="/depot/dawson29/data/Projects/VORTEXSE/simulations/ARPS/2017_IOP4C/EnKF/scatt_6kmconv/"
ARPSEXE="/home/dawson29/arps5.4_main/bin/arps_mpi"
ARPSENKFICEXE="/home/dawson29/arps5.4_main/bin/arpsenkfic"
ARPSENKFEXE="/home/dawson29/arps5.4_main/bin/arpsenkf_mpi"
RADFLAG="template.radflag"
PERTURBIC=1
# The following are only needed when running arpsenkfic
INIFILE="6km033116NAMnoDA.hdf010800"
INIBASE="6km033116NAMnoDA.hdfgrdbas"


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
ln -sf ${CONVDATADIR} obs
cp ${TEMPLATEBASEDIR}/run_real_data_case.py .
cp ${TEMPLATEDIR}/run_real_data_case.csh .
cp ${TEMPLATEDIR}/${RADFLAG} .
mkdir -p inputfiletemplates
cp ${TEMPLATEDIR}/arps.input inputfiletemplates/
cp ${TEMPLATEDIR}/arpsenkfic.input inputfiletemplates/
cp ${TEMPLATEDIR}/arpsenkf.input inputfiletemplates/
cp ${TEMPLATEDIR}/blacklist.sfc .
