# -*- coding: utf-8 -*-
"""
Created on Sun Jun 04 12:15:57 2017

@author: tomd
"""

import json
import sys
import codecs
import io
from unidecode import unidecode

try:
    doUnicode = unicode
except NameError:
    doUnicode = str


sys.stdout=codecs.getwriter('utf-8')(sys.stdout)

#fname = "transcript_may31_seq_resulttranscripts_may31_TAP_Q2_16.json"
fname = "transcript_may31_seq_resultDiageo-Europe-Russia-and-Turkey-Call-with-the-Pres_09_16.json"
#transcript_may31_seq_resulttranscripts_may29_DEO_q2_15.json"
#transcript_may31_seq_resulttranscripts_may31_BrownF.B_Q1_16.json"
#transcript_may31_seq_resulttranscripts_may31_HEINY_Q2_16.json"
#transcript_may31_seq_resulttranscripts_may31_Pernod_Q2_17.json"
#transcript_may31_seq_resulttranscripts_may31_TAP_Q1_16.json"
#transcript_may31_seq_resulttranscripts_may31_TSRYY_17.json"
#"transcript_may31_seq_resulttranscripts_may29abi_Q1_17.json" 
#"transcript_may31_seq_resulttranscripts_may29const_Q1_16.json"



json_data=open('C:\\Users\\tomd\\pda\\' + fname ).read()

data = json.loads(json_data)

text = ''
anexec = "John Kennedy"#"Deirdre Mahlan"#"Ivan Menezes"#"Kathryn Mikells"#"Deirdre A. Mahlan"#"Ivan M. Menezes"
#"Paul Varga"#"Jane Morreau"##"Brian Fitzgerald"#"Jay Koval" 
#"Sonya Ghobrial"#"Laurence Debroux"#"Jean-Francois van Boxmeer"#"Rene Hooft Graafland"# 
#"Alexandre Ricard"#"Julia Massies"#"Gilles Bogaert"#"Jean Touboul"#"Pierre Pringuet"#"Alexandre Ricard"#
#"Simon Cox"#"Dave Dunnewald"#"Gavin Hattersley"#"Mark Hunter"#"Krishnan Anand"
#"Stewart Glendinning"#"Mauricio Restrepo"# 
#"Stewart Glendinning"#"Tracey Joubert" 
#"Carlos Brito" #Rob Sands" #"David Klein" #"Robert Sands" 

i = 0
execeach = {}
resplen = []

for entry in data:
    for executive in entry['entry']['execs']:
        if executive['exec'] == anexec: #"Mark Hunter":
           #print executive['answer']
           text =  text + ' ' + executive['answer']
           resplen.append(executive['answer'])
           i += 1
#print i 

execeach['execName'] = anexec
execeach['execRespCount'] = i
execeach['execResp'] = resplen

prefix = execeach['execName'] + "_text_jun14_"

'''
prefix = execeach['execName'] + "text_jun14_"
with open('C:\\Users\\tomd\\pda\\textout\\execEach\\' + prefix + fname + '.txt', 'w') as text_file:
    text_file.write(execeach)
'''
with io.open('C:\\Users\\tomd\\pda\\textout\\execEach\\' + prefix + fname, 'w', encoding='utf8' ) as outfile:
    bonn = json.dumps(execeach, outfile, indent = 4, ensure_ascii=False)
    outfile.write(doUnicode(bonn))
