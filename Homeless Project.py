#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import zipfile


# In[2]:


with zipfile.ZipFile('homelessness.zip', 'r') as myzip:
    myzip.extractall()


# In[3]:


df_homeless = pd.read_csv('2007-2016-Homelessnewss-USA.csv')
df_homeless


# In[4]:


df_homeless.info()


# In[5]:


df_population = pd.read_csv('Population-by-state.csv')
df_population.head()


# In[6]:


df_population.info()


# - States are abbreviated for df_homeless but are in full in population.
# - Fix year column in df_homeless to fit YYYY format.
# - Data organized by cities/counties in df_homeless.
# - Multiple Measures for each state in df_homeless.
# - Change 'Geography' to 'State' for df_population.
# - Rename columns for df_population for better clarity.
# - Delete 0 index row for df_population.
# - Merge data frames.

# ## Clean
# ### df_homeless

# - keep all rows with Measures == Total Homeless

# In[7]:


df_homeless1 = df_homeless[df_homeless.Measures == 'Total Homeless']


# In[8]:


# drop 'CoC Number' from df_homeless
df_homeless1.drop('CoC Number', axis=1, inplace=True)


# # For completion on 03/12
# - reformat Year column 
# - rename State column values
# - sum Total homeless by state

# In[9]:


# Use only year values for the Year column.

df_homeless1['Year'] = df_homeless1['Year'].str[4:]


# In[10]:


# Rename State column values

df_homeless2= df_homeless1.replace({'State' : {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
    }})
df_homeless2


# 
# ### df_population

# #### Define

# In[11]:


df_population1 = df_population.rename(columns={'GEO.display-label': 'State', 'respop72010': '2010', 'respop72011': '2011', 'respop72012': '2012', 'respop72013': '2013', 'respop72014': '2014', 'respop72015': '2015', 'respop72016': '2016'})
df_population1


# In[12]:


# drop first row [0] of df_population
df_population1.drop([0], inplace=True)


# In[13]:


# drop first 'rescen42010' from df_population
df_population1.drop('rescen42010', axis=1, inplace=True)


# In[14]:


# drop first 'resbase42010' from df_population
df_population1.drop('resbase42010', axis=1, inplace=True)


# In[15]:


# drop first 'GEO.id' from df_population
df_population1.drop('GEO.id', axis=1, inplace=True)


# In[16]:


# drop first 'GEO.id2' from df_population
df_population1.drop('GEO.id2', axis=1, inplace=True)
df_population1
