# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 14:25:57 2019

@author: willi
"""
import pandas as pd
pd.options.display.float_format = '{:.2f}'.format
final_phase_df = pd.read_csv('C:/Users/willi/OneDrive/Documents/GitHub/Revolving_Door_Network_Project/revolving_door_pairs.csv')

financials = pd.read_csv('C:/Users/willi/OneDrive/Documents/GitHub/Revolving_Door_Network_Project/FEC_financial_filings_2017_Present.csv')
cols = [0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,27,28,29,30,31,32]
financials.drop(financials.columns[cols],axis=1,inplace=True)

financials['CAND_F_NAME'] = financials['CAND_F_NAME'].str.lower()
financials['CAND_F_NAME'] = financials['CAND_F_NAME'].astype(str)
financials['CAND_F_NAME'] = financials['CAND_F_NAME'].str.replace(",","")
financials['CAND_F_NAME'] = financials['CAND_F_NAME'].str.replace(";","")
financials['CAND_F_NAME'] = financials['CAND_F_NAME'].str.replace(".","")
financials['CAND_F_NAME'] = financials['CAND_F_NAME'].str.replace(":","")
financials['CAND_F_NAME'] = financials['CAND_F_NAME'].str.strip()

financials['CAND_L_NAME'] = financials['CAND_L_NAME'].str.lower()
financials['CAND_L_NAME'] = financials['CAND_L_NAME'].astype(str)
financials['CAND_L_NAME'] = financials['CAND_L_NAME'].str.replace(",","")
financials['CAND_L_NAME'] = financials['CAND_L_NAME'].str.replace(";","")
financials['CAND_L_NAME'] = financials['CAND_L_NAME'].str.replace(".","")
financials['CAND_L_NAME'] = financials['CAND_L_NAME'].str.replace(":","")
financials['CAND_L_NAME'] = financials['CAND_L_NAME'].str.strip()


# new data frame with split value columns 
new = financials["CAND_F_NAME"].str.split(" ", n = 1, expand = True) 
financials['CAND_F_NAME'] = new[0]

financials['rep_name'] = financials['CAND_F_NAME'] + " " + financials['CAND_L_NAME']
cols2 = [0,1]
financials.drop(financials.columns[cols2],axis=1,inplace=True)


financials = financials.groupby('rep_name').sum()


financials = pd.merge(final_phase_df, financials, how='left', left_on='full_name', right_index=True)

financials.to_csv('C:/Users/willi/OneDrive/Documents/GitHub/Revolving_Door_Network_Project/revolving_pairs_with_financials.csv', index=False)