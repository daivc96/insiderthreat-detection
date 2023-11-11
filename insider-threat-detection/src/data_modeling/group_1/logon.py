import pandas as pd

# Read the logon.csv file
logon = pd.read_csv("logon.csv")

# Convert the date column to datetime format
logon["date"] = pd.to_datetime(logon["date"])

# Extract the user, date, pc, and activity columns
logon = logon[["user", "date", "pc", "activity"]]

# Create a column for working day (1 if Monday to Friday, 0 otherwise)
logon["workingday"] = logon["date"].dt.dayofweek.isin([0, 1, 2, 3, 4]).astype(int)

# Create a column for day or night (1 if 8 AM to 6 PM, 0 otherwise)
logon["daynight"] = logon["date"].dt.hour.isin(range(8, 18)).astype(int)

# Create a column for logon or logoff (1 if Logon or Unlock, -1 if Logoff, 0 otherwise)
logon["logonoff"] = logon["activity"].map({"Logon": 1, "Unlock": 1, "Logoff": -1}).fillna(0).astype(int)

# Group by user and date
grouped = logon.groupby(["user", "date"])

# Aggregate by counting or summing the values of interest
output = grouped.agg(
    numlogonDay = ("logonoff", lambda x: x[x > 0].sum()),
    numlogonNight = ("logonoff", lambda x: x[x > 0].sum()),
    numlogoffDay = ("logonoff", lambda x: -x[x < 0].sum()),
    numlogoffNight = ("logonoff", lambda x: -x[x < 0].sum()),
    numPClogonDay = ("pc", lambda x: x.nunique()),
    numPClogonNight = ("pc", lambda x: x.nunique()),
    numPClogoffDay = ("pc", lambda x: x.nunique()),
    numPClogoffNight = ("pc", lambda x: x.nunique()),
    onoffNotsameDay = ("pc", lambda x: (x != x.shift()).sum()),
    onoffNotsameNight = ("pc", lambda x: (x != x.shift()).sum())
)

# Reset the index
output = output.reset_index()

# Write the output csv file
output.to_csv("output_logon.csv", index=False)
