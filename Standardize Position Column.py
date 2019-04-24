# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 15:31:16 2019

@author: willi
"""
import pandas as pd
from collections import Counter
import itertools
import numpy as np



df = pd.read_csv('C:/Users/willi/OneDrive/Documents/GitHub/Revolving_Door_Network_Project\df.csv')
congressman = pd.read_csv('C:/Users/willi/OneDrive/Documents/GitHub/Revolving_Door_Network_Project\congressman_names.csv')


df['position'] = df['position'].str.lower()
df['position'] = df['position'].astype(str)
df['position'] = df['position'].str.replace(",","")
df['position'] = df['position'].str.replace(";","")
df['position'] = df['position'].str.replace(".","")
df['position'] = df['position'].str.replace(":","")
df['position'] = df['position'].str.strip()

def split_words(input):

    #split the input
    words = input.str.split()

    for i in words:
        word_list.append(i)

    return word_list

word_list = []

split_words(df['position'])

cnt = Counter()
for entry in word_list:
    for word in entry:
        cnt[word] +=1

congressman['first_name'] = congressman['first_name'].str.strip()
congressman['first_name'] = congressman['first_name'].str.lower()
congressman['first_name'] = congressman['first_name'].astype(str)


congressman['last_name'] = congressman['last_name'].str.strip()
congressman['last_name'] = congressman['last_name'].str.lower()
congressman['last_name'] = congressman['last_name'].astype(str)

for entry in word_list:
    for word in entry:
        word = word.strip()

f_name_list = list(congressman['first_name'])
l_name_list = list(congressman['last_name'])

positions_list = df['position'].tolist()



new_list = [[y for y in x if y in f_name_list or y in l_name_list] for x in word_list]


f_name_count_list = []
l_name_count_list = []
for row in new_list:
    f_name_count = 0
    l_name_count = 0
    for word in row:
        if word in l_name_list:
            l_name_count += 1
        elif word in f_name_list:
            f_name_count += 1

    f_name_count_list.append(f_name_count)
    l_name_count_list.append(l_name_count)



    
full_name_count_list = pd.DataFrame(
        {'FirstNameCount': f_name_count_list,
        'LastNameCount': l_name_count_list,
        })

name_num = []
for each in new_list:
    l = len(each)
    name_num.append(l)
    
full_name_count_list['TotalCount'] = full_name_count_list['FirstNameCount'] + full_name_count_list['LastNameCount']  

 


         