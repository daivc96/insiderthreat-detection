# Insider Threat Detection

This project aims to detect insider threats in an organization using machine learning techniques. Insider threats are malicious activities performed by authorized users of a system or network, such as employees, contractors, or partners. Insider threats can cause significant damage to an organization, such as data theft, sabotage, fraud, or espionage.

## Data

The data used for this project is the [CERT synthetic dataset], which is a realistic simulation of insider threat scenarios. The dataset contains various types of data collected from a fictitious company, such as email, file, device, HTTP, logon, and psychometric data. The dataset also provides ground truth labels for the malicious users and their actions.

## Methodology

The methodology of this project consists of four main steps:

- Data preprocessing: This step involves cleaning, filtering, and transforming the raw data into a suitable format for analysis and modeling. This includes handling missing values, outliers, and imbalanced classes.
- Feature engineering: This step involves extracting and selecting relevant features from the preprocessed data using various statistical methods and domain knowledge. This also includes reducing dimensionality and creating new features based on existing ones.
- Model training: This step involves building and training machine learning models to classify users as malicious or benign based on their behavior patterns. This includes using different techniques, such as random forest, XGBoost, and LSTM.
- Model evaluation: This step involves evaluating the performance of the trained models using various metrics, such as accuracy, precision, recall, F1-score, ROC curve, and AUC score. This also includes comparing the results of different models and discussing the advantages and limitations of each approach.

## Results

The results of this project show that machine learning techniques can effectively detect insider threats in an organization based on user behavior data. The best performing model is the LSTM model, which achieves an accuracy of 0.97, a precision of 0.95, a recall of 0.96, an F1-score of 0.96, and an AUC score of 0.99. The LSTM model can capture the temporal and sequential patterns of user actions and identify anomalous or suspicious behavior.

## Presentation

You can find the presentation slides for this project [here], which provide more details and insights about the data analysis and modeling process.

## Requirements

To run this project, you need to install the following dependencies:

- Python 3.8 or higher
- scikit-learn
- TensorFlow
- pandas
- numpy
- matplotlib
- seaborn

You can install them using the command:

`pip install -r requirements.txt`

## Usage

To run this project, you need to execute the main.py file using the command:

`python main.py`

This will run the entire pipeline from data preprocessing to model evaluation and display the results in the console.
