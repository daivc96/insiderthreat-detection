import pandas as pd

# Read the device.csv file
device = pd.read_csv("device.csv")

# Convert the date column to datetime format
device["date"] = pd.to_datetime(device["date"])

# Extract the user, date, pc, and activity columns
device = device[["user", "date", "pc", "activity"]]

# Create a column for working day (1 if Monday to Friday, 0 otherwise)
device["workingday"] = device["date"].dt.dayofweek.isin([0, 1, 2, 3, 4]).astype(int)

# Create a column for day or night (1 if 8 AM to 6 PM, 0 otherwise)
device["daynight"] = device["date"].dt.hour.isin(range(8, 18)).astype(int)

# Create a column for connection (1 if Connect, -1 if Disconnect, 0 otherwise)
device["connection"] = device["activity"].map({"Connect": 1, "Disconnect": -1}).fillna(0).astype(int)

# Read the file.csv file
file = pd.read_csv("file.csv")

# Convert the date column to datetime format
file["date"] = pd.to_datetime(file["date"])

# Extract the user, date, pc, and activity columns
file = file[["user", "date", "pc", "activity"]]

# Create a column for copy (1 if Copy, 0 otherwise)
file["copy"] = (file["activity"] == "Copy").astype(int)

# Create a column for write (1 if Write, 0 otherwise)
file["write"] = (file["activity"] == "Write").astype(int)

# Create a column for delete (1 if Delete, 0 otherwise)
file["delete"] = (file["activity"] == "Delete").astype(int)

# Create a column for open (1 if Open, 0 otherwise)
file["open"] = (file["activity"] == "Open").astype(int)

# Join the device and file tables based on the user and date fields
device_file = pd.merge(device, file, on=["user", "date"], how="outer")

# Group by user and date
grouped = device_file.groupby(["user", "date"])

# Aggregate by counting or summing the values of interest
output = grouped.agg(
    numPCwithUSBDay = ("pc_x", lambda x: x.nunique()),
    numPCwithUSBNight = ("pc_x", lambda x: x.nunique()),
    numConnectionDay = ("connection", lambda x: x[x > 0].sum()),
    numConnectionNight = ("connection", lambda x: x[x > 0].sum()),
    numCopy2DeviceDay = ("copy_x", lambda x: x[x > 0].sum()),
    numCopy2DeviceNight = ("copy_x", lambda x: x[x > 0].sum()),
    numWrite2DeviceDay = ("write_x", lambda x: x[x > 0].sum()),
    numWrite2DeviceNight = ("write_x", lambda x: x[x > 0].sum()),
    numCopyFromDeviceDay = ("copy_x", lambda x: -x[x < 0].sum()),
    numCopyFromDeviceNight = ("copy_x", lambda x: -x[x < 0].sum()),
    numWriteFromDeviceDay = ("write_x", lambda x: -x[x < 0].sum()),
    numWriteFromDeviceNight = ("write_x", lambda x: -x[x < 0].sum()),
    numDelFromDeviceDay = ("delete_x", lambda x: -x[x < 0].sum()),
    numDelFromDeviceNight = ("delete_x", lambda x: -x[x < 0].sum()),
    numOpenOnPCDay = ("open_x", lambda x: -x[x < 0].sum()),
    numOpenOnPCNight = ("open_x", lambda x: -x[x < 0].sum()),
    workingday = ("workingday_x", "first")
)

# Reset the index
output = output.reset_index()

# Write the output csv file
output.to_csv("output_device_file.csv", index=False)
