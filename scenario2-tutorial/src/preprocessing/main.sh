#!/bin/bash
# This script executes a list of bash by order

# Files operations with Bash scripts
# Gather scenario 2 related files

HOME_PATH="src/preprocessing"
# cd $HOME_PATH

sh "$HOME_PATH/gather_scenario2_related_files.sh"
# Check exit status and handle errors
if [ $? -ne 0 ]; then
  echo "Error: failed to gather scenario 2 related files"
  exit 1
fi

# Combine true positive data
sh "$HOME_PATH/combine_truepositive_data.sh"
# Check exit status and handle errors
if [ $? -ne 0 ]; then
  echo "Error: failed to create true positive combined file"
  exit 1
fi

# Comebine true negative data
sh "$HOME_PATH/combine_truenegative_data.sh"
# Check exit status and handle errors
if [ $? -ne 0 ]; then
  echo "Error: failed to create true negative combined file"
  exit 1
fi

# Data operations with Python scripts
# Merge and transform data
# python3 "merge_transform_data.py"
# # Check exit status and handle errors
# if [ $? -ne 0 ]; then
#   echo "Error: failed to merge and transform data"
#   exit 1
# fi

# End of script
echo "Script completed successfully"
exit 0
