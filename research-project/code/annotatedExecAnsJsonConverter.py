# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 12:03:04 2017

@author: tomd

Script to prepare JSON input 
AnnotatedExecAnswers_197.json for dowstream
model performance evaluation against the annotated 
classifiedExecAnswers_197_v0.1.csv

Input csv file of the executive answers

Output JSON file of executive anwsers

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


with io.open('C:\\Users\\tomd\\pda\\textout\\execEach\\AnnotatedExecAnsers.json', 'w', encoding='utf8' ) as outfile:
    bonn = json.dumps(result_dict, outfile, indent = 4, ensure_ascii=False)
    outfile.write(doUnicode(bonn))