import pandas as pd

# Read the email.csv file
email = pd.read_csv("email.csv")

# Convert the date column to datetime format
email["date"] = pd.to_datetime(email["date"])

# Extract the user from email address columns
email = email[["user", "date", "to", "cc", "bcc", "from", "size", "attachments", "content"]]

# Create a column for working day (1 if Monday to Friday, 0 otherwise)
email["workingday"] = email["date"].dt.dayofweek.isin([0, 1, 2, 3, 4]).astype(int)

# Create a column for day or night (1 if 8 AM to 6 PM, 0 otherwise)
email["daynight"] = email["date"].dt.hour.isin(range(8, 18)).astype(int)

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

# Group by user and date
grouped = email.groupby(["user", "date"])

# Aggregate by counting or summing the values of interest
output = grouped.agg(
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
    workingday = ("workingday", "first")
)

# Reset the index
output = output.reset_index()

# Write the output csv file
output.to_csv("output_email.csv", index=False)
