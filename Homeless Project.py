#!/usr/bin/env python
# coding: utf-8

# In[59]:


import pandas as pd
import zipfile


# In[60]:


with zipfile.ZipFile('homelessness.zip', 'r') as myzip:
    myzip.extractall()


# In[61]:


df_homeless = pd.read_csv('2007-2016-Homelessnewss-USA.csv')
df_homeless


# In[62]:


df_homeless.info()


# In[63]:


df_population = pd.read_csv('Population-by-state.csv')
df_population.head()


# In[64]:


df_population.info()


# - States are abbreviated for df_homeless but are in full in population.
# - Fix year column in df_homeless to fit YYYY format.
# - Change 'Geography' to 'State' for df_population.
# - Rename columns for df_population for better clarity.
# - Delete 0 index row for df_population.
# - Merge data frames.

# ## Clean
# ### df_homeless

# - keep all rows with Measures == Total Homeless

# In[65]:


df_homeless1 = df_homeless[df_homeless.Measures == 'Total Homeless']
df_homeless1


# ### df_population

# #### Define

# In[67]:


df_population1 = df_population.rename(columns={'GEO.display-label': 'State', 'respop72010': 'Population_2010', 'respop72011': 'Population_2011', 'respop72012': 'Population_2012', 'respop72013': 'Population_2013', 'respop72014': 'Population_2014', 'respop72015': 'Population_2015', 'respop72016': 'Population_2016'})
df_population1


# In[68]:


# drop first row [0] of df_population
df_population1.drop([0], inplace=True)


# In[69]:


# drop first 'rescen42010' from df_population
df_population1.drop('rescen42010', axis=1, inplace=True)


# In[70]:


# drop first 'resbase42010' from df_population
df_population1.drop('resbase42010', axis=1, inplace=True)


# In[71]:


# drop first 'GEO.id' from df_population
df_population1.drop('GEO.id', axis=1, inplace=True)


# In[72]:


# drop first 'GEO.id2' from df_population
df_population1.drop('GEO.id2', axis=1, inplace=True)
df_population1


# In[ ]:




