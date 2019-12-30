============
Installation
============

The current preferred way to install arpsEnKFtools is using a combination of conda
environments and pip to install the package locally in "editable" mode. Make sure you
first have `Conda <https://conda.io/en/latest/>`_ installed on your system.

Currently, arpsEnKFtools is set up to work on the `Rice <rice.rcac.purdue.edu>`_ cluster at
Purdue's `Rosen Center for Advanced Computing (RCAC) <rcac.purdue.edu>`_. Adaptation for other systems
should be reasonably straightforward and is accomplished by appropriately editing ``batch.py`` in the
``arpsenkftools/`` subdirectory of the repository.

On Rice, it is necessary to first make sure you have the conda module loaded::

    $ module load anaconda

To install arpsEnKFtools, at the command line::

    $ git clone https://github.com/Meteodan/arpsEnKFtools.git
    $ cd arpsEnKFtools
    $ conda env create -f environment.yml
    $ pip install -e .

This will create a conda environment called ``arpsenkftools``. To activate this
environment type::

    $ conda activate arpsEnKFtools

After this, you should be able to run the scripts.
