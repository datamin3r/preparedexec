# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 19:40:52 2017

@author: tomd
"""
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import tempfile
TEMP_FOLDER = tempfile.gettempdir()
print('Folder "{}" will be used to save temporary dictionary and corpus.'.format(TEMP_FOLDER))

from gensim import corpora, models, similarities
import os
import io
import json
import tempfile

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
#from nltk.probability import FreqDist
#from collections import defaultdict
#from heapq import nlargest
from unidecode import unidecode
#import pandas as pd
#import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, cohen_kappa_score, roc_curve



try:
    doUnicode = unicode
except NameError:
    doUnicode = str


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

texts = [[word for word in word_tokenize(document.lower()) if word not in customStopWords] 
        for document in docs]

#sentc = sent_tokenize(docs[0])
#sentc = [sent_tokenize(doc.lower()) for doc in docs]
sentc = [sent_tokenize(doc.lower()) for doc in docs]



sentTokens = [[[ word for word in word_tokenize(wordit) if word not in customStopWords]
        for docit in sentc 
        for wordit in docit]] 
#print "sentence Tokens ", sentTokens

#create lists to hold doccuments and sentences
sentDoc = []
docTag = []

i = 0
for docItem in sentc:
    i += 1
    for sentItem in docItem:
        #print sentItem
        #print "docit", '\n', i, "sentItem ", sentItem
        sentDoc.append(sentItem)
        docTag.append(i)
        #zipi = [sentDoc + tag]
        sentDocTag = zip (sentDoc, docTag)
        





#set up dictionary and save it 
#dictionary = corpora.Dictionary(sentTokens[0])
#dictionary.save(os.path.join(TEMP_FOLDER, 'execsSententceTokens.dict')) 
#print(dictionary)

# load saved dictionary and corpus
dictionary = corpora.Dictionary.load(TEMP_FOLDER + '\execsAnnotatedtext.dict')
corpus = corpora.MmCorpus(TEMP_FOLDER + '\execsSententceTokens.mm')

# create and save corpus
#corpus = [dictionary.doc2bow(sentTk) for sentTk in sentTokens[0]]
#corpora.MmCorpus.serialize(os.path.join(TEMP_FOLDER, 'execsSententceTokens.mm'), corpus)  # store to disk, for later use

# create LSI model with 208 topics
lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=208)

# transform corpus to LSI space and index it
index = similarities.MatrixSimilarity(lsi[corpus]) 

#save the index
#index.save(TEMP_FOLDER + '\execsSententceTokensIndex.index')

#load the saved index
#index = similarities.MatrixSimilarity.load(TEMP_FOLDER + '\execsSententceTokensIndex.index')


#lsi.show_topic(1, topn=15)
docSentLkup = {}
docSentAll = {}
sentNdoc = []
docNsent = []
sentCosSim = []
sourceId = []

p = -1

for targetSent in sentTokens[0]:
    #print targetSent
    p += 1
    vec_bow = dictionary.doc2bow(targetSent)
    vec_lsi = lsi[vec_bow]
    sims = index[vec_lsi]
    #sorted list of number of similar results
    sims = sorted(enumerate(sims), key = lambda item: -item[1]) [:5]
    #print targetSent
    for sentResult in sims:
        if p - 5 <= sentResult[0] <= p + 5 and sentResult[1] > 0.0: 
            xs = sentResult[0]
            cosinSim = sentResult[1]
            mydoc = sentDocTag[xs][1] 
            docNsent.append(mydoc)
            sentNdoc.append(xs)
            sentCosSim.append(cosinSim)
            sourceId.append(p)
        
        
docSentLkup['docId'] = docNsent
docSentLkup['sentReturned'] = sentNdoc
docSentLkup['cosinSim'] = str(sentCosSim)
docSentLkup['sentSource'] = sourceId
#print "docnsnt ", docSentLkup 

srcTarget = [docSentLkup['sentSource'], docSentLkup['sentReturned']]


ansReptListTemp = []
ansReptList = []
for i in range(len(srcTarget[0])):
    #print i
    if srcTarget[0][i] != srcTarget[1][i]:
        #print "Src sentence  ", srcTarget[0][i]
        #print "Is similar to  ", srcTarget[1][i]
        #print " Doc is Src ", docTag[srcTarget[0][i]], " Result ", docTag[srcTarget[1][i]]
        if docTag[srcTarget[0][i]] == docTag[srcTarget[1][i]]:
            #print " this is the doc to we need ", docTag[srcTarget[0][i]]
            ansReptListTemp.append(docTag[srcTarget[0][i]])
            
# populate the answers that are repetitive 1 or -1
# range is the number of answers (document list of sentences) to be processed 
for i in range(len(sentc)):
    if i in ansReptListTemp:
        ansReptList.append(1)
    else:
        ansReptList.append(-1)
    

#sentparis = zip[for j in docTag if  


#with io.open('C:\\Users\\tomd\\pda\\textout\\execEach\\docSentLookupwithCosSimTargetSentLmt2.json', 'w', encoding='utf8' ) as outfile:
#    bonn = json.dumps(docSentLkup, outfile, indent = 4, ensure_ascii=False)
#    outfile.write(doUnicode(bonn))



'''good single test

#docTest = ['want', 'crystal', 'clear', 'management', 'appointed', 'board', 'full', 'competence', 'board', 'carry', 'forward']

docTest = ['delever', 'invest', 'behind', 'brands', 'pursue', 'certain', 'opportunities', 'return', 'money', 'shareholders']
vec_bow = dictionary.doc2bow(docTest)
vec_lsi = lsi[vec_bow] # convert the query to LSI space
#print(vec_lsi)

#perform query of the test doc against the corpus
sims = index[vec_lsi]
#print(list(enumerate(sims)))

#
sims = sorted(enumerate(sims), key = lambda item: -item[1]) [:5]
print sims



docSentLkup = {}
sentNdoc = []
docNsent = []
for sentTarget in sims:
    xs = sentTarget[0]
    mydoc = sentDocTag[xs][1] 
    docNsent.append(mydoc)
    sentNdoc.append(xs)

docSentLkup['docId'] = docNsent
docSentLkup['sentId'] = sentNdoc


print "docnsnt ", docSentLkup 
good'''


#print texts[0]

#number of tokens per documents
#repLens = [len(text) for text in texts]
#repLensR = [len(sentTK) for sentTK in sentTokens[0]]



'''
 REPETITION

 For each document select the documents sentances.
 For each sentence compare it every other sentence in the document
 and calculate the sentance similarity score. The higher the similarity score 
 the higher the indication of a repetition
 '''


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


# assign for performance metrics
y_actu = reptActualLess0
y_pred = reptPredLess0


#Repetition Model Performance 


print "Performance Metrics"
print "-------------------"
print "\n Repetition Confusion Matrix \n"
print confusion_matrix(y_actu, y_pred), '\n'

accuracy =  accuracy_score(y_actu, y_pred)

print "Accuracy " +'\t', "%.2f" % accuracy

ps = precision_score(y_actu, y_pred)
 
print "Precision "+'\t', "%.2f" %  ps  

rs = recall_score(y_actu, y_pred)

print "Recall "+'\t\t', "%.2f" %  rs

f1 = f1_score(y_actu, y_pred)

print "F1 "+'\t\t', "%.2f" %  f1

kappa = cohen_kappa_score(y_actu, y_pred)

print "Kappa "+'\t\t', "%.2f" %  kappa, '\n' 

'''
#End of Repetition Scores
 
'''
