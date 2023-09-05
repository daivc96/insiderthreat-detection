import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from pandas.api.types import CategoricalDtype

file = "data/scenario2_processed/df-export-int-cleaned.csv"

# Read the CSV files
dataframe = pd.read_csv(file)

# Split the dataframe into train, validation, and test
train, test = train_test_split(dataframe, test_size=0.2)
train, val = train_test_split(train, test_size=0.2)
print(len(train), 'train examples')
print(len(val), 'validation examples')
print(len(test), 'test examples')

num_samples = len(train)

# Create an input pipeline using tf.data
# A utility method to create a tf.data dataset from a Pandas Dataframe


def df_to_dataset(dataframe, shuffle=True, batch_size=32):
    dataframe = dataframe.copy()
    labels = dataframe.pop('insiderthreat')
    ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(dataframe))
    ds = ds.batch(batch_size)
    return ds


# choose columns needed for calculations (features)
feature_columns = []
num_features = 5 #"vector", "date", "user", "source", "action"
for header in ["vector", "date", "user", "source", "action"]:
    feature_columns.append(feature_column.numeric_column(header))

# create feature layer
feature_layer = tf.keras.layers.DenseFeatures(feature_columns)

# set batch size pipeline
batch_size = 32
train_ds = df_to_dataset(train, batch_size=batch_size)
val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)

# create compile and train model
# model = tf.keras.Sequential([
#     feature_layer,
#     layers.Dense(128, activation='relu'),
#     layers.Dense(128, activation='relu'),
#     layers.Dense(1)
# ])

# model.compile(optimizer='adam',
#               loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
#               metrics=['accuracy'])

# model.fit(train_ds,
#           validation_data=val_ds,
#           epochs=5)

# Reshape data to be (num_samples, sqrt(num_features), sqrt(num_features), 1)
# This is a square reshaping suitable for CNN
sqrt_features = int(np.sqrt(num_features))
X_train_reshaped = train_ds.reshape(num_samples, sqrt_features, sqrt_features, 1)

# Construct the hybrid CNN-MLP model
# model = keras.Sequential()
model = tf.keras.Sequential([
    feature_layer
])

# CNN layers
model.add(layers.Conv2D(32, (3,3), activation='relu', input_shape=(sqrt_features, sqrt_features, 1)))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(64, (3,3), activation='relu'))
model.add(layers.MaxPooling2D((2,2)))

# Flatten and feed into MLP
model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(1, activation='sigmoid'))  # Binary classification

# Compile and train
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train_reshaped, y_train, epochs=10, batch_size=32, validation_split=0.2)
loss, accuracy = model.evaluate(test_ds)
print("Accuracy", accuracy)