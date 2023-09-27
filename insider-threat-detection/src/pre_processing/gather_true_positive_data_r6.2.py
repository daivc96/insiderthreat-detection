# __author__ = "Vo Chanh Dai"
# __doc__ = "This code gathers true positive data from cert data r6.2"

# Import the pandas library
import pandas as pd

# Source files and destination file are predefined

source_file_path = "../../data/raw/answers/r6.2-*.csv"
destination_file_path = "../../data/processed/true_positive_r6.2.csv"

# Create an empty list to store the data frames
data_frames = []

# Loop through all the csv files that start with r6.2-
import glob
for file in glob.glob(source_file_path):
    # Read the csv file without headers and select only the second column (index 1)
    df = pd.read_csv(file, header=None, usecols=[1])
    # Append the data frame to the list
    data_frames.append(df)

# Concatenate all the data frames in the list
combined_df = pd.concat(data_frames, ignore_index=True)

# Add a new column named "target" with a constant value of 1
combined_df = combined_df.assign(target=1)

# Save the combined data frame to a new csv file with headers "id" and "target"
combined_df.to_csv(destination_file_path, index=False, header=["id", "target"])
