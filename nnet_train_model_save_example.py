import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument('--output_col', type=str, help='name of output column', default=None)
# args = parser.parse_args()
baseline_features = pd.read_csv("data/processed/baseline_features.csv", index_col=0)
output_columns = pd.read_csv("data/processed/output_columns.csv", index_col=0) 

# 23503 x 1470 columns
baseline_features.head()
# 23503 x 6 columns
output_columns.head()

# Specific column to be tested on.
main_output_column = output_columns[["S3CLASSES", "STU_ID"]]

# Merge into a baseline and output into a single column
df = pd.merge(baseline_features, main_output_column, on='STU_ID')

# Remove rows w/ NaN values in the output column
df = df.dropna(axis=0, subset=main_output_column.columns)

# Create the x and y columns
baseline_features_final = df[baseline_features.columns]
baseline_features_final = baseline_features_final.drop(['STU_ID'], axis=1)
output_columns_final = df[main_output_column.columns] 
output_columns_final = output_columns_final.drop(['STU_ID'],axis=1)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
output_columns_final = sc.fit_transform(output_columns_final)

# Splitting the data set into the Training and Testing set
import tensorflow as tf
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(baseline_features_final, output_columns_final, test_size = 0.2)


# Importing the Keras libraries and packages
import keras
from keras.models import Sequential
from keras.layers import Dense

# Initialising the ANN
classifier = Sequential()

# import pdb 
# pdb.set_trace()

import numpy as np
# Adding the input layer and the first hidden layer
classifier.add(Dense(output_dim = 6, init = 'uniform', activation = 'relu'))

# Adding the second hidden layer
classifier.add(Dense(output_dim = 6, init = 'uniform', activation = 'relu'))

# Adding the output layer
classifier.add(Dense(output_dim = 1, init = 'uniform', activation = 'sigmoid'))

# Compiling the ANN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])


# TO-DO: Cross-validation over hyperparameters, understand the X_train scaler, graph of the error (plot)
# Error on validation set vs error on the training set (plot)
# Snakefile, must repeat multiple output column -> set workflow
# pip install h5py <- install this

epoch100 = 1
if os.dir("model/version1/epoch_"+str(epoch100*100)+".json"):
    # run the 100 epochs

# Fitting the ANN to the Training set
for epoch100 in range(1,300):
    if os.dir("model/version1/epoch_"+str(epoch100*100)+".json"):
        next
    else:
        # load the model for the previous epoch iteration <-- because weights and biases
        # load classifier from json file
        json_file = open('classifier.json', 'r')
        classifier_json = json_file.read()
        json_file.close()
        classifier = classifier_from_json(classifier_json)
        # load weights and biases from hd5 file
        classifier.load_weights("classifier.h5")
        print("Loaded classifier from disk")
        # continue with the code

    classifier.fit(X_train.values, y_train, batch_size = 10, nb_epoch = 100, vaidation_split=0.3)
    classifier_json = classifier.to_json()
    with open("classifier.json", "w") as json_file:
        json_file.write(classifier_json)
    classifier.save_weights("classifier.h5")

    # ... save model to: model/version1/epoch_"+str(epoch100*100)+".json"
    # ... save accuracy  / loss / cross validation accuracy and cross validation loss into SAME csv 

# Part 3 - Making the predictions and evaluating the model

# Predicting the Test set results
y_pred = classifier.predict(X_test)
y_pred = (y_pred > 0.5)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)