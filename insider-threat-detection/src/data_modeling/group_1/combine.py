import pandas as pd

# Read the output_logon.csv file
output_logon = pd.read_csv("output_logon.csv")

# Read the output_device_file.csv file
output_device_file = pd.read_csv("output_device_file.csv")

# Read the output_http.csv file
output_http = pd.read_csv("output_http.csv")

# Read the output_email.csv file
output_email = pd.read_csv("output_email.csv")

# Read the psychometric.csv file
psychometric = pd.read_csv("psychometric.csv")

# Extract the user_id, O, C, E, A, N columns
psychometric = psychometric[["user_id", "O", "C", "E", "A", "N"]]

# Rename the user_id column to user
psychometric = psychometric.rename(columns={"user_id": "user"})

# Read the ldap.csv file
ldap = pd.read_csv("ldap.csv")

# Extract the user_id, role, functional_unit, department, team columns
ldap = ldap[["user_id", "role", "functional_unit", "department", "team"]]

# Rename the user_id column to user
ldap = ldap.rename(columns={"user_id": "user"})

# Join the output_logon and output_device_file tables based on user and date
output_logon_device_file = pd.merge(output_logon, output_device_file, on=["user", "date"], how="outer")

# Join the output_logon_device_file and output_http tables based on user and date
output_logon_device_file_http = pd.merge(output_logon_device_file, output_http, on=["user", "date"], how="outer")

# Join the output_logon_device_file_http and output_email tables based on user and date
output_logon_device_file_http_email = pd.merge(output_logon_device_file_http, output_email, on=["user", "date"], how="outer")

# Join the output_logon_device_file_http_email and psychometric tables based on user
output_logon_device_file_http_email_psychometric = pd.merge(output_logon_device_file_http_email, psychometric, on="user", how="outer")

# Join the output_logon_device_file_http_email_psychometric and ldap tables based on user
output_final = pd.merge(output_logon_device_file_http_email_psychometric, ldap, on="user", how="outer")

# Write the final output csv file
output_final.to_csv("output_final.csv", index=False)
