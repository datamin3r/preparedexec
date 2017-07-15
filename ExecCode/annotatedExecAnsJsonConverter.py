# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 12:03:04 2017

@author: tomd
"""
import json
import sys
import codecs
import io
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

result = pd.read_csv('C:\\Users\\tomd\\pda\\ExecAnnotated_for_json_input.csv')
result_dict = result.to_dict('records')

'''
for entry in result_dict:
    for answer in entry['entry']#['execs']:
        if executive['exec'] == anexec: #"Mark Hunter":
           #print executive['answer']
           text =  text + ' ' + executive['answer']
           resplen.append(executive['answer'])
#           i += 1
#print i 

execeach['execName'] = anexec
#execeach['execRespCount'] = i
execeach['execResp'] = resplen

prefix = execeach['execName'] + "_text_jun14_"

'''

with io.open('C:\\Users\\tomd\\pda\\textout\\execEach\\AnnotatedExecAnsers.json', 'w', encoding='utf8' ) as outfile:
    bonn = json.dumps(result_dict, outfile, indent = 4, ensure_ascii=False)
    outfile.write(doUnicode(bonn))