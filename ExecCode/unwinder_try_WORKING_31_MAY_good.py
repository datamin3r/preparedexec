#-*- coding: utf-8 -*-
"""
Created on Mon May 22 18:55:47 2017

Input: Conference call transcript in JSON format 

Output: JSON file of the transript splitting Executieve and Analysts
utterances also adds a turn based pointer. 

@author: tomd
"""

import json
import sys
import codecs
from itertools import izip as zip, count
import io
from unidecode import unidecode

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

sys.stdout=codecs.getwriter('utf-8')(sys.stdout)

fname = "transcripts_may29const_Q4_16.json"

json_data=open('C:\\Users\\tomd\\pda\\' + fname ).read()
#transcripts_may29.json, transcripts_may29const_Q217,  transcripts_may29const_Q4_17
#transcripts_may29const_Q4_16

data = json.loads(json_data)

aQpos = []
eApos = []
analq = []
execsans = []
n = 1
q = 1

details = {}
transcript = {}
executives = []
analysts = []

#build analyst and executive lists
for entry in data:
    for executive in entry['entry']['exec']:
        if executive not in executives:
            executives.append(executive)

    for analyst in entry['entry']['analysts']:
        if analyst not in analysts:
            analysts.append(analyst)
    

    

#create list for just the names
anal = [analyst[0] for analyst in analysts]
execs = [executive[0] for executive in executives]

    
li = []
for entry in data:
   tran = entry['entry']
   for x in tran['questions']:
       li.append(unidecode(x))

for name in anal:
    print (name)
    person = [i for i, j in zip(count(), li) if j == name]
    print person
    aQpos.append({'analyst' :name, 'pos': person}) 
    for personPos in person:
        print "----- Analysts  #1  ------"
        print "personPos ", personPos
        print " n at top of loop", n

        tomIndex1 = next((index for (index, d) in enumerate(analq) if d["question"] == li[personPos+1]), None)
        print "tomIndex #1 ", tomIndex1
        if tomIndex1 == None:
            print "append #1 with ", personPos+1
            #print "level 0 ", li[personPos+1], personPos+1
            analq.append({'analyst': name, 'question' : li[personPos+1],  'sequence': personPos+1})
            n += personPos
            h = 1
            pp = personPos+1
            #if pp+h > len(li):
            #    break
            #else:
            try:
                if li[pp+h] not in execs and li[pp+h] not in anal:
                    morePara = True
                    while morePara: 
                        print "h item is ", li[pp+h], pp+h
                        if li[pp+h] not in execs and li[pp+h] not in anal and li[(pp+h)-1] not in execs:
                            print "append #2 with ", pp+h
                            analq.append({'analyst': name, 'question' : li[pp+h],  'sequence': pp+h})
                        else:
                            break#morePara = False
                        h +=1
                else:
                   print " this should be a person ", li[pp+h]
                   morePara = False
            except:
                print "list exhausted"
            
        else:
            print "already in dict at #1"
  
for ename in execs:
    print ename
    eperson = [i for i, j in zip(count(), li) if j == ename]
    print eperson
    eApos.append({'exec' :ename, 'pos': eperson}) 
    for epersonPos in eperson:
        print "----- Executives  #1  ------"
        print "personPos ", epersonPos
        print " q at top of loop", q

        eIndex = next((index for (index, d) in enumerate(execsans) if d["answer"] == li[epersonPos+1]), None)
        print "eIndex #1 ", eIndex
        if eIndex == None:
            print "eappend #1 with ", epersonPos+1
            print "elevel 0 ", epersonPos+1 #li[epersonPos+1], epersonPos+1
            execsans.append({'exec': ename, 'answer' : li[epersonPos+1], 'sequence' : epersonPos+1})
            q += personPos
            g = 1
            rr = epersonPos+1
            try:
                if li[rr+g] not in execs and li[rr+g] not in anal: 
                    emorePara = True
                    while emorePara: 
                        print "g at top is ",g
                        print "g item is ", li[rr+g], rr+g
                        if li[rr+g] not in execs and li[rr+g] not in anal and li[(rr+g)-1] not in anal:
                            print "eappend #2 with ", rr+g
                            execsans.append({'exec': ename, 'answer' : li[rr+g], 'sequence': rr+g})
                            print "g before incr ", g
                            g +=1
                            print " g at end of if ", g
                        else:
                            break#morePara = False
                        print " g at end of while ", g#g +=1
                else: 
                    emorePara = False
            except:
                print "list exhausted"
            
        else:
            print "already in dict at #1"    


details['title'] = entry['entry']['title']
details['company'] = entry['entry']['company']
details['executivesNames'] = executives
details['analystsNames'] = analysts
details['analysts'] = analq
details['execs'] = execsans
details['posexec'] = eApos
details['posanal'] = aQpos

transcript["entry"] = details

prefix = "transcript_may31_seq_result"
#suffix = "out"
#transcripts_results_ABI_Q1_16.json
with io.open('C:\\Users\\tomd\\pda\\' + prefix + fname, 'w', encoding='utf8' ) as outfile:
    bonn = json.dumps(transcript, outfile, indent = 4, ensure_ascii=False)
    outfile.write(to_unicode(bonn))
    
