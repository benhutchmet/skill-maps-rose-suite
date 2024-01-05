#!/bin/bash

# Verify that the dictionaries.bash file exists
if [ ! -f $PWD/dictionaries.bash ]; then
    echo "ERROR: dictionaries.bash file does not exist"
    exit 1
fi

# Source the dictionaries
source /home/users/benhutch/skill-maps-rose-suite/dictionaries.bash

# Print tas path
echo "tas path is: $tas_path"

# Print the keys of example_array
echo "Keys of example_array are: ${example_array[@]}"

# Print the keys of psl_models_nens
echo "Values of psl_models_nens are: ${psl_models_nens[@]}"

# Print the keys of psl_models_nens
echo "Keys of psl_models_nens are: ${!psl_models_nens[@]}"

# Declare a new associative array
declare -A psl_models_nens_array

# Copy each key-value pair from psl_models_nens to psl_models_nens_array
for key in "${!psl_models_nens[@]}"; do
    psl_models_nens_array[$key]=${psl_models_nens[$key]}
done

# Now you can print the keys and values of psl_models_nens_array
echo "Values of psl_models_nens_array are: ${psl_models_nens_array[@]}"
echo "Keys of psl_models_nens_array are: ${!psl_models_nens_array[@]}"

# Echo the number of ensemble members for each model
for key in "${!psl_models_nens_array[@]}"; do
    echo "psl model and nens"
    echo "Model: $key, nens: ${psl_models_nens_array[$key]}"
done

echo "tas_path is: $tas_path"

# Loop over tas_models_nens
for key in "${!tas_models_nens[@]}"; do
    echo "tas model and nens"
    echo "Model: $key, nens: ${tas_models_nens[$key]}"
done

# Loop over rsds_models_nens
for key in "${!rsds_models_nens[@]}"; do
    echo "rsds model and nens"
    echo "Model: $key, nens: ${rsds_models_nens[$key]}"
done

# Loop over sfcWind_models_nens
for key in "${!sfcWind_models_nens[@]}"; do
    echo "sfcWind model and nens"
    echo "Model: $key, nens: ${sfcWind_models_nens[$key]}"
done

# Loop over tos_models_nens
for key in "${!tos_models_nens[@]}"; do
    echo "tos model and nens"
    echo "Model: $key, nens: ${tos_models_nens[$key]}"
done

echo "finished"