# -*- coding: utf-8 -*-
"""
Created on Sun Jun 04 12:15:57 2017

@author: tomd
"""

import json
import sys
import codecs


sys.stdout=codecs.getwriter('utf-8')(sys.stdout)

#fname = "transcript_may31_seq_resulttranscripts_may31_TAP_Q2_16.json"
fname = "transcript_may31_seq_resulttranscripts_may29const_Q1_17.json"



json_data=open('C:\\Users\\tomd\\pda\\' + fname ).read()

data = json.loads(json_data)

text = ''
anexec = "Rob Sands"

i = 0

#resplen = []

for entry in data:
    for executive in entry['entry']['execs']:
        if executive['exec'] == anexec: #"Mark Hunter":
           #print executive['answer']
           text =  text + ' ' + executive['answer']
           #resplen.append(len(executive['answer']))
           i += 1
print i
           #print text 

prefix = "text_jun04_"
#with open('C:\\Users\\tomd\\pda\\textout\\' + prefix + fname + '.txt', 'w') as text_file:
#    text_file.write(text)


        #for execs in executive['exec']:
            #print execs
        #for ans in executive['answer']:
           #print ans
    #for executive in entry['entry']['execs']:
    #print entry
       
'''
	#print ","
	#print ' '.join(str(x) for x in tran['answer'])
#print "\n"

'''