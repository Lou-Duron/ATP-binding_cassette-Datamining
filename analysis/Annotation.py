#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas
import argparse
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score

################################################################################################
parser = argparse.ArgumentParser(description='Annotation')
parser.add_argument('--data', '-d', type=str, help="data file, format : csv")
parser.add_argument('--trainsize', '-s', type=float, default=float(0.8), help="Size of trainning set (default : 0.8)")
parser.add_argument('--tree', '-t', required=False, action="store_true", help='Decision Tree algorithm')
parser.add_argument('--gaussian', '-g', required=False, action="store_true", help='Gaussian Naive Bayes algorithm')
parser.add_argument('--bernoulli', '-b', required=False, action="store_true", help='Bernoulli Naive Bayes algorithm')
parser.add_argument('--precision', '-p', required=False, action="store_true", help='Return the precision of the prediction, only for binary data like prediction of abc type genes')
'''
Example of use: ./Classification.py -d ../data.preparation/abc.csv -s 0.7 -t -g -b -p
Will train 3 models, using Decision tree (-t) and Naives Bayes models (-g for gaussian and -b for Bernoulli),
on 70% of the data then predict the classes of the remaining 30%.
Then for each model, it will give the accuracy and the precision (only binary classes) of the prediction
'''
args = parser.parse_args()
################################################################################################

# Dataframe setup
df = pandas.read_csv(args.data)
data = df[["Length", "MSD_associated_domains", "NMD_associated_domains", "SBP_associated_domains"]]
classes = df["class"]

# Split of the matrix into random train and test subsets
X_train, X_test, y_train, y_test = train_test_split(data, classes, train_size=args.trainsize)
multiclass = False
for el in y_test:
  if el != 0 and el != 1:
    multiclass = True

# Decision tree algorithm
if args.tree :
  t = tree.DecisionTreeClassifier()
  t.fit(X_train, y_train) # Training
  t_prediction =  t.predict(X_test) # Prediction
  t_accuracy = accuracy_score(y_test, t_prediction)*100 # Evaluation
  print("Decision Tree algorithm :")
  print("Accuracy : " + str(round(t_accuracy,2)) + "%")
  if args.precision:
    if multiclass == False:
      t_precision = precision_score(y_test, t_prediction, average='binary')*100
      print("Precision : " + str(round(t_precision,2)) + "%")
  print("\n")

# Gaussian Naive Bayes algorithm
if args.gaussian :
    gaussian_model = GaussianNB()
    gaussian_model.fit(X_train, y_train) # Training
    g_prediction =  gaussian_model.predict(X_test) # Prediction
    g_accuracy = accuracy_score(y_test, g_prediction)*100 # Evaluation
    print("Gaussian Naive Bayes algorithm :")
    print("Accuracy : " + str(round(g_accuracy,2)) + "%")
    if args.precision:
      if multiclass == False:
        g_precision = precision_score(y_test, g_prediction, average='binary')*100
        print("Precision : " + str(round(g_precision,2)) + "%")
    print("\n")

# Bernoulli Naive Bayes algorithm
if args.bernoulli :
  bernoulli_model = BernoulliNB()
  bernoulli_model.fit(X_train, y_train) # Training
  b_prediction =  bernoulli_model.predict(X_test) # Prediction
  b_accuracy = accuracy_score(y_test, b_prediction)*100 # Evaluation
  print("Bernoulli Naive Bayes algorithm :")
  print("Accuracy : " + str(round(b_accuracy,2)) + "%")
  if args.precision:
    if multiclass == False:
      b_precision = precision_score(y_test, b_prediction, average='binary')*100
      print("Precision : " + str(round(b_precision,2)) + "%")
  print("\n")