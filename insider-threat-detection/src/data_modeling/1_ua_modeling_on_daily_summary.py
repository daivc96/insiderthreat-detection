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

# Read the device.csv file
device = pd.read_csv("device.csv")

# Convert the date column to datetime format
device["date"] = pd.to_datetime(device["date"])

# Extract the id, date, user, pc, activity columns
device = device[["id", "date", "user", "pc", "activity"]]

# Create a column for connection (1 if Connect, -1 if Disconnect, 0 otherwise)
device["connection"] = device["activity"].map({"Connect": 1, "Disconnect": -1}).fillna(0).astype(int)

# Read the file.csv file
file = pd.read_csv("file.csv")

# Convert the date column to datetime format
file["date"] = pd.to_datetime(file["date"])

# Extract the id, date, user, pc, activity columns
file = file[["id", "date", "user", "pc", "activity"]]

# Create a column for copy (1 if Copy, 0 otherwise)
file["copy"] = (file["activity"] == "Copy").astype(int)

# Create a column for write (1 if Write, 0 otherwise)
file["write"] = (file["activity"] == "Write").astype(int)

# Create a column for delete (1 if Delete, 0 otherwise)
file["delete"] = (file["activity"] == "Delete").astype(int)

# Create a column for open (1 if Open, 0 otherwise)
file["open"] = (file["activity"] == "Open").astype(int)

# Read the http.csv file
http = pd.read_csv("http.csv")

# Convert the date column to datetime format
http["date"] = pd.to_datetime(http["date"])

# Extract the id, date, user, pc, url columns
http = http[["id", "date", "user", "pc", "url"]]

# Create a column for access (1 if WWW Visit or WWW Download or WWW Upload)
http["access"] = (http["url"].notnull()).astype(int)

# Create a column for upload (1 if WWW Upload)
http["upload"] = (http["url"].str.contains("WWW Upload")).astype(int)

# Create a column for download (1 if WWW Download)
http["download"] = (http["url"].str.contains("WWW Download")).astype(int)

# Read the email.csv file
email = pd.read_csv("email.csv")

# Convert the date column to datetime format
email["date"] = pd.to_datetime(email["date"])

# Extract the id, date, user from email address columns
email = email[["id", "date", "user", "to", "cc", "bcc", "from", "size", "attachments", "content"]]

# Create a column for attachment (1 if attachments > 0)
email["attachment"] = (email["attachments"] > 0).astype(int)

# Create a column for send (1 if from is user's email address)
email["send"] = (email["from"] == email["user"]).astype(int)

# Create a column for receive (1 if to or cc or bcc contains user's email address)
email["receive"] = (email["to"].str.contains(email["user"]) | email["cc"].str.contains(email["user"]) | email["bcc"].str.contains(email["user"])).astype(int)

# Create a column for recipients (concatenate to, cc, and bcc columns)
email["recipients"] = email["to"].fillna("") + "," + email["cc"].fillna("") + "," + email["bcc"].fillna("")

# Create a column for internal recipients (count the number of recipients with the same domain as user's email address)
email["internal_recipients"] = email.apply(lambda x: x["recipients"].count(x["user"].split("@")[1]), axis=1)

# Read the ldap.csv file
ldap = pd.read_csv("ldap.csv")

# Extract the user_id, role, functional_unit, department, team columns
ldap = ldap[["user_id", "role", "functional_unit", "department", "team"]]

# Rename the user_id column to user
ldap = ldap.rename(columns={"user_id": "user"})

# Join the logon and device tables based on the id, date, user, and pc fields
logon_device = pd.merge(logon, device, on=["id", "date", "user", "pc"], how="outer")

# Join the logon_device and file tables based on the id field
logon_device_file = pd.merge(logon_device, file, on="id", how="outer")

# Join the logon_device_file and http tables based on the id field
logon_device_file_http = pd.merge(logon_device_file, http, on="id", how="outer")

# Join the logon_device_file_http and email tables based on the id field
logon_device_file_http_email = pd.merge(logon_device_file_http, email, on="id", how="outer")

# Join the logon_device_file_http_email and ldap tables based on the user field
logon_device_file_http_email_ldap = pd.merge(logon_device_file_http_email, ldap, on="user", how="outer")

# Group by user and date
grouped = logon_device_file_http_email_ldap.groupby(["user", "date"])

# Aggregate by counting or summing the values of interest
output = grouped.agg(
    numlogonDay = ("logonoff_x", lambda x: x[x > 0].sum()),
    numlogonNight = ("logonoff_x", lambda x: x[x > 0].sum()),
    numlogoffDay = ("logonoff_x", lambda x: -x[x < 0].sum()),
    numlogoffNight = ("logonoff_x", lambda x: -x[x < 0].sum()),
    numPClogonDay = ("pc_x", lambda x: x.nunique()),
    numPClogonNight = ("pc_x", lambda x: x.nunique()),
    numPClogoffDay = ("pc_x", lambda x: x.nunique()),
    numPClogoffNight = ("pc_x", lambda x: x.nunique()),
    onoffNotsameDay = ("pc_x", lambda x: (x != x.shift()).sum()),
    onoffNotsameNight = ("pc_x", lambda x: (x != x.shift()).sum()),
    numPCwithUSBDay = ("pc_y", lambda x: x.nunique()),
    numPCwithUSBNight = ("pc_y", lambda x: x.nunique()),
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
    numWebAccDay = ("access", lambda x: x[x > 0].sum()),
    numWebAccNight = ("access", lambda x: x[x > 0].sum()),
    numURLAccessedDay = ("url", lambda x: x.nunique()),
    numURLAccessedNight = ("url", lambda x: x.nunique()),
    numUploadDay = ("upload", lambda x: x[x > 0].sum()),
    numUploadNight = ("upload", lambda x: x[x > 0].sum()),
    numDownloadDay = ("download", lambda x: x[x > 0].sum()),
    numDownloadNight = ("download", lambda x: x[x > 0].sum()),
    numAttachmentDay = ("attachment", lambda x: x[x > 0].sum()),
    numAttachmentNight = ("attachment", lambda x: x[x > 0].sum()),
    numSendDay = ("send", lambda x: x[x > 0].sum()),
    numSendNight = ("send", lambda x: x[x > 0].sum()),
    numReceiveDay = ("receive", lambda x: x[x > 0].sum()),
    numReceiveNight = ("receive", lambda x: x[x > 0].sum()),
    numEmailSentwithAttachDay = ("send", lambda x: (x * email["attachment"]).sum()),
    numEmailSentwithAttachNight = ("send", lambda x: (x * email["attachment"]).sum()),
    numEmailReceivedwithAttachDay = ("receive", lambda x: (x * email["attachment"]).sum()),
    numEmailReceivedwithAttachNight = ("receive", lambda x: (x * email["attachment"]).sum()),
    numdistinctRecipientsDay = ("recipients", lambda x: len(set(x.sum().split(",")))),
    numdistinctRecipientsNight = ("recipients", lambda x: len(set(x.sum().split(",")))),
    numinternalRecipientsDay = ("internal_recipients", "sum"),
    numinternalRecipientsNight = ("internal_recipients", "sum"),
    role = ("role", "first"),
    functional_unit = ("functional_unit", "first"),
    department = ("department", "first"),
    team = ("team", "first")
)

# Reset the index
output = output.reset_index()

# Write the output csv file
output.to_csv("output.csv", index=False)
