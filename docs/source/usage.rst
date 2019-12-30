=====
Usage
=====

arpsEnKFtools is a work in progress. Some features may not be working and there are
likely many bugs. It is helpful to first take a look at the directory structure:

.. raw:: html

    <p>
    <a href="arpsEnKFtools">arpsEnKFtools</a><br>
    ├── <a href="arpsEnKFtools/arpsenkftools/">arpsenkftools</a><br>
    ├── <a href="arpsEnKFtools/docs/">docs</a><br>
    ├── <a href="arpsEnKFtools/legacy/">legacy</a><br>
    ├── <a href="arpsEnKFtools/notebooks/">notebooks</a><br>
    ├── <a href="arpsEnKFtools/plotting_scripts/">plotting_scripts</a><br>
    ├── <a href="arpsEnKFtools/prep_scripts/">prep_scripts</a><br>
    ├── <a href="arpsEnKFtools/radremap_scripts/">radremap_scripts</a><br>
    ├── <a href="arpsEnKFtools/template/">template</a><br>
    └── <a href="arpsEnKFtools/utility_scripts/">utility_scripts</a><br>
    <br><br>
    </p>

For now, we will focus on just a few of these directories. The project structure is
changing quickly and some of these directories may be renamed or removed altogether.
Pay attention to this documentation.

The ``arpsenkftools/`` subdirectory contains code for editing the FORTRAN namelist files
and generating batch scripts for the HPC system as well as several utility functions.

The ``prep_scripts/`` directory contains several scripts to generate the needed input
data and configuration files, as well as to generate the main working directory for a
given ARPS-EnKF experiment:

.. raw:: html

    <p>
    <a href="prep_scripts">prep_scripts</a><br>
    ├── <a href="prep_scripts/link_lookup_tables.py">link_lookup_tables.py</a><br>
    ├── <a href="prep_scripts/link_nam.py">link_nam.py</a><br>
    ├── <a href="prep_scripts/link_radremap.py">link_radremap.py</a><br>
    ├── <a href="prep_scripts/radarinfo.dat">radarinfo.dat</a><br>
    ├── <a href="prep_scripts/run_arpsintrp.py">run_arpsintrp.py</a><br>
    ├── <a href="prep_scripts/run_arpssfc.py">run_arpssfc.py</a><br>
    ├── <a href="prep_scripts/run_arpstrn.py">run_arpstrn.py</a><br>
    ├── <a href="prep_scripts/run_ext2arps.py">run_ext2arps.py</a><br>
    ├── <a href="prep_scripts/run_radremap.py">run_radremap.py</a><br>
    ├── <a href="prep_scripts/run_wrf2arps.py">run_wrf2arps.py</a><br>
    └── <a href="prep_scripts/setup_experiment_working_dir.py">setup_experiment_working_dir.py</a><br>
    <br><br>
    </p>

Before getting into their function, we note that each of the ``run_<arps_exectuable>.py``,
as well as the ``link_<name>.py`` and ``setup_experiment_working_dir.py`` take one
command line argument each. This command line argument is the path to a python configuration
file for a given experiment, typically named ``master_config.py``. Several examples are
in the ``template/`` subdirectory. This directory contains subdirectories with descriptive
names of a particular experiment that contain template input files and a ``master_config.py``
script. The various driver scripts in the ``prep_scripts/`` directory import the configuration
in ``master_config.py`` for that experiment, and uses the template's namelist input files for
the purpose of running one of the preparation programs. For example, the directory
``template/3km153x153_051913_OK_NAM/`` contains the template for a small 3-km domain centered
on central OK for the 19 May 2013 tornadic supercell case. the ``_NAM`` in the name signifies
that it uses the NAM model forecast/analyses as the initial and boundary conditions. The
directory tree for this template looks like this:

.. raw:: html

    <p>
    <a href="3km153x153_051913_OK_NAM">3km153x153_051913_OK_NAM</a><br>
    ├── <a href="3km153x153_051913_OK_NAM/2013_0519.radflag">2013_0519.radflag</a><br>
    ├── <a href="3km153x153_051913_OK_NAM/arps.input">arps.input</a><br>
    ├── <a href="3km153x153_051913_OK_NAM/arpsenkf.input">arpsenkf.input</a><br>
    ├── <a href="3km153x153_051913_OK_NAM/arpsenkfic.input">arpsenkfic.input</a><br>
    ├── <a href="3km153x153_051913_OK_NAM/arpsintrp.input">arpsintrp.input</a><br>
    ├── <a href="3km153x153_051913_OK_NAM/arpssfc.input">arpssfc.input</a><br>
    ├── <a href="3km153x153_051913_OK_NAM/arpstrn.input">arpstrn.input</a><br>
    ├── <a href="3km153x153_051913_OK_NAM/blacklist.sfc">blacklist.sfc</a><br>
    ├── <a href="3km153x153_051913_OK_NAM/ext2arps.input">ext2arps.input</a><br>
    ├── <a href="3km153x153_051913_OK_NAM/master_config.py">master_config.py</a><br>
    ├── <a href="3km153x153_051913_OK_NAM/plotCRM_control_3km153x153_dBZ_w_zvort.py">plotCRM_control_3km153x153_dBZ_w_zvort.py</a><br>
    ├── <a href="3km153x153_051913_OK_NAM/plotCRM_control_3km153x153_pte_dBZ.py">plotCRM_control_3km153x153_pte_dBZ.py</a><br>
    ├── <a href="3km153x153_051913_OK_NAM/radremap_88D.input">radremap_88D.input</a><br>
    ├── <a href="3km153x153_051913_OK_NAM/run_real_data_case.sh">run_real_data_case.sh</a><br>
    └── <a href="3km153x153_051913_OK_NAM/wrf2arps.input">wrf2arps.input</a><br>
    <br><br>
    </p>

If you are familiar with the ARPS model ecosystem, you will recognize many of the
``*.input`` files as being FORTRAN namelist files that control various programs. At this
point it is a good idea to open up the ``master_config.py`` file. This file sets various
parameters, including the paths to various input, output, and executable files.
There are several dictionaries encapsulating namelist input parameters that will be
copied into the template namelist input files to control the behavior of the different programs.
These include grid and map projection parameters, frequency of boundary conditions, number of
cores for MPI jobs, parameters controlling the behavior of the EnKF assimilation, and so on.

As a quick example, to run the program ``arpstrn`` that generates the terrain file for the
ARPS domain, you would do the following on the command line, assuming you are starting in
the root directory of the repository::

    $ cd prep_scripts
    $ python run_arpstrn.py ../template/3km153x153_051913_OK_NAM/master_config.py

This will create a working directory, copy ``arpstrn.input`` into it, automatically edit
it with the appropriate parameters as defined in ``master_config.py`` and finally execute
``arpstrn``. Output from the program will be placed in a directory that is also specified
in ``master_config.py``.

Similarly, one would also run ``ext2arps`` to generate the initial and boundary conditions
as follows::

    $ python run_ext2arps.py ../template/3km153x153_051913_OK_NAM/master_config.py

The use of a single ``master_config.py`` as input for these scripts greatly simplifies
what otherwise would be a difficult and error-prone workflow by ensuring that each program
that is needed to orchestrate a full experiment is working with the same experiment structure.
This, among other things, obviates the need to manually edit several namelist input files and
manually having to keep track of the same parameters across them.

TODO: continue documentation to explain the other prep scripts and then on to the main
experiment script. Watch this space!