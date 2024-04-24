# This scripts creates and saved a machine learning model
# The model is a classification model
# To create the model you need to input data in the format of: string \t class
# You can run this script in the terminal: python3 classifier_kfold.py
# The script inputs training data found in the folder dataset/ 
# and outputs a model in the folder models/

import pickle
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

# Import dataset
df = pd.read_csv('dataset/bm_nn_genitive_phrases.csv', sep='\t',encoding='UTF-8',skipinitialspace=True,on_bad_lines='skip')   # columns names if no header

# Dataset has 2 columns
# Column 1: Bokmål sentences
# Column 2: Class

# Bokmål sentences that include genitives
x_data = df.iloc[:, 0] 

# Class values: 0, 1, 2, 3, 4.
# Meaning: -s=0, sine=1, preposisjon=2, sammenkrivning=3, omskriving=4
# Example:
# 0 = FNs miljøprogram (UNEP) -> FNs miljøprogram (UNEP)
# 1 = andres rettigheter -> andre sine rettigheter	1
# 2 = politiets nettside -> nettsidene til politiet
# 3 = FNs konferanse -> FN-konferansen
# 4 = kommunens plik -> kommunen har plikt til    NB! Denne kategorien inneholder litt forskjellig. Denne kategorien kan nyanseres om vi vil nyansere modellen mer.
y_data = df.iloc[:, -1] 

print("TRANSFORMING TEXT DATA ...")
vect = CountVectorizer(analyzer = 'char',ngram_range=(4,4)) # This is bag-of-words technique
x_data = vect.fit_transform(x_data)

print('\nTRAINING ...\n')

# We use k-fold cross validation
# We use a Logistic Regression model
scores=[]
kFold=KFold(n_splits=4,random_state=42,shuffle=True)
clf = LogisticRegression(solver="lbfgs",max_iter=400)

for train_index,test_index in kFold.split(x_data):
 #   print("Train Index: ", train_index, "\n")
  #  print("Test Index: ", test_index)
    
    X_train, X_test, y_train, y_test = x_data[train_index], x_data[test_index], y_data[train_index], y_data[test_index]
    clf.fit(X_train, y_train)
    scores.append(clf.score(X_test, y_test))

clf.fit(X_train,y_train)
scores.append(clf.score(X_test,y_test))

print('\nRESULTS:\n')

# Make predictions on the testing data
y_predict = clf.predict(X_test)

# Check results
print(confusion_matrix(y_test, y_predict))
print(classification_report(y_test, y_predict))

print("SCORES:", scores)
print("\nMEAN SCORES",np.mean(scores))
cross_val_score(clf, x_data, y_data, cv=10)

# Save model
print("SAVING MODEL ...")
model_pkl_file = "models/finalized_model.pkl"  

with open(model_pkl_file, 'wb') as model_file:  
    pickle.dump(clf, model_file)

# Save vectorizer
print("SAVING VECTORIZER ...")
vect_pkl_file = "models/vectorizer.pkl"  

with open(vect_pkl_file, 'wb') as vect_file:  
    pickle.dump(vect, vect_file)
  
# Load model and vectorizer as a test
print("LOADING MODEL AND VECTORIZER FOR A SANITY CHECK ...")
with open('models/finalized_model.pkl', 'rb') as loaded_model_file:
    model = pickle.load(loaded_model_file)

with open('models/vectorizer.pkl', 'rb') as loaded_vect_file:
    vect = pickle.load(loaded_vect_file)

# Evaluate model
print("RE-EVALUATE MODEL ...")
y_predict = model.predict(X_test)
print(classification_report(y_test, y_predict)) 

# Test model on a single sentence
my_sent = ["EUs nye regler"]
print("Tested the sent:", my_sent)
my_sent = vect.transform(my_sent)
predicted = model.predict(my_sent)
probability = model.predict_proba(my_sent)
print(predicted, probability)
print("Explanation of categories: -s = 0, sine = 1, preposisjon = 2, sammenkrivning = 3, omskriving = 4\n")
