#!\Python2.7\python

# import json
import pandas as pd
# import pprint

import pymongo

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.execsamp

# select which colloction to do entity extraction on
answers = db.exectrans

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
    # add the results to a list of dicts
    for item in response['entities']:
        textLatin1 = item['text'].encode('latin-1')
        mylist.append ({'type': item['type'], 'text': textLatin1,
                    'count': item['count'], 'date': yReview['date'], 'name': yReview['name'],
                        'nationality_id': yReview['nationality_id']})

    #print 'entities list ' + str(mylist)
    # assign the list to a dataframe for ease of outputing a csv of the results
    df = pd.DataFrame(mylist)
    df.to_csv('C:\dwDataSets\yelpEntities2.csv', index=False)
    '''

print ('End of pgm')