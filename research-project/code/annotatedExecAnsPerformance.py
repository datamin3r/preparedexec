# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 12:03:04 2017

Working Version 1.0

@author: tom.donoghue@gmail.com

"""
#import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
#from nltk.corpus import stopwords
#from string import punctuation
#from nltk.probability import FreqDist
#from collections import defaultdict
#from heapq import nlargest
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, cohen_kappa_score#, roc_curve, precision_recall_curve
#from scipy.stats import hmean
#import matplotlib.pyplot as plt
#from sklearn.metrics import matthews_corrcoef



import json
import sys
import codecs
#import io
from unidecode import unidecode
import pandas as pd
import pickle

try:
    doUnicode = unicode
except NameError:
    doUnicode = str
    
sys.stdout=codecs.getwriter('utf-8')(sys.stdout)

i = 0
execAns = {}
resp = []

# read the classified executive answers
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

unprepared_counts = result['Unprepared'].value_counts()
unprepared_counts.name = 'Unprepared Measures'
unprepared_counts.index = ['Prepared', 'Unprepared', 'Neutral']


print "Annotated Answers"
print "-----------------"
print "Uncertainty" + '\n',  uncertain_counts, '\n'
print "Avoidance" + '\n',  avoidance_counts, '\n'
print "Repetition" + '\n',  repetition_counts, '\n'
print "Unprepared" + '\n',  unprepared_counts, '\n'

#Open the unlabelled extracted executive answers 
path = 'C:\\Users\\tomd\\pda\\textout\\execEach\\'
fname = "UnAnnotatedExecAnswers_197.json"

json_data=open(path + fname ).read()

data = json.loads(json_data)

def getWordList(fileHandle):
    fH = open(fileHandle)
    words = [x.strip().lower() for x in fH]
    return words

# Load LM Uncertainty List of words
# lowercase and strip line endings
lmUcertWords = getWordList('C:\\Users\\tomd\\pda\\LM_Uncertainty.txt')

#Load LIWC avoiding List of words
#lowercase and strip line endings
avoidWords = getWordList('C:\\Users\\tomd\\pda\\Avoid_Words.txt')

youWords = getWordList('C:\\Users\\tomd\\pda\\You_Words.txt')
selfWords = getWordList('C:\\Users\\tomd\\pda\\Self_Words.txt')
futureWords = getWordList('C:\\Users\\tomd\\pda\\Future_Words.txt')
ppWords = getWordList('C:\\Users\\tomd\\pda\\PresentPast_Words.txt')


#Create the list of documents
docs = []
for entry in data: #['execAnswer']:
    #print entry['execAnswer']
    docs.append(unidecode(entry['execAnswer']))
    #docs.append(entry['execAnswer'])

#print len(docs)

#print docs[15]

#set up stop words
#customStopWords=set(stopwords.words('english')+list(punctuation))
# custom edit of nltk stopwords with the words from the word lists removed 
customStopWords=['all', 'just', 'being', '-', 'over', 'both', 'through', 'its', 'before', 'o', '$', 'hadn',  'had', ',', 'should', 'to', 'only', 'won', 'under', 'has', '<', 'do', 'very',  'not', 'during', 'now',  'nor', '`', 'd', 'did', '=', 'didn', '^', 'this',  'each', 'further', 'where', '|', 'few', 'because', 'doing', 'some', 'hasn', 'are', 'out', 'what', 'for', '+', 'while', '/', 're', 'does', 'above', 'between', 'mustn', '?', 't', 'who','were', 'here', 'shouldn',  '[', 'by', '_', 'on', 'about', 'couldn', 'of', '&', 'against', 's', 'isn', '(', '{', 'or', 'own', '*', 'into', 'down', 'mightn', 'wasn', '"' ,'from', 'aren', 'there', 'been', '.', 'whom', 'too', 'wouldn', 'weren', 'was', 'until', '\\', 'more',  'that', 'but', ';', '@', 'don', 'with', 'than', 'those', ':', 'ma', 'these', 'up', 'below', 'ain', 'can',  '>', '~', 'and', 've', 'then', 'is','am', 'it', 'doesn', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', '!', 'again', '%', 'no', ')', 'when','same', 'how', 'other', 'which', 'shan', 'needn', 'haven', 'after', '#', 'most', 'such', ']', 'why', 'a','off', "'", 'm', 'so', 'y', 'the', '}', 'having', 'once']
#customStopWords=""

#create list of tokens for each document 
texts = [[word for word in word_tokenize(document.lower()) if word not in customStopWords] 
        for document in docs]

#print texts[0]

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
        #umsr = float(repLens[i] - wrdCount)/ repLens[i]
        #print "Uncertainty measure", umsr
        #print "-----------------"
        if umsr > 0.0:
            ansList.append(1)
        else:
            ansList.append(-1)
    else:
        ansList.append(-1)

# get the actual scores
uncertActual = [int(token) for token in result['Uncertainty']]

# create a list of the indices of the actual neutral scores (e.g. = 0)
j = 0
actualNeutral = []
for j in range(len(result['Uncertainty'])): 
    if uncertActual[j] == 0:
        actualNeutral.append(j)
        
'''
 Create a new predicted list less the neutral scores.
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

#do pred counts
uncertcnt = 0
certcnt = 0
for n in uncertainPredLess0:
    if n == 1:
        uncertcnt +=1
    else:
        certcnt +=1



# assign for performance metrics
y_actu = uncertActualLess0
y_pred = uncertainPredLess0

'''
Uncertainty Model Performance 

'''
print "-------------------"
print "Performance Metrics"
print "-------------------\n"
print "Uncertainty \n"
print "Pred Certainty count   = ", certcnt 
print "Pred Uncertainty count =  ", uncertcnt, '\n'
#print "Actual Uncertainty" ,  uncertain_counts['Uncertain']  


print "\n Uncertainty Confusion Matrix \n"
print confusion_matrix(y_actu, y_pred), '\n'

#mcc = matthews_corrcoef(y_actu, y_pred)

#print "mcc ", mcc

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
 End of Uncertainity Scores
 
'''

'''
 AVOIDANCE

 For each document check if the tokens are in the avoidance list of words. 
 If an avoidance word is found then sum the counts and calcualte a measure of 
 avoidance as a value between 0 and 1 and subtract this from 1. The higher 
 the score the higher the avoidance
'''
print "----------------\n"
print "Avoidance \n"
ansAvoidList = []
unavoidcnt = 0
avoidcnt = 0
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
    # calcualte future v present past you measure higher value = more avoiding       
    FvP =  np.log(float((1 + futureWordCount)) / ((1 + ppWordCount )))
    #print "FvP ", FvP, futureWordCount, ' ', ppWordCount, " doc id ", a        
    # calcualte self v you measure lower value = more avoiding        
    IvU = np.log(float((1 + selfWordCount)) / ((1 + youWordCount )))
    #print "IvU ", IvU, selfWordCount, ' ', youWordCount, " doc id ", a
    # calcualte avoiding words measure higher value = more avoiding
    amsr = 1 - float(repLens[a] - wrdCountA) / repLens[a] 
    #print "Amsr", amsr, " doc id ", a
    #print "avoid overall ", ((IvU + FvP) * amsr)
    # combiner squares the values to remove negative
    # add avioding and substract non avoiding 
    #totalAvoid = ((amsr**2) + (FvP**2) - (IvU**2))
    # Probably just using amsr is providing best measure of the 3 on its own!!
    #totalAvoid =  (amsr + FvP) - IvU
    totalAvoid =  (FvP - IvU) + amsr
    if totalAvoid > 0.0:
    #if float(IvU + FvP) / (1 + amsr) < 0.00: #18-JUL Acc.55, Pr .34, Rec .45, F1 .39, Kap .05
    #if ((FvP + amsr) + (1 - IvU)) > 0.00: #19-JUL Acc.67, Pr .46, Rec .24, F1 .31, Kap .13
    #if (float((float(1/(1+IvU)) + float(1/(1+FvP)) + float(1/(1+amsr))) / 3) ) > 1.00: # 19-Jul Acc.50, Pr .29, Rec .41, F1 .34, Kap -.04   
        ansAvoidList.append(1)
        
    else: 
        ansAvoidList.append(-1)
        

'''
    if wrdCountA > 0:
        #ansList.append(1)
        #print "No. of Uncertain tokens found", wrdCount
        #print "No. Tokens", repLens[i]
        amsr = 1 - float(repLens[a] - wrdCountA) / repLens[a]
        print "Avoidance measure", amsr, " doc id ", a
        #print "-----------------"
        #if float(IvU + amsr) / 2  > 0.00: 
        if  (IvU - amsr) > 1.00:
            ansAvoidList.append(1)
            #avoid +=1
        else: 
            ansAvoidList.append(-1)
    else:
        ansAvoidList.append(-1)
'''    
#print "Pred Uncert count = ", uncert
#print "Actual Uncertainty" ,  uncertain_counts['Uncertain']  

# get the actual scores
avoidActual = [int(token) for token in result['Avoidance']]

# create a list of the indices of the actual neutral scores (e.g. = 0)
aj = 0
actualAvoidNeutral = []
for aj in range(len(result['Avoidance'])): 
    if avoidActual[aj] == 0:
        actualAvoidNeutral.append(aj)
        
'''
 Cretea a new predicted list less the neutral scores.
 For each item in predicted list if index is not in the list 
 of neutral scores then add it to the new list   
'''
am = 0
avoidPredLess0 = []        
for am in range(len(ansAvoidList)):
    if am not in actualAvoidNeutral:
        avoidPredLess0.append(ansAvoidList[am])

# create a new list of the actual scores less the neutral socres
avoidActualLess0 = [item for item in result['Avoidance'] if item != 0]

#do pred counts
avoidcnt = 0
unavoidcnt = 0
for k in avoidPredLess0:
    if k == 1:
        avoidcnt +=1
    else:
        unavoidcnt +=1

# assign for performance metrics
y_actuA = avoidActualLess0
y_predA = avoidPredLess0

'''
Avoidance Model Performance 

'''

print "Pred Non Avoidance count =  ", unavoidcnt
print "Pred Avoidance count     =  ", avoidcnt , '\n'

print "\n Avoidance Confusion Matrix \n"
print confusion_matrix(y_actuA, y_predA), '\n'

#mccA = matthews_corrcoef(y_actuA, y_predA)

#print "mccA ", mccA

accuracyA =  accuracy_score(y_actuA, y_predA)

print "Accuracy " +'\t', "%.2f" %  accuracyA

psA = precision_score(y_actuA, y_predA)
 
print "Precision "+'\t', "%.2f" %  psA  

rsA = recall_score(y_actuA, y_predA)

print "Recall "+'\t\t', "%.2f" %  rsA

f1A = f1_score(y_actuA, y_predA)

print "F1 "+'\t\t', "%.2f" %  f1A

kappaA = cohen_kappa_score(y_actuA, y_predA)

print "Kappa "+'\t\t', "%.2f" %  kappaA 


'''
 End of Uncertainity Scores
 
'''


'''
 Pickle lists of uncertainty, avoidance
 neutral counts for use in Unpreparedness combiner

'''
# combine the neutrals
neutrals = actualAvoidNeutral + actualNeutral
#print neutrals


output = open('C:\\Users\\tomd\\pda\\answerListUncert.pkl', 'wb')
output1 = open('C:\\Users\\tomd\\pda\\answerListAvoid.pkl', 'wb')
output2 = open('C:\\Users\\tomd\\pda\\neutrals.pkl', 'wb')

# Pickle dictionary using protocol 0.
pickle.dump(ansList, output)
pickle.dump(ansAvoidList, output1)
pickle.dump(neutrals, output2)

output.close()
output1.close()
output2.close()

'''
fpr, tpr, thresholds = roc_curve(y_actu, y_pred)

def plot_roc_curve(fpr, tpr, label=None):
    plt.plot(fpr,tpr, linewidth=2, label=label)
    plt.plot([0,1,[0,1], 'k--'])
    plt.axis([0,1,0,1])
    plt.xlabel('F Pos Rate')
    plt.ylabel('T Pos Rate')
    
plot_roc_curve(fpr, tpr)
plt.show()
'''
#y_actu = pd.Series(uncertActual, name='Actual')
#y_pred = pd.Series(uncertPred, name='Predicted')
#df_confusion = pd.crosstab(y_actu, y_pred)

#df_confusion = pd.crosstab(y_actu, y_pred, rownames=['Actual'], colnames=['Predicted'], margins=True)

#print df_confusion

