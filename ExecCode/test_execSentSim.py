# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 19:40:52 2017

@author: tomd
"""
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


from gensim import corpora, models, similarities
import os
import json
import tempfile

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.probability import FreqDist
from collections import defaultdict
from heapq import nlargest
from unidecode import unidecode
import pandas as pd


# read the classified eecutive answers
result = pd.read_csv('C:\\Users\\tomd\\pda\\classifiedExecAnswers_197_v0.1.csv')


repetition_counts = result['Repetition'].value_counts()
repetition_counts.name = 'Repetition Measures'
repetition_counts.index = ['Non Repetition', 'Repetition', 'Neutral']


print "Annotated Answers"
print "-----------------"
print "Repetition" + '\n',  repetition_counts, '\n'


#Open the extracted executive answers 
path = 'C:\\Users\\tomd\\pda\\textout\\execEach\\'
fname = "AnnotatedExecAnswers_197.json"

json_data=open(path + fname ).read()

data = json.loads(json_data)


#Create the list of documents
docs = []
for entry in data: #['execAnswer']:
    #print entry['execAnswer']
    docs.append(unidecode(entry['execAnswer']))
    #docs.append(entry['execAnswer'])

#print len(docs)

#print docs[0]
customStopWords=set(stopwords.words('english')+list(punctuation))

print  customStopWords

#sentc = sent_tokenize(docs[0])
#sentc = [sent_tokenize(doc.lower()) for doc in docs]
sentc = [[word for word in sent_tokenize(doc.lower()) if word not in customStopWords] 
        for doc in docs]



print sentc[0][1] 


#set up stop words
#customStopWords=set(stopwords.words('english')+list(punctuation))
#customStopWords=customStopWords=['all', 'just', 'being', '-', 'over', 'both', 'through', 'its', 'before', 'o', '$', 'hadn',  'had', ',', 'should', 'to', 'only', 'won', 'under', 'ours', 'has', '<', 'do', 'very',  'not', 'during', 'now',  'nor', '`', 'd', 'did', '=', 'didn', '^', 'this',  'each', 'further', 'where', '|', 'few', 'because', 'doing', 'some', 'hasn', 'are', 'out', 'what', 'for', '+', 'while', '/', 're', 'does', 'above', 'between', 'mustn', '?', 't', 'who','were', 'here', 'shouldn',  '[', 'by', '_', 'on', 'about', 'couldn', 'of', '&', 'against', 's', 'isn', '(', '{', 'or', 'own', '*', 'into', 'yourself', 'down', 'mightn', 'wasn', '"' ,'from', 'aren', 'there', 'been', '.', 'whom', 'too', 'wouldn', 'weren', 'was', 'until', '\\', 'more',  'that', 'but', ';', '@', 'don', 'with', 'than', 'those', ':', 'ma', 'these', 'up', 'below', 'ain', 'can',  '>', '~', 'and', 've', 'then', 'is','am', 'it', 'doesn', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', '!', 'again', '%', 'no', ')', 'when','same', 'how', 'other', 'which', 'shan', 'needn', 'haven', 'after', '#', 'most', 'such', ']', 'why', 'a','off', "'", 'm', 'so', 'y', 'the', '}', 'having', 'once']

#create list of tokens for each document 
#texts = [[word for word in word_tokenize(sentence) if word not in customStopWords] 
#        for sentence in sentc]

#print texts[0]

#number of tokens per documents
repLens = [len(text) for text in texts]



'''
 REPETITION

 For each document select the documents sentances.
 For each sentence compare it every other sentence in the document
 and calculate the sentance similarity score. The higher the similarity score 
 the higher the indication of a repetition
 '''

print "----------------"
ansReptList = []
#avoid = 0
for a in range(len(repLens)):
    wrdCountA = 0
    youWordCount = 0
    selfWordCount = 0
    futureWordCount = 0
    ppWordCount = 0
    for token in texts[a]:
        #print token
        if token in avoidWords:
            wrdCountA +=1
        if token in youWords:
            youWordCount +=1
            #print "ywc ", youWordCount
        if token in selfWords:
            selfWordCount +=1
            #print "swc ", selfWordCount
            #print "Uncertain Word: ", token, " - doc id : ", i
        if token in futureWords:
            futureWordCount +=1
        if token in ppWords:
            ppWordCount +=1
    # calcualte future versus present past you measure         
    FvP =  np.log(float((1 + futureWordCount)) / ((1 + ppWordCount )))
    #print "FvP ", FvP, futureWordCount, ' ', ppWordCount, " doc id ", a        
    # calcualte self versus you measure         
    IvU = np.log(float((1 + selfWordCount)) / ((1 + youWordCount )))
    #print "IvU ", IvU, selfWordCount, ' ', youWordCount, " doc id ", a 
    amsr = 1 - float(repLens[a] - wrdCountA) / repLens[a]
    #print "Amsr", amsr, " doc id ", a
    #print "avoid overall ", ((IvU + FvP) * amsr)
    if ((IvU + FvP) * amsr) < 0.00:    
        ansAvoidList.append(1)
    else: 
        ansAvoidList.append(-1)





reptActual = [int(token) for token in result['Repetition']]

# create a list of the indices of the actual neutral scores (e.g. = 0)
j = 0
actualReptNeutral = []
for j in range(len(result['Repetition'])): 
    if reptActual[j] == 0:
        actualReptNeutral.append(j)
        
'''
 Create a new predicted list less the neutral scores.
 For each item in predicted list if index is not in the list 
 of nuetral scores then add it to the new list   
'''
m = 0
reptPredLess0 = []        
for m in range(len(ansReptList)):
    if m not in actualReptNeutral:
        reptPredLess0.append(ansReptList[m])

# create a new list of the actual scores less the neutral socres
reptActualLess0 = [item for item in result['Repetition'] if item != 0]





