#!/bin/bash 
#SBATCH --partition=test
#SBATCH --job-name=ben-array-sel-region-test
#SBATCH -o ./${SLURM_JOB_NAME}_).out
#SBATCH -e ./${SLURM_JOB_NAME}_).err
#SBATCH --time=10:00
#SBATCH --array=1-8

# Echo th task id
echo "Task id is: ${SLURM_ARRAY_TASK_ID}"

# # Set up the error log files
# ./test-sel-region-array-script.bash ${SLURM_ARRAY_TASK_ID}

# Print the CLI arguments
echo "CLI arguments are: $@"
echo "Number of CLI arguments is: $#"
echo "Desired no. of arguments is: 8"

# Check if the correct number of arguments were passed
if [ $# -ne 8 ]; then
    echo "Usage: test-sel-region-array-script.bash <model> <variable> <region> <forecast-range> <season> <experiment> <start_year> <end_year>"
    exit 1
fi

# Extract the model, variable, region, forecast range and season
model=$1
variable=$2
region=$3
forecast_range=$4
season=$5
experiment=$6
start_year=$7
end_year=$8

# Load cdo
module load jaspy

# Set up the process script
process_script=$PWD/process_scripts/multi-model.sel-region-forecast-range-season.bash

# Loop over the years
for year in $(seq $start_year $end_year); do

    # Echo the year
    echo "Processing year: $year"

    # Run the process script as an array job
    bash $process_script ${model} ${year} ${SLURM_ARRAY_TASK_ID} ${variable} ${region} ${forecast_range} ${season} ${experiment}

done

# End of script
echo "Finished processing ${model} ${variable} ${region} ${forecast_range} ${season} ${experiment} ${start_year} ${end_year}"
