# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 13:59:24 2017

@author: tomd
"""
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
#from collections import defaultdict
#from heapq import nlargest
import numpy as np
#from nltk.metrics import ConfusionMatrix
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
#from sklearn.model_selection import cross_val_predict

import sklearn

print(sklearn.__file__)
print(sklearn.__path__)
print  (sklearn.__version__)
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, cohen_kappa_score, roc_curve
#from scipy.stats import hmean
#import matplotlib as plt


import json
import sys
import codecs
import io
import random
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

uncertainScore = result['Uncertainty']
uncertainAnswers = result['execAnswer']


#set up stop words
customStopWords=set(stopwords.words('english')+list(punctuation))
#customStopWords=['all', 'just', 'being', '-', 'over', 'both', 'through', 'its', 'before', 'o', '$', 'hadn',  'had', ',', 'should', 'to', 'only', 'won', 'under', 'ours', 'has', '<', 'do', 'very',  'not', 'during', 'now',  'nor', '`', 'd', 'did', '=', 'didn', '^', 'this',  'each', 'further', 'where', '|', 'few', 'because', 'doing', 'some', 'hasn', 'are', 'out', 'what', 'for', '+', 'while', '/', 're', 'does', 'above', 'between', 'mustn', '?', 't', 'who','were', 'here', 'shouldn',  '[', 'by', '_', 'on', 'about', 'couldn', 'of', '&', 'against', 's', 'isn', '(', '{', 'or', 'own', '*', 'into', 'yourself', 'down', 'mightn', 'wasn', '"' ,'from', 'aren', 'there', 'been', '.', 'whom', 'too', 'wouldn', 'weren', 'was', 'until', '\\', 'more',  'that', 'but', ';', '@', 'don', 'with', 'than', 'those', ':', 'ma', 'these', 'up', 'below', 'ain', 'can',  '>', '~', 'and', 've', 'then', 'is','am', 'it', 'doesn', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', '!', 'again', '%', 'no', ')', 'when','same', 'how', 'other', 'which', 'shan', 'needn', 'haven', 'after', '#', 'most', 'such', ']', 'why', 'a','off', "'", 'm', 'so', 'y', 'the', '}', 'having', 'once']
#customStopWords=""

#create list of tokens for each document 
texts = [[word for word in word_tokenize(document.lower()) if word not in customStopWords] 
        for document in uncertainAnswers]


#tuple of answer and uncertainty label
uncertainDocs = zip(texts, uncertainScore)
#shuffle the tuple
#random.shuffle(uncertainDocs)

#list of all words
doc2words = []
for words in texts:
    for word in words:
        doc2words.append(word)


wordFreq = nltk.FreqDist(doc2words)

#print wordFreq.most_common(10)

composedFeatures = list(wordFreq.keys()[:2000]) 



def getFeatures(doc):
    wordSet = set(doc)
    features = {}
    for item in composedFeatures:
        #print item, wordSet, item in wordSet
        features[item] = (item in wordSet)

    
    return features

setOfFeatures = [(getFeatures(ans), score) for (ans, score) in uncertainDocs]
random.shuffle(setOfFeatures)


trainingSet = setOfFeatures[:137] 
testSet =  setOfFeatures[137:]

classifer = nltk.NaiveBayesClassifier.train(trainingSet)
print "nltk NB classifier Accuracy = ", nltk.classify.accuracy(classifer, testSet)*100

classifer.show_most_informative_features(20)

MvNBClassifier = SklearnClassifier(MultinomialNB())
MvNBClassifier.train(trainingSet)
print "MvNBClassifier Accuracy = ", nltk.classify.accuracy(MvNBClassifier, testSet)*100

BerNBClassifier = SklearnClassifier(BernoulliNB())
BerNBClassifier.train(trainingSet)
print "BerNBClassifier Accuracy = ", nltk.classify.accuracy(BerNBClassifier, testSet)*100

#GausNBClassifier = SklearnClassifier(GaussianNB())
#GausNBClassifier.train(trainingSet)
#print "GausNBClassifier Accuracy = ", nltk.classify.accuracy(GausNBClassifier, testSet)*100


LogisticRegressionClassifier = SklearnClassifier(LogisticRegression())
LogisticRegressionClassifier.train(trainingSet)
print "LogisticRegressionClassifier Accuracy = ", nltk.classify.accuracy(LogisticRegressionClassifier, testSet)*100

SGDClassifier = SklearnClassifier(SGDClassifier())
SGDClassifier.train(trainingSet)
print "SGDClassifier Accuracy = ", nltk.classify.accuracy(SGDClassifier, testSet)*100

SVCClassifier = SklearnClassifier(SVC())
SVCClassifier.train(trainingSet)
print "SVCClassifier Accuracy = ", nltk.classify.accuracy(SVCClassifier, testSet)*100

LinearSVCClassifier = SklearnClassifier(LinearSVC())
LinearSVCClassifier.train(trainingSet)
print "LinearSVCClassifier Accuracy = ", nltk.classify.accuracy(LinearSVCClassifier, testSet)*100

NuSVCClassifier = SklearnClassifier(NuSVC(nu=0.2))
NuSVCClassifier.train(trainingSet)
print "NuSVCClassifier Accuracy = ", nltk.classify.accuracy(NuSVCClassifier, testSet)*100

#
#x_trainingSet = setOfFeatures[:250]
#y_trainingSet = setOfFeatures[250:501]
#y_train_pred = cross_val_predict(classifer, x_trainingSet,y_trainingSet, cv=3)