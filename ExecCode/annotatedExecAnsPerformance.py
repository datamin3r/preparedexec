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
from nltk.probability import FreqDist
from collections import defaultdict
from heapq import nlargest

from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score


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



print "Uncertainty" + '\n',  uncertain_counts# ['Neutral']
print "Avoidance" + '\n',  avoidance_counts# ['Neutral']
print "Repetition" + '\n',  repetition_counts# ['Neutral']

#Open the extracted executive answers 
path = 'C:\\Users\\tomd\\pda\\textout\\execEach\\'
fname = "AnnotatedExecAnsers_197a.json"

json_data=open(path + fname ).read()

data = json.loads(json_data)

#Load LM Uncertainty List of words
fh = open('C:\\Users\\tomd\\pda\\LM_Uncertainty.txt')

#lowercase and strip line endings
lmUcertWords = [x.strip().lower() for x in fh]

#Create the list of documents
docs = []
for entry in data: #['execAnswer']:
    #print entry['execAnswer']
    docs.append(unidecode(entry['execAnswer']))
    #docs.append(entry['execAnswer'])

print len(docs)

print docs[15]

#set up stop words
customStopWords=set(stopwords.words('english')+list(punctuation))
#create list of tokens for each document 

texts = [[word for word in word_tokenize(document.lower()) if word not in customStopWords] 
        for document in docs]

#number of tokens per documents
repLens = [len(text) for text in texts]

'''
For each documents check if the tokens are in the uncertainty list of words 
If an uncertain word is found then sum the counts and calcualte a measure of 
uncertainty as a value between 0 and 1 and subtract this from 1. The higher 
the score the higher the uncertainty
'''
ansList = []
uncert = 0
for i in range(len(repLens)):
    wrdCount = 0
    for token in texts[i]:
        #print token
        if token in lmUcertWords:
            wrdCount +=1
            print "Uncertain Word: ", token, " - doc id : ", i
    if wrdCount > 0:
        ansList.append(1)
        print "No. of Uncertain tokens found", wrdCount
        print "No. Tokens", repLens[i]
        umsr = 1 - float(repLens[i] - wrdCount)/ repLens[i]
        print "Uncertainty measure", umsr
        print "-----------------"
        uncert +=1
    else:
        ansList.append(-1)        
print "Pred Uncert count = ", uncert
print "Actual Uncertainty" ,  uncertain_counts['Uncertain']  

uncertActual = [int(token) for token in result['Uncertainty']]

pos = 0
upos = []
for j in range(len(result['Uncertainty'])): 
    if uncertActual[j] == 0:
        upos.append(j)
        
'''
for each item in predicted list if index = upos index then remove that item
'''        

#upos = [item for item in result['Uncertainty'] if item != 0]


#uncertActual = [int(token) for token in result['Uncertainty']]

uncertPred = ansList

y_actu = uncertActual
y_pred = uncertPred

print confusion_matrix(y_actu, y_pred)

ps = precision_score(y_actu, y_pred)

rs = recall_score(y_actu, y_pred)

ps = precision_score(y_actu, y_pred)

f1 = f1_score(y_actu, y_pred)

#y_actu = pd.Series(uncertActual, name='Actual')
#y_pred = pd.Series(uncertPred, name='Predicted')
#df_confusion = pd.crosstab(y_actu, y_pred)

#df_confusion = pd.crosstab(y_actu, y_pred, rownames=['Actual'], colnames=['Predicted'], margins=True)

#print df_confusion

