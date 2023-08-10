#!/usr/bin/env bash
# Use descriptive variable names for source and target folders
SOURCE_PATH="cert-12841247/r1"
REDUCED_PATH="data/scenario2_processed/r1/reduced"
TARGET_PATH="data/scenario2_processed"
# Exit on error and undefined variables
set -eu
# Create target folder if it does not exist
mkdir -p "$REDUCED_PATH"
# Loop over all csv files in source folder
for f in device http logon
do
  # Check if source file exists
  if [ -f "$SOURCE_PATH/$f.csv" ]; then
    # Extract the first 4501 lines of source file and remove the header row
    head -n 4501 "$SOURCE_PATH/$f.csv" | tail -n +2 > "$REDUCED_PATH/$f-reduced.csv"
    # Print success message
    echo "Reduced $SOURCE_PATH/$f.csv to $REDUCED_PATH/$f-reduced.csv" >&1
    # Add the value of 'f' (device, http or logon) to the first column of CSV file
    awk -v f="$f" -F"," 'BEGIN {OFS = ","} {$1 = f OFS $1; print}' "$REDUCED_PATH/$f-reduced.csv" > "$REDUCED_PATH/$f-modified.csv"
    # Print success message
    echo "Added $f to the first column of $REDUCED_PATH/$f-reduced.csv" >&1
  else
    # Print error message
    echo "File not found: $SOURCE_PATH/$f.csv" >&2
  fi
done
# Check if target folder contains any reduced files

# Concatenate all reduced files into a single file
cat $REDUCED_PATH/*-modified.csv > $TARGET_PATH/scenario2-truenegative-data.csv
# Print success message
echo "Concatenated all reduced files in $REDUCED_PATH to $SOURCE_PATH/scenario2-truenegative-data.csv" >&1
