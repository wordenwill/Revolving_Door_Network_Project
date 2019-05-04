import pandas as pd
from collections import Counter


df = pd.read_csv('C:/Users/willi/OneDrive/Documents/GitHub/Revolving_Door_Network_Project\df.csv')

#Read in a dataset of names of all US Congressmen and women who have served between 1960 to the present
congressman = pd.read_csv('C:/Users/willi/OneDrive/Documents/GitHub/Revolving_Door_Network_Project\congressman_names.csv')

#Clean up the columns from the DF produced by XML parsing
df['lobbyist_name'] = df['lobbyist_name'].str.lower()
df['position'] = df['position'].str.lower()
df['position'] = df['position'].astype(str)
df['position'] = df['position'].str.replace(",","")
df['position'] = df['position'].str.replace(";","")
df['position'] = df['position'].str.replace(".","")
df['position'] = df['position'].str.replace(":","")
df['position'] = df['position'].str.strip()

#This function takes will take the string in the position description and break it up into individual words 
def split_words(input):
    #split the input
    words = input.str.split()
    for i in words:
        word_list.append(i)
    return word_list
word_list = []
split_words(df['position'])
########################################################################

#Clean up the columns in the congressional names df
congressman['first_name'] = congressman['first_name'].str.strip()
congressman['first_name'] = congressman['first_name'].str.lower()
congressman['first_name'] = congressman['first_name'].astype(str)

congressman['last_name'] = congressman['last_name'].str.strip()
congressman['last_name'] = congressman['last_name'].str.lower()
congressman['last_name'] = congressman['last_name'].astype(str)

congressman['full_name'] = congressman['full_name'].str.strip()
congressman['full_name'] = congressman['full_name'].str.lower()
congressman['full_name'] = congressman['full_name'].astype(str)
##########################################################################

#Stripping out any blanks in the word list that could alter the matching
for entry in word_list:
    for word in entry:
        word = word.strip()

#Create lists out of the congressional names DF
f_name_list = list(congressman['first_name'])
l_name_list = list(congressman['last_name'])
full_name_list = list(congressman['full_name'])

#This list comprehension will take the elements in the broken up list of words from the position description and keep only 
#the word strings that can be found in the list of either congressional first or last names
new_list = [[y for y in x if y in f_name_list or y in l_name_list] for x in word_list]

# Because I used a list comprehension to reduce the position descriptions down to names,
# I now need to piece first and last names together where available. This loop looks through
# the condensed list and checks the congressional names. If found, they will be combined into 
#  asingle string
row = 0
test_list = []
for each in new_list:
    l_name = 1
    f_name = 0
    sublist = []
    if len(each) >= 2:
        while len(each) > l_name :
                        
            if each[f_name] + " " + each[l_name] in full_name_list:
                sublist.append(each[f_name] + " " + each[l_name])
            elif each[f_name] in l_name_list:
                sublist.append(each[f_name])
            
            f_name += 1
            l_name += 1
    
    test_list.append(sublist)
    row += 1
###################################################################################


row = 0
for x in test_list:
    if len(x) == 0:
        test_list[row] = new_list[row]
    row +=1

####################################################################################
#This section focuses on adjusting the list size and shape
    
# The name_num_list will tell me how many congressional names are in the list associated with a particular lobbyist.
# I will use this number to extend the lobby list accordingly
name_num_list = []
for x in test_list:
    #if len(x) == 0:
        #name_num_list.append(1)
    #else:
    name_num_list.append(len(x))
        

#Get list of lobbyist names to the right size
lobby_long_list = []
for each in df['lobbyist_name']:
    lobby_long_list.append([each])
lobby_long_list = [a*b for a,b in zip(lobby_long_list,name_num_list)]
lobby_long_list = [x for x in lobby_long_list if x != []]
flat_lobbyist_list = [item for sublist in lobby_long_list for item in sublist]

#Get list of representative names to the right size
flat_rep_list = [item for sublist in test_list for item in sublist]

#Combine the lists
combined = list(zip(flat_lobbyist_list, flat_rep_list,))

processed_df = pd.DataFrame(combined,columns=['lobbyist_name','worked_for'])
##########################################################################################



merged = processed_df.merge(congressman,left_on='worked_for',right_on='last_name', how='left')

name_count = Counter(congressman['last_name'])
name_count_df = pd.DataFrame.from_dict(name_count, orient='index')
merged = merged.join(name_count_df, on = 'worked_for')

merged['full_name'].isnull()
merged['full_name'].fillna(merged['worked_for'], inplace=True)  

boolean_filter = []
for each in merged['full_name']:
    boolean_filter.append(' ' in each)

merged['bool'] = boolean_filter


merged = merged[merged['bool'] == True]
merged = merged.fillna(0)
final_dataset = merged.loc[merged[0] <= 1] 


cols = [1,2,3,5,6]
final_dataset.drop(final_dataset.columns[cols],axis=1,inplace=True)
final_dataset = final_dataset.drop_duplicates()

final_dataset.to_csv('C:/Users/willi/OneDrive/Documents/GitHub/Revolving_Door_Network_Project/revolving_door_pairs.csv', index=False)





            