# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 12:10:34 2019

@author: willi
"""

import xml.etree.cElementTree as ET
import pandas as pd
import os


d = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
last_name_list = []
first_name_list = []
reg_desc_list = []

def parseXML_2(path):

    for filename in os.listdir(path):
        fullname = os.path.join(path, filename)
        tree = ET.parse(fullname)



        root = tree.getroot()

        for e in root.iter('lobbyistLastName'):
            last_name = e.text
            last_name_list.append(last_name)

        #df['LastName'] = last_name_list

        for e in root.iter('lobbyistFirstName'):
            first_name = e.text
            first_name_list.append(first_name)
        #df['FirstName'] = first_name_list
        #df["lobbyist_name"] = df["FirstName"].map(str) +" " +df["LastName"]
        #del df['LastName']
        #del df['FirstName']

        for e in root.iter('coveredPosition'):
            reg_desc = e.text
            reg_desc_list.append(reg_desc)
        #df['covered_position'] = reg_desc_list
        #df['LastName'] = last_name_list
        #df['FirstName'] = first_name_list


parseXML_2('C:/Users/willi/OneDrive/Documents/GitHub/Revolving_Door_Network_Project/2019_XML_Files')
full = list(zip(first_name_list, last_name_list,reg_desc_list))



df = pd.DataFrame(full,columns=['first_name','last_name','position'])



for index, row in df.iterrows():
    if not any(x in row['first_name'] for x in d):
        df = df.drop(index)

for index, row in df.iterrows():
    try:
        if not any(x in row['position'] for x in d):
            df = df.drop(index)
    except TypeError:
        pass

df = df.dropna()
    

df['first_name'] = df['first_name'].str.strip()
df['last_name'] = df['last_name'].str.strip()
df['position'] = df['position'].str.strip()    
df.drop_duplicates(subset=None, keep="first",inplace=True)
df["lobbyist_name"] = df["first_name"].map(str) +" " +df["last_name"]
del df['last_name']
del df['first_name']
df = df[['lobbyist_name','position']]

df.to_csv('C:/Users/willi/OneDrive/Documents/GitHub/Revolving_Door_Network_Project\df.csv', index=False)
        
