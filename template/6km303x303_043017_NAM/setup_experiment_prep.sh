#!/bin/bash
# This script sets up and optionally executes all of the "preparation" work required to successfully
# run an ARPS-EnKF experiment. This includes running the arpstrn and arpssfc programs to generate
# terrain and surface characteristic files for the domain. It also includes running ext2arps,
# wrf2arps, or arpsintrp to generate the initial and boundary condition files. (Which program
# is used depends on the nature of the external model that will be providing the IC's and BC's.)
# Finally it will also optionally run the radar remapper (88d2arps) and other observation
# conversion programs to prep the observation data to be assimilated (coming soon)

# Define needed directories
SCRATCHBASE="/scratch/rice/d/dawson29/"
DEPOTBASE="/depot/dawson29/"
IOPDIRNAME="2017_IOP4C"
BASEDIR="${SCRATCHBASE}VORTEXSE/simulations/ARPS/${IOPDIRNAME}/prep/"
RUNNAMEBASE="6km303x303_043017"
RUNNAMETAG="_NAM"
RUNNAME=${RUNNAMEBASE}${RUNNAMETAG}
TEMPLATEBASEDIR="${DEPOTBASE}apps/arpsEnKFtools/template/"
TEMPLATEDIR="${TEMPLATEBASEDIR}${RUNNAME}"
SFCDATA="${DEPOTBASE}data/Projects/VORTEXSE/simulations/ARPS/sfcdata/"
TRNDATA="${DEPOTBASE}data/Projects/VORTEXSE/simulations/ARPS/trndata/"
BOUNDARYDIR="${DEPOTBASE}data/Projects/VORTEXSE/simulations/ARPS/${IOPDIRNAME}/EnKF/${RUNNAME}bgandbc/"
# RADARDIR="${DEPOTBASE}data/Projects/VORTEXSE/simulations/ARPS/${IOPDIRNAME}/processed_radar/"
# CONVDATADIR="${DEPOTBASE}data/Projects/VORTEXSE/simulations/ARPS/${IOPDIRNAME}/convobsdata/"
SCATTDIR="/depot/dawson29/data/Projects/VORTEXSE/simulations/ARPS/${IOPDIRNAME}/EnKF/scatt_${RUNNAME}/"
ARPSBASEDIR="/home/dawson29/arps5.4_main/"
# TODO: directories for surface, terrain, and external model data


# Executable file locations
ARPSTRNEXE="${ARPSBASEDIR}bin/arpstrn"
ARPSSFCEXE="${ARPSBASEDIR}bin/arpssfc"
EXT2ARPSEXE="${ARPSBASEDIR}bin/ext2arps_mpi"

# Parameters, flags, etc.
N_ENS=40  # For linking external boundary condition files: TODO: figure out how to perturb BC's

RUN_ARPSTRN = 1
RUN_ARPSSFC = 1
RUN_EXT2ARPS = 0
RUN_WRF2ARPS = 0
RUN_ARPSINTRP = 0

# Create prep directory if it doesn't already exist
mkdir -p ${BASEDIR} || exit 1
cd ${BASEDIR}

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
