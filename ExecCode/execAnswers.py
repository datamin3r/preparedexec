#!\Python2.7\python
'''

Gets a random sample of Executive Answers 
from the MongoDB and writes them out to a CSV file

'''

# import json
import pandas as pd
# import pprint

import pymongo

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.execsamp

# select which colloction to do entity extraction on
answers = db.exectrans7

#print (answers)
#get some reviews by limit
#curAnswer = answers.find({}, {"execName": 1, "answer": 1, "conCallAns" : 1})
curAnswer = list(answers.aggregate([{"$sample": {'size': 250}}]))#, {"execName": 1, "answer": 1, "conCallAns": 1}))

reviews = {}
review =[]
mylist = []

#loop through the cursor and call the entity extraction API
for execAns in curAnswer:
    print execAns['answer']
    execName = execAns['execName']
    conCallAns = execAns['conCallAns']
    answer = execAns['answer'].encode('utf-8')
    #print answer
    if len(answer) > 100:
        mylist.append({'execAnswer': answer, 'execName': execName, 'conCallAns' : conCallAns})
print mylist
df = pd.DataFrame(mylist)
df.to_csv('C://rcDataSets//execAnswers7d250.csv', index=False)

print ('End of pgm')
