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

docTest = ['want', 'crystal', 'clear', 'management', 'appointed', 'board', 'full', 'competence', 'board', 'carry', 'forward']

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



#print texts[0]

#number of tokens per documents
repLens = [len(text) for text in texts]
repLensR = [len(sentTK) for sentTK in sentTokens[0]]



'''
 REPETITION

 For each document select the documents sentances.
 For each sentence compare it every other sentence in the document
 and calculate the sentance similarity score. The higher the similarity score 
 the higher the indication of a repetition
 '''
'''kkk
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
kkk'''        
        
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





