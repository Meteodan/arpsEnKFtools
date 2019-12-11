# plotARPS_control.py
# This module contains controlling parameters for the plotARPS_beta.py script
# It is split into two sections.  The first contains control parameters that determine
# the overall plotting setup (i.e. which variables to plot, whether to overlay a
# map, and the like).  The second section contains parameters controlling what is being
# plotted (i.e. directory and runnames, type of model used, times to plot)
#
# This module is imported into plotARPS_beta.py by default with the line inside plotARPS_beta.py
# that reads "from plotARPS_control.pyimport *".  However, it is highly recommended that the
# user copy this module and make their own version.  The module would then be dynamically
# imported by passing the user's version as a command line argument to plotARPS_beta.py

import numpy as N
import matplotlib
import matplotlib.cm as cm
from metpy.plots import ctables

#-----------------------------------------------------------------------------------------
# Section 1.
# Plot configuration parameters (how and what variables to plot, what overlays to use,
# contour levels and colormaps).
#-----------------------------------------------------------------------------------------

toPlot = True           # Option to plot or not.  Set to False if you only want to
                        # compute the variables and save to files.  These variables
                        # can then be read into this script or other scripts later
                        # for analysis/plotting.
loadvars = False        # Set to True if variables have been precomputed and saved
                        # to .npz files.  This saves time on subsequent plotting
                        # jobs if the user simply wants to modify the plots without
                        # needing to recalculate everything.
savedir = 'npzs/'       # Directory name (relative to output directory specified below)
                        # where .npz files are saved
ptype = 2               # 1 = Filled contour plot, 2 = Filled "pcolor" plot
pltfigtitle = True      # Plot figure titles or not?
ovrmap = True           # Overlay a map on relevant plots? (Ignored for plot_slice = 2 or plot_slice = 3).
plot_ref_model = False      # Plot reflectivity as calculated in-model?
storeCDF = False            # Option to store dual-pol variables in netCDF format.

movepltgrid = False           # Option to move plotting domain window to follow a feature of interest
pltgrid_u = 14.0              # W-E storm motion (m/s)
pltgrid_v =  8.0              # S-N storm motion (m/s)

ovrwind = True              # Overlay wind vectors on plots?
storm_u = 0.0 #-9.75 # -9.75 # -11.69 # 0.0
storm_v = 0.0 #-2.80 # -2.80 # -1.41 # 0.0

windintv_horz = 5               # Grid interval for wind vector plotting
windintv_vert = 5
wind_standard_value = 20
wind_scale = 1

# Parameters for T-matrix reflectivity calculation
tmat_opt = True
wavelen = 107.0 #Units of mm
#dirscatt = '/Users/ddawson/arps5.3_CVS/data/scatt/S-band/'
dirscatt = '/home/dawson29/Projects/pyCRMtools/data/tmatrix/S-band/MFflg1/'

# Map and GIS overlay stuff

ovrmap = True
gis_info = None # ["Moore OK", 35.3387, -97.4864]  # Plot location of a town, radar, etc
county_shapefile_location = '/home/dawson29/Projects/pyCRMtools/data/shapefiles/county/countyp020'
urban_shapefile_location = '/home/dawson29/Projects/pyCRMtools/data/shapefiles/urban2/tl_2008_us_cbsa'

draw_counties = 0
draw_urban = 0
draw_radar = 0

# Colormaps for various variables
refl_colors = ['#00FFFF', '#6495ED', '#000090', '#00FF00', '#00BB00', '#008800', '#FFFF00',
               '#FFDD00', '#DAA520', '#FF0000', '#B21111', '#990000', '#FF00FF', '#BB55DD']

# cmapdBZ = ctables.__getattribute__('NWSReflectivity')
normdBZ, cmapdBZ = ctables.registry.get_with_steps('NWSReflectivity', 5., 5.)

#Slice control parameters

plot_slice = 1          # Type of slice to plot: 1 - horizontal slice at given model levels
                        #                        2 - vertical E-W cross section at given j-location
                        #                        3 - vertical S-N cross section at given i-location
                        #                        4 - Radar elevation angle (deg) (not implemented yet!)
intrpswp = 1            # If plot_slice = 4, how should we interpolate to the radar sweep surface?
                        # intrpswp = 0: Simple vertical linear interpolation
                        # intrpswp = 1: Gaussian power-weighted average.
slices = [1]          # List of slices to plot (not yet implemented, see slice1,2,3 below)

# Tick intervals for each axis (m)
plotxtickintv = 100000.
plotytickintv = 100000.
plotztickintv = 1000.

savefigopt = 1
figfmt = 'png'              # Format of figures (e.g., .png, .pdf, .jpg, .eps, etc.)

nproc_x_in = 3             # Number of patches for split history files.
nproc_y_in = 5

# Misc section (incomplete or unimplemented stuff)
ovrtrajc = False
trajxoffset = -54750.0
trajyoffset = -64750.0

filter_opt = False   # Filter with a Raymond Low-pass implicit filter?
filt3d = False
filtcoeff = 10.0         # Coefficient for filter: 1.0 = 50% reduction in 4*delta_x amplitude
                        # Higher values damp progressively larger scales and vice versa

smooth = False # Smooth variable with a uniform filter?
filterwidth = 3

ovrquad = False  # Overlay quadrants for tornado analysis?
# tor_x = 107875.0 # 5100 s MY3
# tor_y = 114375.0
#
# tor_x = 103125.0 # 4380 s
# tor_y = 110375.0

tor_x = 106875.0+trajxoffset # 4860 s
tor_y = 113125.0+trajyoffset

ovrxzslice = False               # Overlay location of vertical cross section on some plots?
xzslice = 50
ovryzslice = False
yzslice = 50

#-----------------------------------------------------------------------------------------
# Section 2:
# Data input parameters.
#-----------------------------------------------------------------------------------------

basedir = '/scratch/rice/d/dawson29/Projects/051913_OK/ARPS/EnKF/3km153x153_051913_OK_NAM/3km153x153_051913_OK_NAM/' # Base directory name where individual
                                                                # run folders reside
outdirname = basedir+'plots/' # The directory name where the simulated dual-pol data will be saved.
toPlot_list = [False, False, True, False]
dir_list = ['./ENamean/', './ENfmean/', './EN001/', './ENF001/']
dir_extra_list = ['./', './', './', './']
runname_list = ['enmean', 'efmean', 'ena001', 'enf001']
runlabel_list = ['enmean', 'efmean', 'ena001', 'enf001']
trailer_list = ['', '', '', '']
mphyopt_list = [15, 15, 15, 15]
plotlim_list = [None, None, None, None]
master_time_list = [N.arange(49500.0, 72000.0+900.0, 900.0), N.arange(6300.0, 6300.0+900.0, 900.0),
                    N.arange(17400.0, 18000.0+300.0, 300.0), N.arange(49500.0, 72000.0+900.0, 900.0)]
start_timestamp_list = ['20130519180000', '20130519180000', '20130519180000', '20130519180000']
arbfile_list = [None, None, None, None]

# Variables to plot

fieldname = "dBZmod"
fieldlevels = N.arange(5.0,85.0+5.0,5.0)
clvls = matplotlib.ticker.MultipleLocator(base=10.0)
clabel = r'dBZ'
cformat = None
fieldcm = cmapdBZ
norm = matplotlib.colors.BoundaryNorm(fieldlevels,fieldcm.N)
plabel = None
slice1 = 1
stag = 's'

fieldovername = "w"
fieldoverlevels = N.arange(5.0,60.0+5.0,5.0)
fieldovercolor = 'k'
slice2 = 14
stagovr = 's'

fieldover2name = "vortz"
fieldover2levels = N.arange(3.e-3,1.e-2,1.e-3) # N.arange(1.e-1,1.,1.e-1)
fieldover2color = 'purple'
slice3 = 14 # 14
stagovr2 = 's'
