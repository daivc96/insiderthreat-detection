#!/bin/bash
# This script executes a list of bash and python scripts by order

# Files operations with Bash scripts
# Gather scenario 2 related files
sh "gather_scenario2_related_files.sh"
# Check exit status and handle errors
if [ $? -ne 0 ]; then
  echo "Error: failed to gather scenario 2 related files"
  exit 1
fi

# Create true positive data
sh "combine-truepositive-data.sh"
# Check exit status and handle errors
if [ $? -ne 0 ]; then
  echo "Error: failed to create true positive combined file"
  exit 1
fi

# Create true negative data
sh "combine-truenegative-data.sh"
# Check exit status and handle errors
if [ $? -ne 0 ]; then
  echo "Error: failed to create true negative combined file"
  exit 1
fi

# Data operations with Python scripts
# Merge and transform data
python3 "merge-transform-data.py"
# Check exit status and handle errors
if [ $? -ne 0 ]; then
  echo "Error: failed to merge and transform data"
  exit 1
fi

# End of script
echo "Script completed successfully"
exit 0
