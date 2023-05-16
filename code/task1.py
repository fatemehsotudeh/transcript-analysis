#!/usr/bin/env python
# coding: utf-8

#    # find the body, start and end time of each story in the news show

# ______________________________________________________________________

# ## 1- Import libraries

# In[1]:


import numpy as np
import pandas as pd
import os, json
import re


# ## 2- Write the required functions

# In[2]:


def read_json_files(path_to_json_files = '../data'):
    #get all JSON file names as a list
    json_file_names = [filename for filename in os.listdir(path_to_json_files) if filename.endswith('.json')]

    json_text={}
    for json_file_name in json_file_names:
        with open(os.path.join(path_to_json_files, json_file_name)) as json_file:
            json_text[json_file_name[:json_file_name.find('.')]] = json.load(json_file)
    
    return json_text


# In[3]:


def find_index(string,words):
    match= re.search(words,string)
    if match:
         return {
        'start_index':match.start(),
        'end_index':match.end()
        }
    else:
        return False


# In[4]:


def extract_text(string,start_index,end_index):
    return string[start_index:end_index]


# In[5]:


def add_columns(df, col_names,values):
    for i in range(len(col_names)):
        if col_names[i] not in df.columns:
            df[col_names[i]]=values[i]

    return df


# In[6]:


def count_words(string):
    return len(string.split(' '))


# ## 3- Load the datas

# In[7]:


# read transcription file of news shows 
news=read_json_files()


# In[8]:


to_fill_path='../data/to_fill.csv'
df=pd.read_csv(to_fill_path)


# ## 4- extract the body,start and end time

# In[9]:


bodies, start_times, end_times=([] for i in range(3))

for index,row in df.iterrows():
    body=start_time=end_time=''
    
    video_id=str(row['source_video_id'])
    video_text=news[video_id]['text']
    
    if ((first_words:=find_index(video_text,row['first_words'])) and (last_words:=find_index(video_text,row['last_words']))):
        start_index, end_index= first_words['start_index'], last_words['end_index']
        body=extract_text(video_text,start_index,end_index)
        start_time=news[video_id]['words'][count_words(video_text[:start_index-1])]['start']
        end_time=news[video_id]['words'][count_words(video_text[:end_index])-1]['end']               
    else:
        body=start_time=end_time='Not found'                                       
        
    bodies.append(body)
    start_times.append(start_time)
    end_times.append(end_time)                                               


# ## 5- add 3 column(body,start,end) to dataframe

# In[10]:


df=add_columns(df,['body','start','end'],[bodies,start_times,end_times])


# ## 6- convert dataframe to csv

# In[11]:


df.to_csv(to_fill_path,index=False)


# In[ ]:




