#!/bin/bash
#SBATCH --partition=test
#SBATCH --job-name=calc-anoms-array-test
#SBATCH -o /gws/nopw/j04/canari/users/benhutch/batch_logs/calc-anoms-array-test/%j.out
#SBATCH -e /gws/nopw/j04/canari/users/benhutch/batch_logs/calc-anoms-array-test%j.err
#SBATCH --time=10:00
#SBATCH --array=1960-1965

# Form the path for the logs folder and make sure it exists
logs_dir="/gws/nopw/j04/canari/users/benhutch/batch_logs/calc-anoms-array-test"

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
echo "SLURM_ARRAY_TASK_ID is: ${SLURM_ARRAY_TASK_ID}"

# Echo trhe CLI's
echo "CLI arguments are: $@"
echo "Number of CLI arguments is: $#"
echo "Desired no. of arguments is: 6" # FIXME: might need to change this

# Check if the correct number of arguments were passed
if [ $# -ne 6 ]; then
    echo "Usage: sbatch calc-anoms-array-test.bash <model> <variable> <region> \
<forecast-range> <season> <pressure-level>"
    echo "Example: sbatch calc-anoms-array-test.bash HadGEM3-GC31-MM psl global \
2-9 DJFM 100000"
    exit 1
fi

# Extract the model, variable, region, forecast range and season
model=$1
variable=$2
region=$3
forecast_range=$4
season=$5
pressure_level=$6

# Print the model, variable, region, forecast range and season
echo "Model is: $model"
echo "Variable is: $variable"
echo "Region is: $region"
echo "Forecast range is: $forecast_range"
echo "Season is: $season"
echo "Pressure level is: $pressure_level"

# Load cdo
module load jaspy

# Set the process script
process_script="/home/users/benhutch/skill-maps-rose-suite/process_scripts/\
multi-model.calc-anoms-sub-anoms.bash"

# Check that the process script exists
if [ ! -f $process_script ]; then
    echo "ERROR: process script does not exist: $process_script"
    exit 1
fi

# If model is all
if [ $model == "all" ]; then
    
    echo "Extracting data for all models"

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
        echo "Extracting data for model: $model"

        # Extract the number of ensemble members
        nens=${nens_extractor[$model]}
            