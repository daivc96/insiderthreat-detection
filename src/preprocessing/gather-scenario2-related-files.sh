#!/bin/bash
# Set the input field separator to semicolon
IFS=';'
# Use relative paths or variables for source and target folders
SOURCE_PATH="12841247/answers"
TARGET_PATH="data/scenario2-input"
# Create target folder if it does not exist
mkdir -p "$TARGET_PATH"
# Exit on error and undefined variables
set -eu
# Skip the header row of the csv file and read the rest line by line
tail -n +2 "$SOURCE_PATH/insiders.csv" | while read -r dataset scenario details user start end
do
  # Check if the scenario is equal to 2
  if [ "$scenario" -eq 2 ]; then
    # Find the file with name=details in the source folder
    filepath=$(find "$SOURCE_PATH" -name "$details")
    # Check if filepath is a regular file
    if [ -f "$filepath" ]; then
      # Copy the file to the target folder with -p option
      cp -p "$filepath" "$TARGET_PATH"
      # Print success message to standard output
      echo "Copied $filepath to $TARGET_PATH/$details" >&1
    else
      # Print error message to standard error
      echo "File not found: $filepath" >&2
    fi
  fi
done
