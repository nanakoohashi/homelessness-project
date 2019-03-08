#!/usr/bin/env python
# coding: utf-8

# ## Gather

# In[1]:


import pandas as pd
import zipfile


# In[2]:


with zipfile.ZipFile('homelessness.zip', 'r') as myzip:
    myzip.extractall()


# ## Assess
# 

# In[4]:


# dataset 1 -
df_homeless = pd.read_csv('2007-2016-Homelessnewss-USA.csv')
df_homeless.head()


# In[11]:


df_homeless.info()


# In[9]:


df_population = pd.read_csv('Population-by-state.csv')
df_population.head()


# In[10]:


df_population.info()


# In[ ]:




