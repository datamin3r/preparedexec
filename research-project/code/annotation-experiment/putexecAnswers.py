#!\Python2.7\python

import json
import sys
#import pandas as pd
import os
# import pprint

import pymongo

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.execsamp

# select which collection to insert to
answers = db.exectrans7
#fname = "Ivan Menezes_text_jun14_transcript_may31_seq_resulttranscripts_may29_DEO_q4_16.json"

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



print ('End of pgm')