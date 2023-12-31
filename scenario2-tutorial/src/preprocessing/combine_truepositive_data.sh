#!/bin/bash
# This script concatenates all the csv files in the source path and writes them to the target path

# Define source and target paths
SOURCE_PATH="data/scenario2_raw"
TARGET_PATH="data/scenario2_processed/scenario2-truepositive-data.csv"

# Concatenate files
cat "$SOURCE_PATH"/*.csv > "$TARGET_PATH"
# Check exit status and handle errors
if [ $? -ne 0 ]; then
  echo "Error: failed to concatenate files"
  exit 1
fi

# End of script
echo "Script completed successfully"
exit 0
