import pandas as pd

# Read the http.csv file
http = pd.read_csv("http_truncated.csv")

# Convert the date column to datetime format
http["date"] = pd.to_datetime(http["date"])

# Extract the user, date, pc, url columns
http = http[["user", "date", "pc", "url"]]

# # Create a column for working day (1 if Monday to Friday, 0 otherwise)
# http["workingday"] = http["date"].dt.dayofweek.isin([0, 1, 2, 3, 4]).astype(int)

# Create a column for day or night (1 if 8 AM to 6 PM, 0 otherwise)
http["daynight"] = http["date"].dt.hour.isin(range(8, 18)).astype(int)

# Create a column for access (1 if WWW Visit or WWW Download or WWW Upload)
http["access"] = (http["url"].notnull()).astype(int)

# Create a column for upload (1 if WWW Upload)
http["upload"] = (http["url"].str.contains("WWW Upload")).astype(int)

# Create a column for download (1 if WWW Download)
http["download"] = (http["url"].str.contains("WWW Download")).astype(int)

# Group by user and date
grouped = http.groupby(["user", "date"])

# Aggregate by counting or summing the values of interest
output = grouped.agg(
    numWebAccDay = ("access", lambda x: x[x > 0].sum()),
    numWebAccNight = ("access", lambda x: x[x > 0].sum()),
    numURLAccessedDay = ("url", lambda x: x.nunique()),
    numURLAccessedNight = ("url", lambda x: x.nunique()),
    numUploadDay = ("upload", lambda x: x[x > 0].sum()),
    numUploadNight = ("upload", lambda x: x[x > 0].sum()),
    numDownloadDay = ("download", lambda x: x[x > 0].sum()),
    numDownloadNight = ("download", lambda x: x[x > 0].sum())
)

# Reset the index
output = output.reset_index()

# Write the output csv file
output.to_csv("output_http.csv", index=False)
