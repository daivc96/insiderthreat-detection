# Insider Threat Detection

This project aims to simulate the tutorial named "Insider Threat Detection with AI Using Tensorflow and RepidMiner Studio"

## Repo Structure

- data: all data used for scenario 2 insider threat detection, including all true positive and true negative data
- src: bash scripts and Python scripts used for some phases of AI life cycle including preprocessing, feature engineering and model training
- results: all results proving the project works

## Tools Setup

- Download the datasets from website: https://kilthub.cmu.edu/articles/dataset/Insider_Threat_Test_Dataset/12841247/1
(ftp://ftp.sei.cmu.edu/pub/cert-data/ is not working anymore), store to project at **cert-12841247**/
- The data used for this project is the CERT synthetic dataset, which is a realistic simulation of insider threat scenarios. The dataset contains various types of data collected from a fictitious company, such as email, file, device, HTTP, logon data,... . The dataset also provides ground truth labels for the malicious users and their actions.
- Install RapidMiner Studio
- The following dependencies need installed:, Python 3.8 or higher, scikit-learn, TensorFlow, pandas, numpy, matplotlib, seaborn.
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