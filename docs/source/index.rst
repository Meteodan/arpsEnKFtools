.. Packaging Scientific Python documentation master file, created by
   sphinx-quickstart on Thu Jun 28 12:35:56 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

arpsEnKFtools
===========================

arpsEnKFtools is a package containing a set of scripts and configuration files for
running the ARPS-EnKF system. `ARPS <arps.caps.ou.edu>`_ is a non-hydrostatic, fully compressible storm-scale
NWP model developed at the `Center for Analysis and Prediction of Storms (CAPS) <http://www.caps.ou.edu/>`_ at the
`University of Oklahoma <www.ou.edu>`_. ARPS-EnKF is an ensemble Kalman Filter-based data assimilation
system for use with ARPS and WRF.

The arpsEnKFtools package is developed by Dan Dawson of Purdue University in collaboration with CAPS
scientists. This code merely provides a framework for orchestrating a typical real-data ARPS-EnKF
experiment; the source code for ARPS and ARPS-EnKF and auxilliary tools must be obtained separately.

arpsEnKFtools is available under the `BSD 3-Clause License <https://raw.githubusercontent.com/Meteodan/arpsEnKFtools/master/LICENSE>`_


.. toctree::
   :maxdepth: 2

   installation
   usage
