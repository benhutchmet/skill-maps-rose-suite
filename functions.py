# functions for the main program
# these should be tested one by one
# before being used in the main program
#
# Usage: python functions.py <variable> <model> <region> <forecast_range> <season>
#
# Example: python functions.py "psl" "BCC-CSM2-MR" "north-atlantic" "2-5" "DJF"
#

# Imports
import argparse
import os
import sys
import glob
import re

# Third party imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs
from datetime import datetime
import scipy.stats as stats
import matplotlib.animation as animation
from matplotlib import rcParams
from PIL import Image


# Install imageio
# ! pip install imageio
import imageio.v3 as iio

# Set the path to imagemagick
rcParams['animation.convert_path'] = r'/usr/bin/convert'

# Local imports
sys.path.append('/home/users/benhutch/skill-maps')
import dictionaries as dic

# We want to write a function that takes a data directory and list of models
# which loads all of the individual ensemble members into a dictionary of datasets /
# grouped by models
# the arguments are:
# base_directory: the base directory where the data is stored
# models: a list of models to load
# variable: the variable to load, extracted from the command line
# region: the region to load, extracted from the command line
# forecast_range: the forecast range to load, extracted from the command line
# season: the season to load, extracted from the command line

def load_data(base_directory, models, variable, region, forecast_range, season):
    """Load the data from the base directory into a dictionary of datasets.
    
    This function takes a base directory and a list of models and loads
    all of the individual ensemble members into a dictionary of datasets
    grouped by models.
    
    Args:
        base_directory: The base directory where the data is stored.
        models: A list of models to load.
        variable: The variable to load, extracted from the command line.
        region: The region to load, extracted from the command line.
        forecast_range: The forecast range to load, extracted from the command line.
        season: The season to load, extracted from the command line.
        
    Returns:
        A dictionary of datasets grouped by models.
    """
    
    # Create an empty dictionary to store the datasets.
    datasets_by_model = {}
    
    # Loop over the models.
    for model in models:
        
        # Create an empty list to store the datasets for this model.
        datasets_by_model[model] = []
        
        # create the path to the files for this model
        files_path = base_directory + "/" + variable + "/" + model + "/" + region + "/" + f"years_{forecast_range}" + "/" + season + "/" + "outputs" + "/" + "mergetime" + "/" + "*-anoms.nc"

        # print the path to the files
        print("Searching for files in ", files_path)

        # Create a list of the files for this model.
        files = glob.glob(files_path)

        # if the list of files is empty, print a warning and
        # exit the program
        if len(files) == 0:
            print("No files found for " + model)
            sys.exit()
        
        # Print the files to the screen.
        print("Files for " + model + ":", files)

        # Loop over the files.
        for file in files:

            # Print the file to the screen.
            # print(file)
            
            # check that the file exists
            # if it doesn't exist, print a warning and
            # exit the program
            if not os.path.exists(file):
                print("File " + file + " does not exist")
                sys.exit()

            # Load the dataset.
            dataset = xr.open_dataset(file, chunks = {"time":50})

            # Append the dataset to the list of datasets for this model.
            datasets_by_model[model].append(dataset)
            
    # Return the dictionary of datasets.
    return datasets_by_model

# Write a function to process the data
# this includes an outer function that takes datasets by model
# and an inner function that takes a single dataset
# the outer function loops over the models and calls the inner function
# the inner function processes the data for a single dataset
# by extracting the variable and the time dimension
def process_data(datasets_by_model, variable):
    """Process the data.
    
    This function takes a dictionary of datasets grouped by models
    and processes the data for each dataset.
    
    Args:
        datasets_by_model: A dictionary of datasets grouped by models.
        variable: The variable to load, extracted from the command line.
        
    Returns:
        variable_data_by_model: the data extracted for the variable for each model.
        model_time_by_model: the model time extracted from each model for each model.
    """
    
    print(f"Dataset type: {type(datasets_by_model)}")

    def process_model_dataset(dataset, variable):
        """Process a single dataset.
        
        This function takes a single dataset and processes the data.
        
        Args:
            dataset: A single dataset.
            variable: The variable to load, extracted from the command line.
            
        Returns:
            variable_data: the extracted variable data for a single model.
            model_time: the extracted time data for a single model.
        """
        
        if variable == "psl":
           

            # print the variable data
            # print("Variable data: ", variable_data)
            # # print the variable data type
            # print("Variable data type: ", type(variable_data))

            # # print the len of the variable data dimensions
            # print("Variable data dimensions: ", len(variable_data.dims))
            
            # Convert from Pa to hPa.
            # Using try and except to catch any errors.
            try:
                # Extract the variable.
                variable_data = dataset["psl"]

                # print the values of the variable data
                print("Variable data values: ", variable_data.values)

            except:
                print("Error converting from Pa to hPa")
                sys.exit()

        elif variable == "tas":
            # Extract the variable.
            variable_data = dataset["tas"]
        elif variable == "rsds":
            # Extract the variable.
            variable_data = dataset["rsds"]
        elif variable == "sfcWind":
            # Extract the variable.
            variable_data = dataset["sfcWind"]
        else:
            print("Variable " + variable + " not recognised")
            sys.exit()

        # If variable_data is empty, print a warning and exit the program.
        if variable_data is None:
            print("Variable " + variable + " not found in dataset")
            sys.exit()

        # Extract the time dimension.
        model_time = dataset["time"].values
        # Set the type for the time dimension.
        model_time = model_time.astype("datetime64[Y]")

        # If model_time is empty, print a warning and exit the program.
        if model_time is None:
            print("Time not found in dataset")
            sys.exit()

        return variable_data, model_time
    
    # Create empty dictionaries to store the processed data.
    variable_data_by_model = {}
    model_time_by_model = {}
    for model, datasets in datasets_by_model.items():
        try:
            # Create empty lists to store the processed data.
            variable_data_by_model[model] = []
            model_time_by_model[model] = []
            # Loop over the datasets for this model.
            for dataset in datasets:
                # Process the dataset.
                variable_data, model_time = process_model_dataset(dataset, variable)
                # Append the processed data to the lists.
                variable_data_by_model[model].append(variable_data)
                model_time_by_model[model].append(model_time)
        except Exception as e:
            print(f"Error processing dataset for model {model}: {e}")
            print("Exiting the program")
            sys.exit()

    # Return the processed data.
    return variable_data_by_model, model_time_by_model

# Functions to process the observations.
# Broken up into smaller functions.
# ---------------------------------------------
def check_file_exists(file_path):
    """
    Check if a file exists in the given file path.

    Parameters:
    file_path (str): The path of the file to be checked.

    Returns:
    None

    Raises:
    SystemExit: If the file does not exist in the given file path.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist")
        sys.exit()

def regrid_observations(obs_dataset):
    """
    Regrids an input dataset of observations to a standard grid.

    Parameters:
    obs_dataset (xarray.Dataset): The input dataset of observations.

    Returns:
    xarray.Dataset: The regridded dataset of observations.

    Raises:
    SystemExit: If an error occurs during the regridding process.
    """
    try:

        regrid_example_dataset = xr.Dataset({
            "lon": (["lon"], np.arange(0.0, 359.9, 2.5)),
            "lat": (["lat"], np.arange(90.0, -90.1, -2.5)),
        })
        regridded_obs_dataset = obs_dataset.interp(
            lon=regrid_example_dataset.lon,
            lat=regrid_example_dataset.lat
        )
        return regridded_obs_dataset
    
    except Exception as e:
        print(f"Error regridding observations: {e}")
        sys.exit()


def select_region(regridded_obs_dataset, region_grid):
    """
    Selects a region from a regridded observation dataset based on the given region grid.

    Parameters:
    regridded_obs_dataset (xarray.Dataset): The regridded observation dataset.
    region_grid (dict): A dictionary containing the region grid with keys 'lon1', 'lon2', 'lat1', and 'lat2'.

    Returns:
    xarray.Dataset: The regridded observation dataset for the selected region.

    Raises:
    SystemExit: If an error occurs during the region selection process.
    """
    try:

        # Echo the dimensions of the region grid
        print(f"Region grid dimensions: {region_grid}")

        # Define lon1, lon2, lat1, lat2
        lon1, lon2 = region_grid['lon1'], region_grid['lon2']
        lat1, lat2 = region_grid['lat1'], region_grid['lat2']

        # dependent on whether this wraps around the prime meridian
        if lon1 < lon2:
            regridded_obs_dataset_region = regridded_obs_dataset.sel(
                lon=slice(lon1, lon2),
                lat=slice(lat1, lat2)
            )
        else:
            # If the region crosses the prime meridian, we need to do this in two steps
            # Select two slices and concatenate them together
            regridded_obs_dataset_region = xr.concat([
                regridded_obs_dataset.sel(
                    lon=slice(0, lon2),
                    lat=slice(lat1, lat2)
                ),
                regridded_obs_dataset.sel(
                    lon=slice(lon1, 360),
                    lat=slice(lat1, lat2)
                )
            ], dim='lon')

        return regridded_obs_dataset_region
    except Exception as e:
        print(f"Error selecting region: {e}")
        sys.exit()

def select_season(regridded_obs_dataset_region, season):
    """
    Selects a season from a regridded observation dataset based on the given season string.

    Parameters:
    regridded_obs_dataset_region (xarray.Dataset): The regridded observation dataset for the selected region.
    season (str): A string representing the season to select. Valid values are "DJF", "MAM", "JJA", "SON", "SOND", "NDJF", and "DJFM".

    Returns:
    xarray.Dataset: The regridded observation dataset for the selected season.

    Raises:
    ValueError: If an invalid season string is provided.
    """
def select_season(regridded_obs_dataset_region, season):
    try:
        # Extract the months from the season string
        if season == "DJF":
            months = [12, 1, 2]
        elif season == "MAM":
            months = [3, 4, 5]
        elif season == "JJA":
            months = [6, 7, 8]
        elif season == "JJAS":
            months = [6, 7, 8, 9]
        elif season == "SON":
            months = [9, 10, 11]
        elif season == "SOND":
            months = [9, 10, 11, 12]
        elif season == "NDJF":
            months = [11, 12, 1, 2]
        elif season == "DJFM":
            months = [12, 1, 2, 3]
        else:
            raise ValueError("Invalid season")

        # Select the months from the dataset
        regridded_obs_dataset_region_season = regridded_obs_dataset_region.sel(
            time=regridded_obs_dataset_region["time.month"].isin(months)
        )

        return regridded_obs_dataset_region_season
    except:
        print("Error selecting season")
        sys.exit()

def calculate_anomalies(regridded_obs_dataset_region_season):
    """
    Calculates the anomalies for a given regridded observation dataset for a specific season.

    Parameters:
    regridded_obs_dataset_region_season (xarray.Dataset): The regridded observation dataset for the selected region and season.

    Returns:
    xarray.Dataset: The anomalies for the given regridded observation dataset.

    Raises:
    ValueError: If the input dataset is invalid.
    """
    try:
        obs_climatology = regridded_obs_dataset_region_season.mean("time")
        obs_anomalies = regridded_obs_dataset_region_season - obs_climatology
        return obs_anomalies
    except:
        print("Error calculating anomalies for observations")
        sys.exit()

def calculate_annual_mean_anomalies(obs_anomalies, season):
    """
    Calculates the annual mean anomalies for a given observation dataset and season.

    Parameters:
    obs_anomalies (xarray.Dataset): The observation dataset containing anomalies.
    season (str): The season for which to calculate the annual mean anomalies.

    Returns:
    xarray.Dataset: The annual mean anomalies for the given observation dataset and season.

    Raises:
    ValueError: If the input dataset is invalid.
    """
    try:
        # Shift the dataset if necessary
        if season in ["DJFM", "NDJFM"]:
            obs_anomalies_shifted = obs_anomalies.shift(time=-3)
        elif season in ["DJF", "NDJF"]:
            obs_anomalies_shifted = obs_anomalies.shift(time=-2)
        else:
            obs_anomalies_shifted = obs_anomalies

        # Calculate the annual mean anomalies
        obs_anomalies_annual = obs_anomalies_shifted.resample(time="Y").mean("time")

        return obs_anomalies_annual
    except:
        print("Error shifting and calculating annual mean anomalies for observations")
        sys.exit()

def select_forecast_range(obs_anomalies_annual, forecast_range):
    """
    Selects the forecast range for a given observation dataset.

    Parameters:
    obs_anomalies_annual (xarray.Dataset): The observation dataset containing annual mean anomalies.
    forecast_range (str): The forecast range to select.

    Returns:
    xarray.Dataset: The observation dataset containing annual mean anomalies for the selected forecast range.

    Raises:
    ValueError: If the input dataset is invalid.
    """
    try:
        forecast_range_start, forecast_range_end = map(int, forecast_range.split("-"))
        print("Forecast range:", forecast_range_start, "-", forecast_range_end)
        rolling_mean_range = forecast_range_end - forecast_range_start + 1
        print("Rolling mean range:", rolling_mean_range)
        obs_anomalies_annual_forecast_range = obs_anomalies_annual.rolling(time=rolling_mean_range, center = True).mean()
        return obs_anomalies_annual_forecast_range
    except Exception as e:
        print("Error selecting forecast range:", e)
        sys.exit()


def check_for_nan_values(obs):
    """
    Checks for NaN values in the observations dataset.

    Parameters:
    obs (xarray.Dataset): The observations dataset.

    Raises:
    SystemExit: If there are NaN values in the observations dataset.
    """
    try:
        if obs['var151'].isnull().values.any():
            print("Error: NaN values in observations")
            sys.exit()
    except Exception as e:
        print("Error checking for NaN values in observations:", e)
        sys.exit()

# Call the functions to process the observations
def process_observations(variable, region, region_grid, forecast_range, season, observations_path, obs_var_name):
    """
    Processes the observations dataset by regridding it to the model grid, selecting a region and season,
    calculating anomalies, calculating annual mean anomalies, selecting the forecast range, and returning
    the processed observations.

    Args:
        variable (str): The variable to process.
        region (str): The region to select.
        region_grid (str): The grid to regrid the observations to.
        forecast_range (str): The forecast range to select.
        season (str): The season to select.
        observations_path (str): The path to the observations dataset.
        obs_var_name (str): The name of the variable in the observations dataset.

    Returns:
        xarray.Dataset: The processed observations dataset.
    """

    # Check if the observations file exists
    check_file_exists(observations_path)

    try:
        # Load the observations dataset
        obs_dataset = xr.open_dataset(observations_path, chunks={"time": 50})[variable] if variable in ["tas", "sfcWind"] else xr.open_dataset(observations_path, chunks={"time": 50})

        # Regrid the observations to the model grid
        regridded_obs_dataset = regrid_observations(obs_dataset)

        # Select the region
        regridded_obs_dataset_region = select_region(regridded_obs_dataset, region_grid)

        # Select the season
        regridded_obs_dataset_region_season = select_season(regridded_obs_dataset_region, season)

        # Calculate anomalies
        obs_anomalies = calculate_anomalies(regridded_obs_dataset_region_season)

        # Calculate annual mean anomalies
        obs_annual_mean_anomalies = calculate_annual_mean_anomalies(obs_anomalies, season)

        # Select the forecast range
        obs_anomalies_annual_forecast_range = select_forecast_range(obs_annual_mean_anomalies, forecast_range)

        # Print the dimensions of the processed dataset to the user
        print("Processed observations dataset:", obs_anomalies_annual_forecast_range.dims)

        return obs_anomalies_annual_forecast_range

    except Exception as e:
        print(f"Error processing observations dataset: {e}")
        sys.exit()

def plot_data(obs_data, variable_data, model_time):
    """
    Plots the observations and model data as two subplots on the same figure.
    One on the left and one on the right.

    Parameters:
    obs_data (xarray.Dataset): The processed observations data.
    variable_data (xarray.Dataset): The processed model data for a single variable.
    model_time (str): The time dimension of the model data.

    Returns:
    None
    """

    # print the dimensions of the observations data
    print("Observations dimensions:", obs_data.dims)

    # Take the time mean of the observations
    obs_data_mean = obs_data.mean(dim='time')

    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 6))

    # Plot the observations on the left subplot
    obs_data_mean.plot(ax=ax1, transform=ccrs.PlateCarree(), cmap='coolwarm', vmin=-2, vmax=2)
    ax1.set_title('Observations')

    # Plot the model data on the right subplot
    variable_data.mean(dim=model_time).plot(ax=ax2, transform=ccrs.PlateCarree(), cmap='coolwarm', vmin=-2, vmax=2)
    ax2.set_title('Model Data')

    # Set the title of the figure
    # fig.suptitle(f'{obs_data.variable.long_name} ({obs_data.variable.units})\n{obs_data.region} {obs_data.forecast_range} {obs_data.season}')

    # Show the plot
    plt.show()

def plot_obs_data(obs_data):
    """
    Plots the first timestep of the observations data as a single subplot.

    Parameters:
    obs_data (xarray.Dataset): The processed observations data.

    Returns:
    None
    """

    # print the dimensions of the observations data
    print("Observations dimensions:", obs_data.dims)
    print("Observations variables:", obs_data)

    # Print all of the latitude values
    print("Observations latitude values:", obs_data.lat.values)
    print("Observations longitude values:", obs_data.lon.values)

    # Select the first timestep of the observations
    obs_data_first = obs_data.isel(time=-1)

    # Select the variable to be plotted
    # and convert to hPa
    obs_var = obs_data_first["var151"]/100

    # print the value of the variable
    print("Observations variable:", obs_var.values)

    # print the dimensions of the observations data
    print("Observations dimensions:", obs_data_first)

    # Create a figure with one subplot
    fig, ax = plt.subplots(figsize=(12, 6), subplot_kw={'projection': ccrs.PlateCarree()})

    # Plot the observations on the subplot
    c = ax.contourf(obs_data_first.lon, obs_data_first.lat, obs_var, transform=ccrs.PlateCarree(), cmap='coolwarm')

    # Add coastlines and gridlines to the plot
    ax.coastlines()
    ax.gridlines(draw_labels=True)

    # Add a colorbar to the plot
    fig.colorbar(c, ax=ax, shrink=0.6)

    # Set the title of the figure
    # fig.suptitle(f'{obs_data.variable.long_name} ({obs_data.variable.units})\n{obs_data.region} {obs_data.forecast_range} {obs_data.season}')

    # Show the plot
    plt.show()

# Define a function to make gifs
def make_gif(frame_folder):
    """
    Makes a gif from a folder of images.

    Parameters:
    frame_folder (str): The path to the folder containing the images.
    """

    # Set up the frames to be used
    frames = [Image.open(os.path.join(frame_folder, f)) for f in os.listdir(frame_folder) if f.endswith("_anomalies.png")]
    frame_one = frames[0]
    # Save the frames as a gif
    frame_one.save(os.path.join(frame_folder, "animation.gif"), format='GIF', append_images=frames, save_all=True, duration=300, loop=0)

def plot_model_data(model_data, models, gif_plots_path):
    """
    Plots the first timestep of the model data as a single subplot.

    Parameters:
    model_data (dict): The processed model data.
    models (list): The list of models to be plotted.
    gif_plots_path (str): The path to the directory where the plots will be saved.
    """

    # if the gif_plots_path directory does not exist
    if not os.path.exists(gif_plots_path):
        # Create the directory
        os.makedirs(gif_plots_path)

    # initialize an empty list to store the ensemble members
    ensemble_members = []

    # initialize a dictionary to store the count of ensemble members
    # for each model
    ensemble_members_count = {}

    # Initialize a dictionary to store the filepaths
    # of the plots for each model
    filepaths = []

    # For each model
    for model in models:
        model_data_combined = model_data[model]

        if model not in ensemble_members_count:
            ensemble_members_count[model] = 0

        for member in model_data_combined:
            ensemble_members.append(member)

            # Extract the lat and lon values
            lat = member.lat.values
            lon = member.lon.values

            years = member.time.dt.year.values

            # Increment the count of ensemble members for the model
            ensemble_members_count[model] += 1

    # Conver the ensemble members counts dictionary to a list of tuples
    ensemble_members_count_list = [(model, count) for model, count in ensemble_members_count.items()]

    # Conver the list of all ensemble members to a numpy array
    ensemble_members = np.array(ensemble_members)

    # take the ensemble mean over the members
    ensemble_mean = ensemble_members.mean(axis=0)

    # # print the values of lat and lon
    # print("lat values", ensemble_mean[0, :, 0])
    # print("lon values", ensemble_mean[0, 0, :])

    # lat_test = ensemble_mean[0, :, 0]
    # lon_test = ensemble_mean[0, 0, :]

    # print the dimensions of the model data
    print("ensemble mean shape", np.shape(ensemble_mean))

    # Extract the years from the model data
    # print the values of the years
    print("years values", years)
    print("years shape", np.shape(years))
    print("years type", type(years))


    # set the vmin and vmax values
    vmin = -500
    vmax = 500

    # Loop over the years array
    for year in years:
        # print the year
        print("year", year)

        # Set up the figure
        fig, ax = plt.subplots(figsize=(12, 6), subplot_kw={'projection': ccrs.PlateCarree()})

        # Plot the ensemble mean on the subplot
        # for the specified year
        # Check that the year index is within the range of the years array
        if year < years[0] or year > years[-1]:
            continue

        # Find the index of the year in the years array
        year_index = np.where(years == year)[0][0]

        # Plot the ensemble mean on the subplot
        # for the specified year
        c = ax.contourf(lon, lat, ensemble_mean[year_index, :, :], transform=ccrs.PlateCarree(), cmap='coolwarm', vmin=vmin, vmax=vmax, norm=plt.Normalize(vmin=vmin, vmax=vmax))

        # Add coastlines and gridlines to the plot
        ax.coastlines()
        ax.gridlines(draw_labels=True)

        # Annotate the plot with the year
        ax.annotate(f"{year}", xy=(0.01, 0.92), xycoords='axes fraction', fontsize=16)

        # Set up the filepath for saving
        filepath = os.path.join(gif_plots_path, f"{year}.png")
        # Save the figure
        fig.savefig(filepath)

        # Add the filepath to the list of filepaths
        filepaths.append(filepath)

        # Add coastlines and gridlines to the plot
        ax.coastlines()
        ax.gridlines(draw_labels=True)

        # Annotate the plot with the year
        ax.annotate(f"{year}", xy=(0.01, 0.92), xycoords='axes fraction', fontsize=16)

        # Set up the filepath for saving
        filepath = os.path.join(gif_plots_path, f"{year}_anomalies.png")
        # Save the figure
        fig.savefig(filepath)

        # Add the filepath to the list of filepaths
        filepaths.append(filepath)

    # Create the gif
    # Using the function defined above
    make_gif(gif_plots_path)

    # Show the plot
    # plt.show()


# Define a function which processes the model data for spatial correlations
def process_model_data_for_plot(model_data, models):
    """
    Processes the model data and calculates the ensemble mean.

    Parameters:
    model_data (dict): The processed model data.
    models (list): The list of models to be plotted.

    Returns:
    ensemble_mean (xarray.core.dataarray.DataArray): The equally weighted ensemble mean of the ensemble members.
    """
    # Initialize a list for the ensemble members
    ensemble_members = []

    # Initialize a dictionary to store the number of ensemble members
    ensemble_members_count = {}

    # Loop over the models
    for model in models:
        # Extract the model data
        model_data_combined = model_data[model]

        # Set the ensemble members count to zero
        # if the model is not in the ensemble members count dictionary
        if model not in ensemble_members_count:
            ensemble_members_count[model] = 0
        
        # Loop over the ensemble members in the model data
        for member in model_data_combined:
            # Append the ensemble member to the list of ensemble members
            ensemble_members.append(member)

            # Extract the lat and lon values
            lat = member.lat.values
            lon = member.lon.values

            # Extract the years
            years = member.time.dt.year.values

            # Increment the count of ensemble members for the model
            ensemble_members_count[model] += 1

    # Convert the list of all ensemble members to a numpy array
    ensemble_members = np.array(ensemble_members)

    # Take the equally weighted ensemble mean
    ensemble_mean = ensemble_members.mean(axis=0)

    # Convert ensemble_mean to an xarray DataArray
    ensemble_mean = xr.DataArray(ensemble_mean, coords=member.coords, dims=member.dims)

    return ensemble_mean, lat, lon, years

def calculate_spatial_correlations(observed_data, model_data, models):
    """
    Ensures that the observed and model data have the same dimensions, format and shape. Before calculating the spatial correlations between the two datasets.
    
    Parameters:
    observed_data (xarray.core.dataset.Dataset): The processed observed data.
    model_data (dict): The processed model data.
    models (list): The list of models to be plotted.

    Returns:
    rfield (xarray.core.dataarray.DataArray): The spatial correlations between the observed and model data.
    pfield (xarray.core.dataarray.DataArray): The p-values for the spatial correlations between the observed and model data.
    """
    try:
        # Process the model data and calculate the ensemble mean
        ensemble_mean, lat, lon, years = process_model_data_for_plot(model_data, models)

        # Extract the lat and lon values
        obs_lat = observed_data.lat.values
        obs_lon = observed_data.lon.values
        # And the years
        obs_years = observed_data.time.dt.year.values

        # Initialize lists for the converted lons
        obs_lons_converted, lons_converted = [], []

        # Transform the obs lons
        obs_lons_converted = np.where(obs_lon > 180, obs_lon - 360, obs_lon)
        # add 180 to the obs_lons_converted
        obs_lons_converted = obs_lons_converted + 180

        # For the model lons
        lons_converted = np.where(lon > 180, lon - 360, lon)
        # # add 180 to the lons_converted
        lons_converted = lons_converted + 180

        # Find the years that are in both the observed and model data
        years_in_both = np.intersect1d(obs_years, years)

        # Select only the years that are in both the observed and model data
        observed_data = observed_data.sel(time=observed_data.time.dt.year.isin(years_in_both))
        ensemble_mean = ensemble_mean.sel(time=ensemble_mean.time.dt.year.isin(years_in_both))

        # Remove years with NaNs
        observed_data, ensemble_mean = remove_years_with_nans(observed_data, ensemble_mean)

        # Convert both the observed and model data to numpy arrays
        # ----------------------------------------
        # Hardcoded for psl for now
        # ----------------------------------------
        observed_data_array = observed_data['var151'].values / 100
        ensemble_mean_array = ensemble_mean.values

        # Check that the observed data and ensemble mean have the same shape
        if observed_data_array.shape != ensemble_mean_array.shape:
            raise ValueError("Observed data and ensemble mean must have the same shape.")

        # Calculate the correlations between the observed and model data
        rfield, pfield = calculate_correlations(observed_data_array, ensemble_mean_array, obs_lat, obs_lon)

        return rfield, pfield, obs_lons_converted, lons_converted

    except Exception as e:
        print(f"An error occurred when calculating spatial correlations: {e}")

def calculate_correlations(observed_data, model_data, obs_lat, obs_lon):
    """
    Calculates the spatial correlations between the observed and model data.

    Parameters:
    observed_data (numpy.ndarray): The processed observed data.
    model_data (numpy.ndarray): The processed model data.
    obs_lat (numpy.ndarray): The latitude values of the observed data.
    obs_lon (numpy.ndarray): The longitude values of the observed data.

    Returns:
    rfield (xarray.core.dataarray.DataArray): The spatial correlations between the observed and model data.
    pfield (xarray.core.dataarray.DataArray): The p-values for the spatial correlations between the observed and model data.
    """
    try:
        # Initialize empty arrays for the spatial correlations and p-values
        rfield = np.empty([len(obs_lat), len(obs_lon)])
        pfield = np.empty([len(obs_lat), len(obs_lon)])

        # Loop over the latitudes and longitudes
        for y in range(len(obs_lat)):
            for x in range(len(obs_lon)):
                # set up the obs and model data
                obs = observed_data[:, y, x]
                mod = model_data[:, y, x]

                # Calculate the correlation coefficient and p-value
                r, p = stats.pearsonr(obs, mod)

                # Append the correlation coefficient and p-value to the arrays
                rfield[y, x], pfield[y, x] = r, p

        # Print the range of the correlation coefficients and p-values
        # to 3 decimal places
        print(f"Correlation coefficients range from {rfield.min():.3f} to {rfield.max():.3f}")
        print(f"P-values range from {pfield.min():.3f} to {pfield.max():.3f}")

        # Return the correlation coefficients and p-values
        return rfield, pfield

    except Exception as e:
        print(f"Error calculating correlations: {e}")
        sys.exit()

# checking for Nans in observed data
def remove_years_with_nans(observed_data, ensemble_mean):
    """
    Removes years from the observed data that contain NaN values.

    Args:
        observed_data (xarray.Dataset): The observed data.
        ensemble_mean (xarray.Dataset): The ensemble mean (model data).

    Returns:
        xarray.Dataset: The observed data with years containing NaN values removed.
    """

    for year in observed_data.time.dt.year.values[::-1]:
        # Extract the data for the year
        data = observed_data.sel(time=f"{year}")

        # If there are any Nan values in the data
        if np.isnan(data['var151'].values).any():
            # Print the year
            print(year)

            # Select the year from the observed data
            observed_data = observed_data.sel(time=observed_data.time.dt.year != year)

            # for the model data
            ensemble_mean = ensemble_mean.sel(time=ensemble_mean.time.dt.year != year)

        # if there are no Nan values in the data for a year
        # then print the year
        # and "no nan for this year"
        # and continue the script
        else:
            print(year, "no nan for this year")

            # exit the loop
            break

    return observed_data, ensemble_mean

# plot the correlations and p-values
def plot_correlations(model, rfield, pfield, obs, variable, region, season, forecast_range, plots_dir, obs_lons_converted, lons_converted, azores_grid, iceland_grid):
    """Plot the correlation coefficients and p-values.
    
    This function plots the correlation coefficients and p-values
    for a given variable, region, season and forecast range.
    
    Parameters
    ----------
    model : str
        Name of the model.
    rfield : array
        Array of correlation coefficients.
    pfield : array
        Array of p-values.
    obs : str
        Observed dataset.
    variable : str
        Variable.
    region : str
        Region.
    season : str
        Season.
    forecast_range : str
        Forecast range.
    plots_dir : str
        Path to the directory where the plots will be saved.
    obs_lons_converted : array
        Array of longitudes for the observed data.
    lons_converted : array
        Array of longitudes for the model data.
    azores_grid : array
        Array of longitudes and latitudes for the Azores region.
    iceland_grid : array
        Array of longitudes and latitudes for the Iceland region.

    """

    # Extract the lats and lons for the azores grid
    azores_lon1, azores_lon2 = azores_grid['lon1'], azores_grid['lon2']
    azores_lat1, azores_lat2 = azores_grid['lat1'], azores_grid['lat2']

    # Extract the lats and lons for the iceland grid
    iceland_lon1, iceland_lon2 = iceland_grid['lon1'], iceland_grid['lon2']
    iceland_lat1, iceland_lat2 = iceland_grid['lat1'], iceland_grid['lat2']

    # subtract 180 from all of the azores and iceland lons
    azores_lon1, azores_lon2 = azores_lon1 - 180, azores_lon2 - 180
    iceland_lon1, iceland_lon2 = iceland_lon1 - 180, iceland_lon2 - 180

    # set up the converted lons
    lons = lons_converted - 180

    # Set the font size for the plots
    plt.rcParams.update({'font.size': 12})

    # Set the figure size
    plt.figure(figsize=(10, 8))

    # Set the projection
    ax = plt.axes(projection=ccrs.PlateCarree())

    # Add coastlines
    ax.coastlines()

    # Add gridlines with labels for the latitude and longitude
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=2, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 12}
    gl.ylabel_style = {'size': 12}

    # Add green lines outlining the Azores and Iceland grids
    ax.plot([azores_lon1, azores_lon2, azores_lon2, azores_lon1, azores_lon1], [azores_lat1, azores_lat1, azores_lat2, azores_lat2, azores_lat1], color='green', linewidth=2, transform=ccrs.PlateCarree())
    ax.plot([iceland_lon1, iceland_lon2, iceland_lon2, iceland_lon1, iceland_lon1], [iceland_lat1, iceland_lat1, iceland_lat2, iceland_lat2, iceland_lat1], color='green', linewidth=2, transform=ccrs.PlateCarree())

    # Add filled contours
    # Contour levels
    clevs = np.arange(-1, 1.1, 0.1)
    # Contour levels for p-values
    clevs_p = np.arange(0, 1.1, 0.1)
    # Plot the filled contours
    cf = plt.contourf(lons, obs.lat, rfield, clevs, cmap='RdBu_r', transform=ccrs.PlateCarree())

    # replace values in pfield that are greater than 0.01 with nan
    pfield[pfield > 0.01] = np.nan

    # print the pfield
    print("pfield mod", pfield)

    # Add stippling where rfield is significantly different from zero
    plt.contourf(lons, obs.lat, pfield, hatches=['....'], alpha=0, transform=ccrs.PlateCarree())

    # Add colorbar
    cbar = plt.colorbar(cf, orientation='horizontal', pad=0.05, aspect=50)
    cbar.set_label('Correlation Coefficient')

    # extract the model name from the list
    # given as ['model']
    # we only want the model name
    # if the length of the list is 1
    # then the model name is the first element
    if len(model) == 1:
        model = model[0]
    elif len(model) > 1:
        model = "all_models"
    else :
        print("Error: model name not found")
        sys.exit()

    # Add title
    plt.title(f"{model} {variable} {region} {season} {forecast_range} Correlation Coefficients")

    # set up the path for saving the figure
    fig_name = f"{model}_{variable}_{region}_{season}_{forecast_range}_correlation_coefficients_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    fig_path = os.path.join(plots_dir, fig_name)

    # Save the figure
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')

    # Show the figure
    plt.show()

# Functions for choosing the observed data path
# and full variable name
def choose_obs_path(args):
    """
    Choose the obs path based on the variable
    """
    if args.variable == "psl":
        obs_path = dic.obs_psl
    elif args.variable == "tas":
        obs_path = dic.obs_tas
    elif args.variable == "sfcWind":
        obs_path = dic.obs_sfcWind
    elif args.variable == "rsds":
        obs_path = dic.obs_rsds
    else:
        print("Error: variable not found")
        sys.exit()
    return obs_path

# Choose the observed variable name
def choose_obs_var_name(args):
    """
    Choose the obs var name based on the variable
    """
    if args.variable == "psl":
        obs_var_name = dic.psl_label
    elif args.variable == "tas":
        obs_var_name = dic.tas_label
    elif args.variable == "sfcWind":
        obs_var_name = dic.sfc_wind_label
    elif args.variable == "rsds":
        obs_var_name = dic.rsds_label
    else:
        print("Error: variable not found")
        sys.exit()
    return obs_var_name

# define a main function
def main():
    """Main function for the program.
    
    This function parses the arguments from the command line
    and then calls the functions to load and process the data.
    """

    # Create a usage statement for the script.
    USAGE_STATEMENT = """python functions.py <variable> <model> <region> <forecast_range> <season>"""

    # Check if the number of arguments is correct.
    if len(sys.argv) != 6:
        print(f"Expected 6 arguments, but got {len(sys.argv)}")
        print(USAGE_STATEMENT)
        sys.exit()

    # Make the plots directory if it doesn't exist.
    if not os.path.exists(dic.plots_dir):
        os.makedirs(dic.plots_dir)

    # Parse the arguments from the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("variable", help="variable", type=str)
    parser.add_argument("model", help="model", type=str)
    parser.add_argument("region", help="region", type=str)
    parser.add_argument("forecast_range", help="forecast range", type=str)
    parser.add_argument("season", help="season", type=str)
    args = parser.parse_args()

    # Print the arguments to the screen.
    print("variable = ", args.variable)
    print("model = ", args.model)
    print("region = ", args.region)
    print("forecast range = ", args.forecast_range)
    print("season = ", args.season)

    # If the model specified == "all", then run the script for all models.
    if args.model == "all":
        args.model = dic.models

    # If the type of the model argument is a string, then convert it to a list.
    if type(args.model) == str:
        args.model = [args.model]

    # Load the data.
    datasets = load_data(dic.base_dir, args.model, args.variable, args.region, args.forecast_range, args.season)

    # Process the model data.
    variable_data, model_time = process_data(datasets, args.variable)

    # Choose the obs path based on the variable
    obs_path = choose_obs_path(args)

    # choose the obs var name based on the variable
    obs_var_name = choose_obs_var_name(args)

    # Process the observations.
    obs = process_observations(args.variable, args.region, dic.north_atlantic_grid, args.forecast_range, args.season, obs_path, obs_var_name)

    # Call the function to calculate the ACC
    rfield, pfield, obs_lons_converted, lons_converted = calculate_spatial_correlations(obs, variable_data, args.model)

    # Call the function to plot the ACC
    plot_correlations(args.model, rfield, pfield, obs, args.variable, args.region, args.season, args.forecast_range, dic.plots_dir, obs_lons_converted, lons_converted, dic.azores_grid, dic.iceland_grid)

# Call the main function.
if __name__ == "__main__":
    main()
