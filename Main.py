# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 13:18:23 2022

@author: joefo
"""
import tensorflow as tf
import pandas as pd
import numpy as np

dataset = pd.read_csv(r'C:\Users\joefo\OneDrive\Desktop\NeuralNetworks\ChurnModel\Churn_Modelling.csv')

X = dataset.iloc[:, 3:-1].values #Removing parts of the csv file not pertinent to the analysis. 
#Starting from column 4 to snd to last column
y = dataset.iloc[:, -1].values #output actual
print(X)
print(y)

# Encoding categorical data
# Label Encoding the "Gender" column
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
X[:, 2] = le.fit_transform(X[:, 2])
print(X)
# One Hot Encoding the "Geography" column
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [1])], remainder='passthrough')
X = np.array(ct.fit_transform(X))
print(X)
#Dummy Variables encoded
#France [1,0,0]
#Germany [0,1,0]
#Spain [0,0,1]

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Feature Scaling-Fundamntal for deep learning
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Part 2 - Building the ANN

# Initializing the ANN
ann = tf.keras.models.Sequential()

# Adding the input layer and the first hidden layer
ann.add(tf.keras.layers.Dense(units=6, activation='relu')) #rectified linear activation function
#f(x) = max(0,x), more computationally efficient
#units-number of neurons (input layer)

# Adding the second hidden layer
ann.add(tf.keras.layers.Dense(units=6, activation='relu')) #rectified linear activation function
#ReLU function does not activate all the neurons at the same time. 

# Adding the output layer
ann.add(tf.keras.layers.Dense(units=1, activation='sigmoid')) #Logistic
#f(x) = 1 / 1+e^-x

# Part 3 - Training the ANN

# Compiling the ANN
#Adam is a stochastic gradient descent optimization method
'''
Loss function: Entropy is a measure of the uncertainty associated with
a given distribution q(y).
    
H_p(q) = -1/n /sum^n_{i=1} y_i * log(p(y_i)) + (1-y_i) * log(1-p(y_i))

If we compute entropy like above, we are actually computing the cross-entropy 
between both distributions.

cross-entropy will have a BIGGER value than the entropy computed on the true distribution.
 
 H_p(q)-H(q) >= 0
 Daniel Godoy-Understanding binary cross-entropy / log loss: a visual explanation
'''
ann.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Training the ANN on the Training set
ann.fit(X_train, y_train, batch_size = 32, epochs = 100)

# Part 4 - Making the predictions and evaluating the model

# Predicting the result of a single observation

"""
Homework:
Use our ANN model to predict if the customer with the following informations will leave the bank: 
Geography: France
Credit Score: 600
Gender: Male
Age: 40 years old
Tenure: 3 years
Balance: $ 60000
Number of Products: 2
Does this customer have a credit card? Yes
Is this customer an Active Member: Yes
Estimated Salary: $ 50000
So, should we say goodbye to that customer?

Solution:
"""

print(ann.predict(sc.transform([[1, 0, 0, 600, 1, 40, 3, 60000, 2, 1, 1, 50000]])) > 0.5)

"""
Therefore, our ANN model predicts that this customer stays in the bank!
Important note 1: Notice that the values of the features were all input in a double pair of square brackets. That's because the "predict" method always expects a 2D array as the format of its inputs. And putting our values into a double pair of square brackets makes the input exactly a 2D array.
Important note 2: Notice also that the "France" country was not input as a string in the last column but as "1, 0, 0" in the first three columns. That's because of course the predict method expects the one-hot-encoded values of the state, and as we see in the first row of the matrix of features X, "France" was encoded as "1, 0, 0". And be careful to include these values in the first three columns, because the dummy variables are always created in the first columns.
"""

# Predicting the Test set results
y_pred = ann.predict(X_test)
y_pred = (y_pred > 0.5)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)
print(accuracy_score(y_test, y_pred))
