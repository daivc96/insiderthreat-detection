# Insider Threat Detection

This project aims to detect insider threats in an organization using machine learning techniques. Insider threats are malicious activities performed by authorized users of a system or network, such as employees, contractors, or partners. Insider threats can cause significant damage to an organization, such as data theft, sabotage, fraud, or espionage.

## Data

The data used for this project is the CERT synthetic dataset, which is a realistic simulation of insider threat scenarios. The dataset contains various types of data collected from a fictitious company, such as email, file, device, HTTP, logon, and psychometric data. The dataset also provides ground truth labels for the malicious users and their actions.

## Requirements

To run this project, the following dependencies need installed:

- Python 3.8 or higher
- scikit-learn
- TensorFlow
- pandas
- numpy
- matplotlib
- seaborn

Installation command:

`pip install -r requirements.txt`

## Usage

To run this project, execute below commands at root path

### Preprocessing
`bash src/preprocessing/main.sh`

### Feature Engineering
`bash src/feature_engineering/main.sh`

### Model Training
`bash src/feature_engineering/main.sh`