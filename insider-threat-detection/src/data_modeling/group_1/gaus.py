import pandas as pd
import numpy as np
from scipy.stats import norm

# Load your data into a pandas DataFrame
data = pd.read_csv("your_data.csv")

# List of variables to consider
variables = ["variable1", "variable2", "variable3", ...]

# Significance level
alpha = 0.1

# List to store selected variables
selected_variables = []

# Iterate over each variable
for var in variables:
    # Estimate mean and standard deviation
    mean = data[var].mean()
    std = data[var].std()

    # Calculate critical values for rejection region
    lower_bound = norm.ppf(alpha / 2, mean, std)
    upper_bound = norm.ppf(1 - alpha / 2, mean, std)

    # Check if any abnormal activity is in the rejection region
    abnormal_activities = data[data["label"] == "abnormal"][var]
    if any((abnormal_activities < lower_bound) | (abnormal_activities > upper_bound)):
        selected_variables.append(var)

# Print selected variables
print("Selected variables for anomaly detection modeling:", selected_variables)
