#!\Python2.7\python

# import json
import pandas as pd
# import pprint

import pymongo

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.execsamp

# select which colloction to do entity extraction on
answers = db.exectrans7

print (answers)
#get some reviews by limit
curAnswer = answers.find({}, {"execName": 1, "answer": 1})
                                #sort("date", pymongo.DESCENDING).limit(521) # set to 521 for live run

reviews = {}
review =[]
mylist = []

#loop through the cursor and call the entity extraction API
for execAns in curAnswer:
    print execAns['answer']
    execName = execAns['execName']
    answer = execAns['answer']#.encode('utf-8')
    #print answer
    if len(answer) > 100:
        mylist.append({'execAnswer': answer})
print mylist
df = pd.DataFrame(mylist)
df.to_csv('C://rcDataSets//execAnswers7b.csv', index=False)

print ('End of pgm')