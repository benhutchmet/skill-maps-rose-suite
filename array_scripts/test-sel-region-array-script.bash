#!/bin/bash
#SBATCH --partition=test
#SBATCH --job-name=ben-array-sel-region-test
#SBATCH -o /gws/nopw/j04/canari/users/benhutch/batch_logs/ben-array-sel-region-test/%j.out
#SBATCH -e /gws/nopw/j04/canari/users/benhutch/batch_logs/ben-array-sel-region-test/%j.err
#SBATCH --time=10:00
#SBATCH --array=1960-1963

# Form the path for the logs folder and make sure it exists
logs_dir="/gws/nopw/j04/canari/users/benhutch/batch_logs/ben-array-sel-region-test"

# If the logs directory does not exist
if [ ! -d $logs_dir ]; then
    # Make the logs directory
    mkdir -p $logs_dir
fi

# Verify that the dictionaries.bash file exists
if [ ! -f $PWD/dictionaries.bash ]; then
    echo "ERROR: dictionaries.bash file does not exist"
    exit 1
fi

# Source the dictionaries
source /home/users/benhutch/skill-maps-rose-suite/dictionaries.bash

# Echo th task id
echo "Task id is: ${SLURM_ARRAY_TASK_ID}"

# # Set up the error log files
# ./test-sel-region-array-script.bash ${SLURM_ARRAY_TASK_ID}

# Print the CLI arguments
echo "CLI arguments are: $@"
echo "Number of CLI arguments is: $#"
echo "Desired no. of arguments is: 6"

# Check if the correct number of arguments were passed
if [ $# -ne 6 ]; then
    echo "Usage: sbatch test-sel-region-array-script.bash <model> <variable> <region> <forecast-range> <season> <experiment>"
    echo "Example: sbatch test-sel-region-array-script.bash HadGEM3-GC31-MM psl global 2-9 DJFM dcppA-hindcast"
    exit 1
fi

# Extract the model, variable, region, forecast range and season
model=$1
variable=$2
region=$3
forecast_range=$4
season=$5
experiment=$6

# Print the model, variable, region, forecast range and season
echo "Model is: $model"
echo "Variable is: $variable"
echo "Region is: $region"
echo "Forecast range is: $forecast_range"
echo "Season is: $season"
echo "Experiment is: $experiment"

# Load cdo
module load jaspy

# Set up the process script
process_script=$PWD/process_scripts/multi-model.sel-region-forecast-range-season.bash

#FIXME: NENS extractor not working, but we use this in a different mode
# If model is all
if [ $model == "all" ]; then

    # Extract the models list using a case statement
    case $variable in
    "psl")
        models=$models
        nens_extractor=$psl_models_nens
        ;;
    "sfcWind")
        models=$sfcWind_models
        nens_extractor=$sfcWind_models_nens
        ;;
    "rsds")
        models=$rsds_models
        nens_extractor=$rsds_models_nens
        ;;
    "tas")
        models=$tas_models
        nens_extractor=$tas_models_nens
        ;;
    "tos")
        models=$tos_models
        nens_extractor=$tos_models_nens
        ;;
    *)
        echo "ERROR: variable not recognized: $variable"
        exit 1
        ;;
    esac

    # Loop over the models
    for model in $models; do

        # Echo the model name
        echo "Processing model: $model"

        # Declare nameref for the nens extractor
        declare -n nens_extractor_ref=nens_extractor

        # Extract the number of ensemble members
        nens=${nens_extractor_ref[$model]}

        # Loop over the years
        for run in $(seq 1 $nens); do

            # Echo the year
            echo "Processing run: $run"

            # Run the process script as an array job
            bash $process_script ${model} ${SLURM_ARRAY_TASK_ID} ${run} ${variable} ${region} ${forecast_range} ${season} ${experiment}

        done

    done

    # End the script
    echo "Finished processing ${model} ${variable} ${region} ${forecast_range} ${season} ${experiment} ${start_year} ${end_year}"
    exit 0

fi

# In the case of individual models
echo "Processing single model: $model"

# Echo the year which we are processing
echo "Processing year: ${SLURM_ARRAY_TASK_ID}"

# Extract the number of ensemble members for a single model
nens=${nens_extractor[$model]}

# Loop over the ensemble members
for run in $(seq 1 $nens); do

    # Echo the ensemble member
    echo "Processing run: $run"

    # # Run the process script as an array job
    # bash $process_script ${model} ${SLURM_ARRAY_TASK_ID} ${run} ${variable} \
    #     ${region} ${forecast_range} ${season} ${experiment}

done

# End of script
echo "Finished processing ${model} ${variable} ${region} ${forecast_range} ${season} ${experiment} ${start_year} ${end_year}"
