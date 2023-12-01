#!/bin/bash 
#SBATCH --partition=test
#SBATCH --job-name=ben-array-sel-region-test
#SBATCH -o /home/users/benhutch/skill-maps-rose-suite/logs
#SBATCH -e /home/users/benhutch/skill-maps-rose-suite/logs
#SBATCH --time=30:00
#SBATCH --array=1-10

# Echo th task id
echo "Task id is: ${SLURM_ARRAY_TASK_ID}"

# Set up the error log files
./test-sel-region-array-script.bash ${SLURM_ARRAY_TASK_ID}

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
    sbatch $process_script ${model} ${year} ${SLURM_ARRAY_TASK_ID} ${variable} ${region} ${forecast_range} ${season} ${experiment}

done

# End of script
echo "Finished processing ${model} ${variable} ${region} ${forecast_range} ${season} ${experiment} ${start_year} ${end_year}"
