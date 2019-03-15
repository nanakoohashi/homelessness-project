#!/usr/bin/env python
# coding: utf-8

# In[22]:


import pandas as pd
import zipfile


# In[23]:


with zipfile.ZipFile('homelessness.zip', 'r') as myzip:
    myzip.extractall()


# In[24]:


df_homeless = pd.read_csv('2007-2016-Homelessnewss-USA.csv')
df_homeless


# ## Assess
# In[25]:


df_homeless.info()


# In[26]:


df_population = pd.read_csv('Population-by-state.csv')
df_population.head()


# In[27]:


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

# In[28]:


df_homeless1 = df_homeless[df_homeless.Measures == 'Total Homeless']


# In[29]:


# drop 'CoC Number' from df_homeless
df_homeless1.drop('CoC Number', axis=1, inplace=True)


# In[30]:


# Use only year values for the Year column.

df_homeless1['Year'] = df_homeless1['Year'].str[4:]


# In[31]:


# Rename State column values

df_homeless2= df_homeless1.replace({'State' : {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
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
    'PR': 'Puerto Rico',
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


# In[32]:


df_homeless2.drop(df_homeless2[df_homeless2.State == "VI"].index, inplace=True)


# In[33]:


df_homeless2.drop(df_homeless2[df_homeless2.State == "GU"].index, inplace=True)


# In[34]:


df_homeless2.State.unique()


# In[35]:


df_homeless2.reset_index(drop=True)


# In[41]:


df_homeless2.shape


# In[42]:


df_homeless2.drop('CoC Name', axis=1, inplace=True)


# In[44]:


df_homeless2.drop('Measures', axis=1, inplace=True)


# In[49]:


df_homeless2['Count'] = df_homeless2['Count'].str.replace(',', '')


# In[50]:


df_homeless2['Count'] = pd.to_numeric(df_homeless2['Count'])


# In[51]:

d = {'Count': 'sum'}
df_homeless3 = df_homeless2.groupby(['Year', 'State']).aggregate(d)
df_homeless3


# ### df_population

# #### Define

# In[ ]:


df_population1 = df_population.rename(columns={'GEO.display-label': 'State', 'respop72010': '2010', 'respop72011': '2011', 'respop72012': '2012', 'respop72013': '2013', 'respop72014': '2014', 'respop72015': '2015', 'respop72016': '2016'})
df_population1


# In[ ]:


# drop first row [0] of df_population
df_population1.drop([0], inplace=True)


# In[ ]:


# drop first 'rescen42010' from df_population
df_population1.drop('rescen42010', axis=1, inplace=True)


# In[ ]:


# drop first 'resbase42010' from df_population
df_population1.drop('resbase42010', axis=1, inplace=True)


# In[ ]:


# drop first 'GEO.id' from df_population
df_population1.drop('GEO.id', axis=1, inplace=True)


# In[ ]:


# drop first 'GEO.id2' from df_population
df_population1.drop('GEO.id2', axis=1, inplace=True)
df_population1


# In[ ]:




