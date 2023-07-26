#!/bin/bash
#
# multi-model.calc-anoms-sub-anoms.bash
#
# Script for calculating the anomalies from the model mean state for a given model, variable, region, forecast range, and season.
#
# For example: multi-model.calc-anoms-sub-anoms.bash HadGEM3-GC31-MM 1960 1 psl north-atlantic 2-5 DJF

# Set the usage message
USAGE_MESSAGE="Usage: multi-model.calc-anoms-sub-anoms.bash <model> <initialization-year> <run-number> <variable> <region> <forecast-range> <season>"

# Check that the correct number of arguments have been passed
if [ $# -ne 7 ]; then
    echo "$USAGE_MESSAGE"
    exit 1
fi

# Extract the model-year-run, variable, region, forecast range and season
model=$1
year=$2
run=$3
variable=$4
region=$5
forecast_range=$6
season=$7

# Load cdo
module load jaspy

# Set the base directory
base_dir="/work/scratch-nopw2/benhutch/$variable/$model/$region/years_${forecast_range}/$season/outputs"
OUTPUT_DIR="${base_dir}/anoms"

# Function for calculating anomalies
calculate_anoms() {
    # Extract the initialization scheme
    init_scheme=$1

    # Set up the input file path
    INPUT_FILE="$base_dir/mean-years-${forecast_range}-${season}-${region}-${variable}_Amon_${model}_dcppA-hindcast_s${year}-r${run}${init_scheme}*.nc"
    # Set up the model mean state file path
    MODEL_MEAN_STATE="$base_dir/tmp/model_mean_state_${init_scheme}.nc"

    # Echo the files to be processed
    echo "Calculating anomalies for: $INPUT_FILE"
    echo "Using model mean state file: $MODEL_MEAN_STATE"

    # Check that the input files exist
    if [ ! -f $INPUT_FILE ]; then
        echo "ERROR: input files not found ${init_scheme}"
        exit 1
    fi

    # Check that the model mean state file exists
    if [ ! -f $MODEL_MEAN_STATE ]; then
        echo "ERROR: model mean state file not found ${init_scheme}"
        exit 1
    fi

    # Set up the output file name
    OUTPUT_FILE="$OUTPUT_DIR/$(basename ${INPUT_FILE%.nc})-anoms.nc"

    # Calculate the anomalies
    cdo sub $INPUT_FILE $MODEL_MEAN_STATE $OUTPUT_FILE
}


# Create output directories
mkdir -p $OUTPUT_DIR

# Processing
case $model in
    "NorCPM1")
        calculate_anoms "i1"
        calculate_anoms "i2"
        ;;
    "EC-Earth3")
        calculate_anoms "i1"
        calculate_anoms "i2"
        calculate_anoms "i4"
        ;;
    *)
        # For all other models, use a wildcard for init_scheme
        calculate_anoms "i1"
        ;;
esac

echo "Anomalies calculated for model $model, variable $variable, region $region, forecast range $forecast_range, season $season and saved to $OUTPUT_DIR"

# End of script
exit 0