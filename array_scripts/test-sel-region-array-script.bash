#!/bin/bash 
#SBATCH --partition=test
#SBATCH --job-name=ben-array-sel-region-test
#SBATCH -o ./${SLURM_JOB_NAME}_).out
#SBATCH -e ./${SLURM_JOB_NAME}_).err
#SBATCH --time=10:00
#SBATCH --array=1960-2021

# Echo th task id
echo "Task id is: ${SLURM_ARRAY_TASK_ID}"

# # Set up the error log files
# ./test-sel-region-array-script.bash ${SLURM_ARRAY_TASK_ID}

# Print the CLI arguments
echo "CLI arguments are: $@"
echo "Number of CLI arguments is: $#"
echo "Desired no. of arguments is: 7"

# Check if the correct number of arguments were passed
if [ $# -ne 7 ]; then
    echo "Usage: test-sel-region-array-script.bash <model> <variable> <region> <forecast-range> <season> <experiment> <nens>"
    exit 1
fi

# Extract the model, variable, region, forecast range and season
model=$1
variable=$2
region=$3
forecast_range=$4
season=$5
experiment=$6
nens=$7

# Load cdo
module load jaspy

# Set up the process script
process_script=$PWD/process_scripts/multi-model.sel-region-forecast-range-season.bash

# Loop over the years
for run in $(seq 1 $nens); do

    # Echo the year
    echo "Processing run: $run"

    # Run the process script as an array job
    bash $process_script ${model} ${year} ${SLURM_ARRAY_TASK_ID} ${variable} ${region} ${forecast_range} ${season} ${experiment}

done

# End of script
echo "Finished processing ${model} ${variable} ${region} ${forecast_range} ${season} ${experiment} ${start_year} ${end_year}"
