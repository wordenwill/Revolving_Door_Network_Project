# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 11:05:05 2019

@author: willi
"""

import pandas as pd
import nltk
from nltk.tag.stanford import StanfordNERTagger


st = StanfordNERTagger('C:/Users/willi/OneDrive/Documents/GitHub/Revolving_Door_Network_Project/stanford-ner/stanford-ner-2017-06-09/english.all.3class.distsim.crf.ser.gz',
                       'C:/Users/willi/OneDrive/Documents/GitHub/Revolving_Door_Network_Project/stanford-ner/stanford-ner-2017-06-09/stanford-ner.jar')

df = pd.read_csv('C:/Users/willi/OneDrive/Documents/GitHub/Revolving_Door_Network_Project/df.csv')
df['position'] = df['position'].astype(str)

import os
java_path = 'C:/Program Files/Java/jdk-12.0.1/bin/java.exe'
os.environ['JAVAHOME'] = java_path


texts = df['position'].tolist()
texts_sample = texts[0:5]

name_list = []
name_list2 = []

for row in texts_sample:
    for sent in nltk.sent_tokenize(row):
        tokens = nltk.tokenize.word_tokenize(sent)
        tags = st.tag(tokens)
        name_list.append(tags)

for row in name_list:    
    out_tup = [i for i in row if i[1] == "PERSON"]
    name_list2.append(out_tup)

out_tup_list = []
for each in name_list2:
    OutputTuple = [(a) for a, b in each]
    out_tup_list.extend(OutputTuple)

for each in name_list2:
    print(len(each))
