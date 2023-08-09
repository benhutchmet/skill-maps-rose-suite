# python dictionaries to be used in python/functions.py

# define the base directory where the data is stored
base_dir = "/home/users/benhutch/skill-maps-processed-data"

# define the directory where the plots will be saved
plots_dir = base_dir + "/plots"

gif_plots_dir = base_dir + "/plots/gif"

# list of the test model
test_model = [ "CMCC-CM2-SR5" ]

# List of the full models
models = [ "BCC-CSM2-MR", "MPI-ESM1-2-HR", "CanESM5", "CMCC-CM2-SR5", "HadGEM3-GC31-MM", "EC-Earth3", "MPI-ESM1-2-LR", "FGOALS-f3-L", "MIROC6", "IPSL-CM6A-LR", "CESM1-1-CAM5-CMIP5", "NorCPM1" ]

# define the paths for the observations
obs_psl = "/home/users/benhutch/ERA5_psl/long-ERA5-full.nc"

# the variable has to be extracted from these
obs_tas = "/home/users/benhutch/ERA5/adaptor.mars.internal-1687448519.6842003-11056-8-3ea80a0a-4964-4995-bc42-7510a92e907b.nc"
obs_sfcWind = "/home/users/benhutch/ERA5/adaptor.mars.internal-1687448519.6842003-11056-8-3ea80a0a-4964-4995-bc42-7510a92e907b.nc"
#

obs_rsds="not/yet/implemented"

# Define the labels for the plots - wind
sfc_wind_label="10-metre wind speed"
sfc_wind_units = 'm s\u207b\u00b9'

# Define the labels for the plots - temperature
tas_label="2-metre temperature"
tas_units="K"

psl_label="Sea level pressure"
psl_units="hPa"

rsds_label="Surface solar radiation downwards"
rsds_units="W m\u207b\u00b2"

# Define the dimensions for the grids
# for processing the observations
north_atlantic_grid = {
    'lon1': 280,
    'lon2': 37.5,
    'lat1': 77.5,
    'lat2': 20
}

# Define the dimensions for the gridbox for the azores
azores_grid = {
    'lon1': 152,
    'lon2': 160,
    'lat1': 36,
    'lat2': 40
}

# Define the dimensions for the gridbox for iceland
iceland_grid = {
    'lon1': 155,
    'lon2': 164,
    'lat1': 63,
    'lat2': 70
}


# HadGEM files
# -rw-r----- 1 badc open  779073 Jan  7  2021 sfcWind_Amon_HadGEM3-GC31-MM_dcppA-hindcast_s1960-r1i1p1f2_gn_196011-196012.nc
# -rw-r----- 1 badc open 4308880 Jan  7  2021 sfcWind_Amon_HadGEM3-GC31-MM_dcppA-hindcast_s1960-r1i1p1f2_gn_196101-196112.nc
# -rw-r----- 1 badc open 4309866 Jan  7  2021 sfcWind_Amon_HadGEM3-GC31-MM_dcppA-hindcast_s1960-r1i1p1f2_gn_196201-196212.nc
# -rw-r----- 1 badc open 4312259 Jan  7  2021 sfcWind_Amon_HadGEM3-GC31-MM_dcppA-hindcast_s1960-r1i1p1f2_gn_196301-196312.nc
# -rw-r----- 1 badc open 4311639 Jan  7  2021 sfcWind_Amon_HadGEM3-GC31-MM_dcppA-hindcast_s1960-r1i1p1f2_gn_196401-196412.nc
# -rw-r----- 1 badc open 4316503 Jan  7  2021 sfcWind_Amon_HadGEM3-GC31-MM_dcppA-hindcast_s1960-r1i1p1f2_gn_196501-196512.nc
# -rw-r----- 1 badc open 4312597 Jan  7  2021 sfcWind_Amon_HadGEM3-GC31-MM_dcppA-hindcast_s1960-r1i1p1f2_gn_196601-196612.nc
# -rw-r----- 1 badc open 4315542 Jan  7  2021 sfcWind_Amon_HadGEM3-GC31-MM_dcppA-hindcast_s1960-r1i1p1f2_gn_196701-196712.nc
# -rw-r----- 1 badc open 4311627 Jan  7  2021 sfcWind_Amon_HadGEM3-GC31-MM_dcppA-hindcast_s1960-r1i1p1f2_gn_196801-196812.nc
# -rw-r----- 1 badc open 4316690 Jan  7  2021 sfcWind_Amon_HadGEM3-GC31-MM_dcppA-hindcast_s1960-r1i1p1f2_gn_196901-196912.nc
# -rw-r----- 1 badc open 4316014 Jan  7  2021 sfcWind_Amon_HadGEM3-GC31-MM_dcppA-hindcast_s1960-r1i1p1f2_gn_197001-197012.nc
# -rw-r----- 1 badc open 1137799 Jan  7  2021 sfcWind_Amon_HadGEM3-GC31-MM_dcppA-hindcast_s1960-r1i1p1f2_gn_197101-197103.nc

# /badc/cmip6/data/CMIP6/DCPP/MOHC/HadGEM3-GC31-MM/dcppA-hindcast/s1960-r1i1p1f2/Amon/sfcWind/gn/files/d20200417
