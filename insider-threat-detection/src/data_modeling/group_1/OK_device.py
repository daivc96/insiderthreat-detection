# Import modules
import pandas as pd

# Read the device_truncated.csv file
device = pd.read_csv("device.csv")

# Convert the date column to datetime format
device["date"] = pd.to_datetime(device["date"])

# Extract the user, date, pc, and activity columns
device = device[["user", "date", "pc", "activity"]]

# Create a column for day or night (1 if 8 AM to 6 PM and Monday to Friday, 0 otherwise)
device["daynight"] = (device["date"].dt.hour.isin(range(8, 18)) & device["date"].dt.dayofweek.isin(range(5))).astype(int)
print(device["daynight"].unique())
# # Create a column for connection (1 if Connect, 0 if Disconnect, -1 otherwise)
# device["connection"] = device["activity"].map({"Connect": 1, "Disconnect": 0}).fillna(-1).astype(int)
device["connection"] = (device["activity"] == "Connect").astype(int)

# device["big_date"] = pd.to_datetime(device["date"])
device["big_date"] = pd.to_datetime(device["date"], format='%Y-%m-%d').dt.date

print(device)
# Read the file_truncated.csv file
file = pd.read_csv("file.csv")

# Convert the date column to datetime format
file["date"] = pd.to_datetime(file["date"])

# Extract the user, date, pc, and activity columns
file = file[["user", "date", "pc", "activity"]]

# Create a column for copy (1 if Copy, 0 otherwise)
file["copy"] = (file["activity"] == "File Copy").astype(int)

# Create a column for write (1 if Write, 0 otherwise)
file["write"] = (file["activity"] == "File Write").astype(int)

# Create a column for delete (1 if Delete, 0 otherwise)
file["delete"] = (file["activity"] == "File Delete").astype(int)

# Create a column for open (1 if Open, 0 otherwise)
file["open"] = (file["activity"] == "File Open").astype(int)
file["big_date"] = pd.to_datetime(file["date"], format='%Y-%m-%d').dt.date
print(file)
# Join the device and file tables based on the user and date fields
device_file = pd.merge(device, file, on=["user", "big_date"], how="outer")
print(device_file)




# Group by user and date
grouped = device_file.groupby(["user", "big_date"])

print(grouped)
# Define a function to calculate the output fields
def calculate_output_fields(group):
    # Get the day or night column
    daynight = group["daynight"]
    # Get the connection column
    connection = group["connection"]
    # Get the copy column
    copy = group["copy"]
    # Get the write column
    write = group["write"]
    # Get the delete column
    delete = group["delete"]
    # Get the open column
    open = group["open"]
    # Initialize the output fields
    output_fields = {}
    # Calculate the number of PC that uses USB device on working hours
    output_fields["numPCwithUSBDay"] = group.loc[daynight == 1, "pc_x"].nunique()
    # Calculate the number of PC that uses USB device on off-hours
    output_fields["numPCwithUSBNight"] = group.loc[daynight == 0, "pc_x"].nunique()
    # Calculate the number of connections with devices on working hours
    output_fields["numConnectionDay"] = connection[daynight == 1].sum().astype(int)
    # Calculate the number of connections with devices on off-hours
    output_fields["numConnectionNight"] = connection[daynight == 0].sum().astype(int)
    # Calculate the number of copied files from PC to devices on working hours
    output_fields["numCopy2DeviceDay"] = copy[daynight == 1].sum().astype(int)
    # Calculate the number of copied files from PC to devices on off-hours
    output_fields["numCopy2DeviceNight"] = copy[daynight == 0].sum().astype(int)
    # Calculate the number of written files from PC to devices on working hours
    output_fields["numWrite2DeviceDay"] = write[daynight == 1].sum().astype(int)
    # Calculate the number of written files from PC to devices on off-hours
    output_fields["numWrite2DeviceNight"] = write[daynight == 0].sum().astype(int)
    # Calculate the number of copied files from devices to PC on working hours
    output_fields["numCopyFromDeviceDay"] = copy[daynight == 1].sum().astype(int)
    # Calculate the number of copied files from devices to PC on off-hours
    output_fields["numCopyFromDeviceNight"] = copy[daynight == 0].sum().astype(int)
    # Calculate the number of files written from devices to PC on working hours
    output_fields["numWriteFromDeviceDay"] = write[daynight == 1].sum().astype(int)
    # Calculate the number of files written from devices to PC on off-hours
    output_fields["numWriteFromDeviceNight"] = write[daynight == 0].sum().astype(int)
    # Calculate the number of deleted files from devices on working hours
    output_fields["numDelFromDeviceDay"] = delete[daynight == 1].sum().astype(int)
    # Calculate the number of deleted files from devices on off-hours
    output_fields["numDelFromDeviceNight"] = delete[daynight == 0].sum().astype(int)
    # Calculate the number of opened files on working hours
    output_fields["numOpenOnPCDay"] = open[daynight == 1].sum().astype(int)
    # Calculate the number of opened files on off-hours
    output_fields["numOpenOnPCNight"] = open[daynight == 0].sum().astype(int)
    # Return the output fields as a series
    return pd.Series(output_fields)

# Apply the function to the grouped data
output = grouped.apply(calculate_output_fields)

# Print the output data
print(output)

# Save the output data to a CSV file
output.to_csv("device_file_output.csv")
