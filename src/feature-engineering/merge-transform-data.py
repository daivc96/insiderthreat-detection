# Import pandas library
import pandas as pd
# Import datetime library
import datetime

# Define the file names
file1 = "data/scenario2-processing/scenario2-truenegative-data.csv"
file2 = "data/scenario2-processing/scenario2-truepositive-data.csv"

# Define the column names
columns = ["vector", "id", "date", "user", "source", "action"]

# Read the CSV files without header
df1 = pd.read_csv(file1, header=None, names=columns, usecols=[0, 1, 2, 3, 4, 5])
df2 = pd.read_csv(file2, header=None, names=columns, usecols=[0, 1, 2, 3, 4, 5])

# Add the InsiderThreat column with False for file1 and True for file2
df1["insiderthreat"] = False
df2["insiderthreat"] = True

# Concatenate the two data frames
df = pd.concat([df1, df2], ignore_index=True)

# Convert the Date column to Epoch integer
df["date"] = df["date"].apply(lambda x: int(datetime.datetime.strptime(x, "%m/%d/%Y %H:%M:%S").timestamp()))

# Replace the Vector values with numeric values
df["vector"] = df["vector"].replace({"http": 0, "email": 1, "device": 2, "logon": 3})

df = df [ ["insiderthreat", "vector", "date", "user", "source", "action"]]
# # Save the result to a new CSV file
# df.to_csv("data/scenario2-processing/combined-transformed.csv", index=False)

df["user"] = df["user"].astype('category')
df["source"] = df["source"].astype('category')
df["action"] = df["action"].astype('category')
df["user_cat"] = df["user"].cat.codes
df["source_cat"] = df["source"].cat.codes
df["action_cat"] = df["action"].cat.codes

#print(df.info())
#print(df.head())

#save df with new columns for future datmapping
# df.to_csv('df-export-allcolumns.csv')

#remove old columns
del df["user"]
del df["source"]
del df["action"]
#restore original names of columns
df.rename(columns={"user_cat": "user", "source_cat": "source", "action_cat": "action"}, inplace=True)
print(df.head())
print(df.info())

#save df cleaned up
df.to_csv('data/scenario2-output/df-export-int-cleaned.csv')
