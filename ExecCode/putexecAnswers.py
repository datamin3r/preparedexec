#!\Python2.7\python

import json
import sys
import pandas as pd
import os
# import pprint

import pymongo

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.execsamp

# select which collection to insert to
answers = db.exectrans7
#fname = "Ivan Menezes_text_jun14_transcript_may31_seq_resulttranscripts_may29_DEO_q4_16.json"
#x = [fname]

for fname in os.listdir('C://rcDataSets//'):
    print fname
    json_data = open("C://rcDataSets//" + fname ).read()

    conCall = fname[-20:-5]

    data = json.loads(json_data)
    #execResp
    for entry in data:
        #print entry
        execName = entry['execName']
        #print execName
        i = 0
        for execUtter in entry['execResp']:
            #print execUtter
            conCallAns = conCall + "_" +str(i)
            try:
                answers.insert_one({'execName': execName, 'answer':execUtter, 'conCallAns': conCallAns})
                print "inserting answer"
            except:
                print "Error ", sys.exc_info()[0]

            #text =  text + ' ' + executive['answer']
            #resplen.append(executive['answer'])
            i += 1
        print i


'''

print (answers)
#get some reviews by limit
curAnswer = answers.find({}, {"execName": 1, "execResp": 1, "execRespCount": 1})
                                #sort("date", pymongo.DESCENDING).limit(521) # set to 521 for live run

reviews = {}
review =[]
mylist = []

#loop through the cursor and call the entity extraction API
for execAns in curAnswer:
    #print execAns
    execName = execAns['execName']
    text = execAns['execResp']#.encode('utf-8')
    for answer in text:
        if len(answer) > 350:
            print answer
            mylist.append({'execAnswer': answer})
            df = pd.DataFrame(mylist)
            df.to_csv('C:\dwDataSets\execAnswers.csv', index=False)

            #print execName, text
'''
print ('End of pgm')