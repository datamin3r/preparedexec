# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 19:40:52 2017

@author: tom.donoghue@gmail.com
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
import pickle
import pandas as pd

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


# read the classified executive answers
result = pd.read_csv('C:\\Users\\tomd\\pda\\classifiedExecAnswers_197_v0.1.csv')


repetition_counts = result['Repetition'].value_counts()
repetition_counts.name = 'Repetition Measures'
repetition_counts.index = ['Non Repetition', 'Repetition', 'Neutral']


unprepared_counts = result['Unprepared'].value_counts()
unprepared_counts.name = 'Unprepared Measures'
unprepared_counts.index = ['Prepared', 'Unprepared', 'Neutral']


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

'''
 REPETITION

 For each document select the documents sentances.
 For each sentence compare it every other sentence in the document
 and calculate the sentance similarity score. The higher the similarity score 
 the higher the indication of a repetition
 '''

customStopWords=set(stopwords.words('english')+list(punctuation))
#texts = [[word for word in word_tokenize(document.lower()) if word not in customStopWords] 
#        for document in docs]

#sentc = sent_tokenize(docs[0])
#sentc = [sent_tokenize(doc.lower()) for doc in docs]
# sentence tokenise the answers
sentc = [sent_tokenize(doc.lower()) for doc in docs]

# tokenise the sentences
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
        # tuple of the sentence and the doc it belongs to
        sentDocTag = zip (sentDoc, docTag)
        


#set up dictionary and save it 
#dictionary = corpora.Dictionary(sentTokens[0])
#dictionary.save(os.path.join(TEMP_FOLDER, 'execsSententceTokens.dict')) 
#print(dictionary)


# create and save corpus
#corpus = [dictionary.doc2bow(sentTk) for sentTk in sentTokens[0]]
#corpora.MmCorpus.serialize(os.path.join(TEMP_FOLDER, 'execsSententceTokens.mm'), corpus)  # store to disk, for later use

# load saved dictionary and corpus
dictionary = corpora.Dictionary.load(TEMP_FOLDER + '\execsAnnotatedtext.dict')
corpus = corpora.MmCorpus(TEMP_FOLDER + '\execsSententceTokens.mm')


# create LSI model with 250 topics
lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=250)

# transform corpus to LSI space and index it
index = similarities.MatrixSimilarity(lsi[corpus])#, num_features=208) 

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

# sentence in sentences
for targetSent in sentTokens[0]:
    #print targetSent
    p += 1
    vec_bow = dictionary.doc2bow(targetSent)
    vec_lsi = lsi[vec_bow]
    sims = index[vec_lsi]
    #sorted list of number of 5 most similar results
    sims = sorted(enumerate(sims), key = lambda item: -item[1]) [:5]
    #print targetSent
    for sentResult in sims:
        # sentence window bewteen -5 and + 5 of the source sentence 
        if p - 5 <= sentResult[0] <= p + 5 and sentResult[1] > 0.0:
            #print " p ", p, "sentRslt " ,sentResult[0]
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

# list of source and similar returned sentences
srcTarget = [docSentLkup['sentSource'], docSentLkup['sentReturned']]

# get the answers with similar sentences
ansReptListTemp = []
ansReptList = []
for i in range(len(srcTarget[0])):
    #print i
    # not the same sentence
    if srcTarget[0][i] != srcTarget[1][i]:
        #print "Src sentence  ", srcTarget[0][i]
        #print "Is similar to  ", srcTarget[1][i]
        #print " Doc is Src ", docTag[srcTarget[0][i]], " Result ", docTag[srcTarget[1][i]]
        # but is the same document
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
        

# get the actual scores
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

#do pred counts
repcnt = 0
nonrepcnt = 0
print "Repetition \n"
for k in reptPredLess0:
    if k == 1:
        repcnt +=1
    else:
        nonrepcnt +=1
        

# assign for performance metrics
y_actu = reptActualLess0
y_pred = reptPredLess0


#Repetition Model Performance 


print "Performance Metrics"
print "-------------------"

print "Pred Non Repetition count = ", nonrepcnt
print "Pred Repetition count     =  ", repcnt, '\n'

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

'''
Load pickle files to work combiner for Unprepared measures

'''


pkl = open('C:\\Users\\tomd\\pda\\answerListUncert.pkl', 'rb')
pkl1 = open('C:\\Users\\tomd\\pda\\answerListAvoid.pkl', 'rb')
pkl2 = open('C:\\Users\\tomd\\pda\\neutrals.pkl', 'rb')

ansList = pickle.load(pkl)
ansAvoidList = pickle.load(pkl1)
neutrals = pickle.load(pkl2)


# get the actual prepared scores
# get the actual scores
unprepActual = [int(token) for token in result['Unprepared']]

# create a list of the indices of the actual neutral scores (e.g. = 0)
jk = 0
actualUnprepNeutral = []
for jk in range(len(result['Unprepared'])): 
    if unprepActual[jk] == 0:
        actualUnprepNeutral.append(jk)        




# add the repetition neutrals
allNeutrals = set(neutrals + actualReptNeutral + actualUnprepNeutral)

#print len(allNeutrals)

# extract the non neutral scores for both 
ix = 0
cleanAnsUncert = []
for ix in range(len(ansList)):
    if ix not in allNeutrals:
        #print ix
        cleanAnsUncert.append(ansList[ix])        
        
ix = 0    
cleanAnsAvoid = []
for ix in range(len(ansAvoidList)):
    if ix not in allNeutrals:
        #print ix
        cleanAnsAvoid.append(ansAvoidList[ix])
    
ix = 0    
cleanAnsRept = []
for ix in range(len(ansReptList)):
    if ix not in allNeutrals:
        #print ix
        cleanAnsRept.append(ansReptList[ix])
        


pkl.close()
pkl1.close()
pkl2.close()


'''
 Unprepared measures
 
'''

print "-----------------"
print "Unprepared" + '\n',  unprepared_counts, '\n'

# create a new list of the actual scores less the neutral socres
#UnprepActualLess0 = [item for item in result['Unprepared'] if item != 0]
UnprepActual = [item for item in result['Unprepared']]


ix = 0    
cleanAnsUnprep = []
for ix in range(len(UnprepActual)):
    if ix not in allNeutrals:
        #print ix
        cleanAnsUnprep.append(UnprepActual[ix])

# calculate the Unprepared score 
# sum the scores for each feature

#do pred counts
unprepcnt = 0
prepcnt = 0
print "Unprepared \n"

unprepList = []
for u in range(len(cleanAnsUnprep)):
    unPrepScore = cleanAnsUncert[u] + cleanAnsAvoid[u] + cleanAnsRept[u] 
    if unPrepScore > 0:
        unprepcnt +=1
        unprepList.append(1)
    else:
        prepcnt +=1
        unprepList.append(-1)
        

# assign for performance metrics
y_actuUprep = cleanAnsUnprep
y_predUprep = unprepList

print "Pred Unprepared count = ", unprepcnt
print "Pred prepared count  =  ", prepcnt, '\n'

print "\n Unprepared Confusion Matrix \n"
print confusion_matrix(y_actuUprep, y_predUprep), '\n'

accuracy =  accuracy_score(y_actuUprep, y_predUprep)

print "Accuracy " +'\t', "%.2f" % accuracy

ps = precision_score(y_actuUprep, y_predUprep)
 
print "Precision "+'\t', "%.2f" %  ps  

rs = recall_score(y_actuUprep, y_predUprep)

print "Recall "+'\t\t', "%.2f" %  rs

f1 = f1_score(y_actuUprep, y_predUprep)

print "F1 "+'\t\t', "%.2f" %  f1

kappa = cohen_kappa_score(y_actuUprep, y_predUprep)

print "Kappa "+'\t\t', "%.2f" %  kappa, '\n' 

'''
# End of Unprepared Scores
 
'''


