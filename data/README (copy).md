# Intro

This project was made by Lou DURON and Etienne BARDET as a assignment of the Datamining course of the Bioinformatics Master Degree of Paul-Sabatier University. The goal of this projet is to create and evaluate an annotation method in terms of ABC transporters in procaryote complete genomes.

# Documentation

## Data_preparation.py

**Usage :** Data_preparation.py -u [USER_NAME] -p [PASSWORD] [OPTION]  
Create .csv file(s) from the database for annotation method training and testing.

**Mandatory arguments :**  
  *-u, --user=STRING*   username for the mysql database  
  -p, --password=STRING   password for the mysql database 
  
**Optional arguments :**  
  -a, --abc   creates a .csv file for the ABC annotation (abc.csv)  
  -b, --sub   creates a .csv file for the ABC subfamilies annotation (subfamilies.csv)  
  -s, --score=30   minimal score for domain recovery  
  -n, --nb_domain=10    minimal number of occurence in gene dataset of each domains  
  
**Example of use:** ./Data_parser.py -u username -p pwd -s 40 -n 10 -a -b  
Will keep only conserved domains having a score > 40 that appears in at least 10 genes  
With this setting, will create 2 csv file :
- abc.csv : for the prediction abc-type genes
- subfamilies.csv : for the prediction of abc subfamilies


## Annotation.py

**Usage :** Annotation.py -d [FILE] [OPTION]  
Creates and evaluates classification models for abc and abc subfamilies annotation

**Mandatory arguments :**  
  -d, --data   .csv file with dataset (abc.csv for abc annotation and subfamilies.csv for subfamilies annotation)
  
**Optional arguments :**  
  -t, --tree    decision tree algorithm  
  -g, --gaussian    gaussian naive Bayes algorithm  
  -b, --bernoulli   bernoulli naive Bayes algorithm  
  -s, --trainsize=0.8   proportion of dataset used for model training  
  -p, --precision   add precision evaluation for binary class data (only for abc annotation, not abc subfamilies with is multiclass)  

**Example of use:** ./Annotation.py -d ../data.preparation/abc.csv -s 0.7 -t -g -b -p  
Will train 3 models, using Decision tree (-t) and Naives Bayes models (-g for gaussian and -b for Bernoulli),  
on 70% of the data then predict the classes of the remaining 30%.  
Then for each model, it will give the accuracy and the precision (only binary class) of the prediction



