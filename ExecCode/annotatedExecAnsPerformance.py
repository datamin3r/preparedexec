# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 12:03:04 2017

@author: tomd
"""
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
#from nltk.probability import FreqDist
#from collections import defaultdict
#from heapq import nlargest

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, cohen_kappa_score, roc_curve
#import matplotlib as plt

import json
import sys
import codecs
import io
from unidecode import unidecode
import pandas as pd

try:
    doUnicode = unicode
except NameError:
    doUnicode = str
    
sys.stdout=codecs.getwriter('utf-8')(sys.stdout)

i = 0
execAns = {}
resp = []

# read the classified eecutive answers
result = pd.read_csv('C:\\Users\\tomd\\pda\\classifiedExecAnswers_197_v0.1.csv')
# result_dict = result.to_dict('records')

# Create the Series to store the annotated featrure scores
# and add some meaningful names
uncertain_counts = result['Uncertainty'].value_counts()

uncertain_counts.name = 'Uncertainty Measures'
uncertain_counts.index = ['Certain', 'Uncertain', 'Neutral']

avoidance_counts = result['Avoidance'].value_counts()
avoidance_counts.name = 'Avoidance Measures'
avoidance_counts.index = ['Non Avoidance', 'Avoidance', 'Neutral']


repetition_counts = result['Repetition'].value_counts()
repetition_counts.name = 'Repetition Measures'
repetition_counts.index = ['Non Repetition', 'Repetition', 'Neutral']



print "Uncertainty" + '\n',  uncertain_counts, '\n'
print "Avoidance" + '\n',  avoidance_counts, '\n'
print "Repetition" + '\n',  repetition_counts, '\n'

#Open the extracted executive answers 
path = 'C:\\Users\\tomd\\pda\\textout\\execEach\\'
fname = "AnnotatedExecAnswers_197.json"

json_data=open(path + fname ).read()

data = json.loads(json_data)

#Load LM Uncertainty List of words
fhu = open('C:\\Users\\tomd\\pda\\LM_Uncertainty.txt')

#lowercase and strip line endings
lmUcertWords = [x.strip().lower() for x in fhu]

#Load LIWC avoiding List of words
fha = open('C:\\Users\\tomd\\pda\\Avoid_Words.txt')

#lowercase and strip line endings
avoidWords = [x.strip().lower() for x in fha]



#Create the list of documents
docs = []
for entry in data: #['execAnswer']:
    #print entry['execAnswer']
    docs.append(unidecode(entry['execAnswer']))
    #docs.append(entry['execAnswer'])

#print len(docs)

#print docs[15]

#set up stop words
customStopWords=set(stopwords.words('english')+list(punctuation))
#create list of tokens for each document 

texts = [[word for word in word_tokenize(document.lower()) if word not in customStopWords] 
        for document in docs]

#number of tokens per documents
repLens = [len(text) for text in texts]

'''
 UNCERTAINTY

 For each document check if the tokens are in the uncertainty list of words. 
 If an uncertain word is found then sum the counts and calcualte a measure of 
 uncertainty as a value between 0 and 1 and subtract this from 1. The higher 
 the score the higher the uncertainty
'''
ansList = []
#uncert = 0
for i in range(len(repLens)):
    wrdCount = 0
    for token in texts[i]:
        #print token
        if token in lmUcertWords:
            wrdCount +=1
            #print "Uncertain Word: ", token, " - doc id : ", i
    if wrdCount > 0:
        #ansList.append(1)
        #print "No. of Uncertain tokens found", wrdCount
        #print "No. Tokens", repLens[i]
        umsr = 1 - float(repLens[i] - wrdCount)/ repLens[i]
        #print "Uncertainty measure", umsr
        #print "-----------------"
        if umsr > 0.01:
            ansList.append(1)
            #uncert +=1
        else:
            ansList.append(-1)
    else:
        ansList.append(-1)        
#print "Pred Uncert count = ", uncert
#print "Actual Uncertainty" ,  uncertain_counts['Uncertain']  

# get the actual scores
uncertActual = [int(token) for token in result['Uncertainty']]

# create a list of the indices of the actual neutral scores (e.g. = 0)
j = 0
actualNeutral = []
for j in range(len(result['Uncertainty'])): 
    if uncertActual[j] == 0:
        actualNeutral.append(j)
        
'''
 Cretea a new predicted list less the neutral scores.
 For each item in predicted list if index is not in the list 
 of nuetral scores then add it to the new list   
'''
m = 0
uncertainPredLess0 = []        
for m in range(len(ansList)):
    if m not in actualNeutral:
        uncertainPredLess0.append(ansList[m])

# create a new list of the actual scores less the neutral socres
uncertActualLess0 = [item for item in result['Uncertainty'] if item != 0]

# assign for performance metrics
y_actu = uncertActualLess0
y_pred = uncertainPredLess0

'''
Uncertainty Model Performance 

'''

print "\n Confusion Matrix \n"
print confusion_matrix(y_actu, y_pred), '\n'

accuracy =  accuracy_score(y_actu, y_pred)

print "Accuracy " +'\t', accuracy

ps = precision_score(y_actu, y_pred)
 
print "Precision "+'\t', ps  

rs = recall_score(y_actu, y_pred)

print "Recall "+'\t\t', rs

f1 = f1_score(y_actu, y_pred)

print "F1 "+'\t\t', f1

kappa = cohen_kappa_score(y_actu, y_pred)

print "Kappa "+'\t\t', kappa 

'''
 End of Uncertainity Scores
 
'''

'''
 AVOIDANCE

 For each document check if the tokens are in the avoidance list of words. 
 If an avoidance word is found then sum the counts and calcualte a measure of 
 avoidance as a value between 0 and 1 and subtract this from 1. The higher 
 the score the higher the avoidance
'''
print "----------------"
ansAvoidList = []
#avoid = 0
for a in range(len(repLens)):
    wrdCount = 0
    for token in texts[a]:
        #print token
        if token in avoidWords:
            wrdCount +=1
            #print "Uncertain Word: ", token, " - doc id : ", i
    if wrdCount > 0:
        #ansList.append(1)
        #print "No. of Uncertain tokens found", wrdCount
        #print "No. Tokens", repLens[i]
        amsr = 1 - float(repLens[i] - wrdCount)/ repLens[a]
        #print "Uncertainty measure", umsr
        #print "-----------------"
        if amsr > 0.00:
            ansAvoidList.append(1)
            #avoid +=1
        else:
            ansAvoidList.append(-1)
    else:
        ansAvoidList.append(-1)        
#print "Pred Uncert count = ", uncert
#print "Actual Uncertainty" ,  uncertain_counts['Uncertain']  

# get the actual scores
avoidActual = [int(token) for token in result['Avoidance']]

# create a list of the indices of the actual neutral scores (e.g. = 0)
aj = 0
actualAviodNeutral = []
for aj in range(len(result['Avoidance'])): 
    if avoidActual[aj] == 0:
        actualAviodNeutral.append(aj)
        
'''
 Cretea a new predicted list less the neutral scores.
 For each item in predicted list if index is not in the list 
 of neutral scores then add it to the new list   
'''
am = 0
avoidPredLess0 = []        
for am in range(len(ansAvoidList)):
    if am not in actualAviodNeutral:
        avoidPredLess0.append(ansAvoidList[am])

# create a new list of the actual scores less the neutral socres
avoidActualLess0 = [item for item in result['Avoidance'] if item != 0]

# assign for performance metrics
y_actuA = avoidActualLess0
y_predA = avoidPredLess0

'''
Avoidance Model Performance 

'''

print "\n Avoidance Confusion Matrix \n"
print confusion_matrix(y_actuA, y_predA), '\n'

accuracyA =  accuracy_score(y_actuA, y_predA)

print "Accuracy " +'\t', accuracyA

psA = precision_score(y_actuA, y_predA)
 
print "Precision "+'\t', psA  

rsA = recall_score(y_actuA, y_predA)

print "Recall "+'\t\t', rsA

f1A = f1_score(y_actuA, y_predA)

print "F1 "+'\t\t', f1A

kappaA = cohen_kappa_score(y_actuA, y_predA)

print "Kappa "+'\t\t', kappaA 


'''
 End of Uncertainity Scores
 
'''



'''
fpr, tpr, thresholds = roc_curve(y_actu, y_pred)

def plot_roc_curve(fpr, tpr, lable=None):
    plt.plot(fpr,tpr, linewidth=2, lable=label)
    plt.plot([0,1,[0,1], 'k--'])
    plt.axis([0,1,0,1])
    plt.xlabel('F Pos Rate')
    plt.ylabel('T Pos Rate')
    
plot_roc_curve(fpr.tpr)
plt.show()
'''
#y_actu = pd.Series(uncertActual, name='Actual')
#y_pred = pd.Series(uncertPred, name='Predicted')
#df_confusion = pd.crosstab(y_actu, y_pred)

#df_confusion = pd.crosstab(y_actu, y_pred, rownames=['Actual'], colnames=['Predicted'], margins=True)

#print df_confusion

