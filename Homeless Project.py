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

# In[14]:


# dataset 1 - homelessness data
df_homeless = pd.read_csv('2007-2016-Homelessnewss-USA.csv')
df_homeless


# In[11]:


df_homeless.info()


# In[13]:


# dataset 2 - population data
df_population = pd.read_csv('Population-by-state.csv')
df_population.head()


# In[10]:


df_population.info()
#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import zipfile


# In[4]:


with zipfile.ZipFile('homelessness.zip', 'r') as myzip:
    myzip.extractall()


# In[5]:


df_homeless = pd.read_csv('2007-2016-Homelessnewss-USA.csv')
df_homeless


# In[6]:


df_homeless.info()


# In[7]:


df_population = pd.read_csv('Population-by-state.csv')
df_population.head()


# In[8]:


df_population.info()


# - States are abbreviated for df_homeless but are in full in population.
# - Change 'Geography' to 'State' for df_population.
# - Rename columns for df_population for better clarity.
# - Delete 0 index row for df_population.
# - Merge data frames.

# ## Clean
# 
# #### Define

# In[9]:


#rename columns for df_population

df_population1 = df_population.rename(columns={'GEO.display-label': 'State', 'respop72010': 'Population_2010', 'respop72011': 'Population_2011', 'respop72012': 'Population_2012', 'respop72013': 'Population_2013', 'respop72014': 'Population_2014', 'respop72015': 'Population_2015', 'respop72016': 'Population_2016'})
df_population1


# In[11]:


# drop first row [0] of df_population
df_population1.drop([0])



# - States are abbreviated for df_homeless but are in full in population.
# - Change 'Geography' to 'State' for df_population.
# - Rename columns for df_population for better clarity.
# - Delete 0 index row for df_population.
# - Merge data frames.

# ## Clean

# #### Define

# In[22]:


df_population1 = df_population.rename(columns={'GEO.display-label': 'State', 'respop72010': 'Population_2010', 'respop72011': 'Population_2011', 'respop72012': 'Population_2012', 'respop72013': 'Population_2013', 'respop72014': 'Population_2014', 'respop72015': 'Population_2015', 'respop72016': 'Population_2016'})
df_population1

# In[11]:


# drop first row [0] of df_population
df_population1.drop([0])

# In[16]:

# drop 'rescen42010' column from df_population
df_population1.drop('rescen42010', axis=1, inplace=True)

# In[17]:

# drop 'resbase42010' from df_population
df_population1.drop('resbase42010', axis=1, inplace=True)
