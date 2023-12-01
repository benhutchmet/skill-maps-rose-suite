#!/bin/bash
#SBATCH --partition=test
#SBATCH --job-name=ben-array-sel-region-test
#SBATCH -o ./logs/%j.out
#SBATCH -e ./logs/%j.err
#SBATCH --time=10:00
#SBATCH --array=1960-1965

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
    echo "Usage: test-sel-region-array-script.bash <model> <variable> <region> <forecast-range> <season> <experiment>"
    exit 1
fi

# Extract the model, variable, region, forecast range and season
model=$1
variable=$2
region=$3
forecast_range=$4
season=$5
experiment=$6

# Load cdo
module load jaspy

# Set up the process script
process_script=$PWD/process_scripts/multi-model.sel-region-forecast-range-season.bash

# Set up a test models list
test_models="BCC-CSM2-MR MPI-ESM1-2-HR CanESM5 CMCC-CM2-SR5"

# Loop over models
for model in $test_models; do

    # Echo the model name
    echo "Processing model: $model"

    # Extract the number of ensemble members
    # declare these as integers
    declare -i nens=${psl_models_nens[$model]}

    # Loop over the years
    for run in $(seq 1 $nens); do

        # Echo the year
        echo "Processing run: $run"

        # Run the process script as an array job
        bash $process_script ${model} ${SLURM_ARRAY_TASK_ID} ${run} ${variable} ${region} ${forecast_range} ${season} ${experiment}

    done

done

# End of script
echo "Finished processing ${model} ${variable} ${region} ${forecast_range} ${season} ${experiment} ${start_year} ${end_year}"
