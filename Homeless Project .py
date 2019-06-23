#!/usr/bin/env python
# coding: utf-8

# # How has Homelessness Changed in the US from 2010 to 2016?

# This dataset reports the national estimates of homelessness by state from 2007 - 2018. Estimates of homeless veterans are included from the beginning of 2011. This dataset was obtained from [**HUD EXCHANGE**](https://www.hudexchange.info/resource/3031/pit-and-hic-data-since-2007/).
# 

# ## Gather

# In[63]:


import pandas as pd
import zipfile
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')


# In[64]:


with zipfile.ZipFile('homelessness.zip', 'r') as myzip:
    myzip.extractall()


# In[65]:


df_homeless = pd.read_csv('2007-2016-Homelessnewss-USA.csv')
df_homeless


# ## Assess

# In[66]:


df_homeless.info()


# In[67]:


df_population = pd.read_csv('Population-by-state.csv')
df_population.head()


# In[68]:


df_population.info()


# ## Issues
# ### `df_homeless`
# 
# >1. Fix year column in `df_homeless` to fit *YYYY* format.
# >2. States are abbreviated for `df_homeless` but are in full in `df_population`.
# >3. Remove the extra states in `df_homeless` that don't appear in `df_population`.
# >4. Data organized by cities/counties in `df_homeless`.
# >5. Multiple Measures for each state in `df_homeless`.
# >6. Convert **'Count'** column from *str* to *int* in `df_homeless`.
# >7. Year in `df_homeless` dataframe should be a column not a row.
# 
# ### `df_population`
# >1. Rename columns for `df_population` for better clarity.
# >2. Delete 0 index row for `df_population`.
# >3. Convert column entries to *int*.

# ## Clean
# ### `df_homeless`

# In[69]:


# make copy of data set
df_homeless1 = df_homeless.copy()


# In[70]:


# drop 'CoC Number' from df_homeless
df_homeless1.drop('CoC Number', axis=1, inplace=True)


# > **Fix year column in df_homeless to fit YYYY format.**

# In[71]:


# Use only year values for the Year column.
df_homeless1['Year'] = df_homeless1['Year'].str[4:]


# > **States are abbreviated for df_homeless but are in full in df_population.**

# In[72]:


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


# > **Remove the extra states in `df_homeless` that don't appear in `df_population`.**

# In[73]:


# drop "VI" entries in State column
df_homeless2.drop(df_homeless2[df_homeless2.State == "VI"].index, inplace=True)


# In[74]:


# drop "GU" entries in State column
df_homeless2.drop(df_homeless2[df_homeless2.State == "GU"].index, inplace=True)


# In[75]:


# find all unique entries in State column
df_homeless2.State.unique()


# In[76]:


# reset index
df_homeless2.reset_index(drop=True)


# In[77]:


# ensure that unwanted entries have been removed
df_homeless2.shape


# > **Data organized by cities/counties in `df_homeless`.**

# In[78]:


# drop CoC Name column
df_homeless2.drop('CoC Name', axis=1, inplace=True)


# In[79]:


# make copy of df_homeless2
df_homeless_measures = df_homeless2.copy()


# > **Multiple Measures for each state in `df_homeless`.**

# In[80]:


# drop Measures column
df_homeless2.drop('Measures', axis=1, inplace=True)


# > **Convert 'Count' column from str to int in `df_homeless`.**

# In[81]:


# remove commas from Count column
df_homeless2['Count'] = df_homeless2['Count'].str.replace(',', '')


# In[82]:


# convert all entries in Count column from string to integer
df_homeless2['Count'] = pd.to_numeric(df_homeless2['Count'])


# In[83]:


# sum Count by state and year
d = {'Count': 'sum'}
df_homeless3 = df_homeless2.groupby(['Year', 'State']).aggregate(d)
df_homeless3


# In[84]:


# pivot table
df_homeless4 = pd.pivot_table(df_homeless3, values='Count', index=['State'], columns=['Year'], aggfunc=np.sum)
df_homeless4


# > **Drop 2007-2009 columns in df_homeless**

# In[85]:


# drop columns due df_population data set 
df_homeless4.drop(['2007', '2008', '2009'], axis=1, inplace=True)
df_homeless4


# 
# ### `df_population`

# > **Rename columns in `df_population`.**

# In[86]:


# rename columns
df_population1 = df_population.rename(columns={'GEO.display-label': 'State', 'respop72010': '2010', 'respop72011': '2011', 'respop72012': '2012', 'respop72013': '2013', 'respop72014': '2014', 'respop72015': '2015', 'respop72016': '2016'})


# > **Delete 0 index row for `df_population`**.

# In[87]:


# drop first row [0] of df_population
df_population1.drop([0], inplace=True)


# In[88]:


# drop first 'rescen42010' from df_population
df_population1.drop('rescen42010', axis=1, inplace=True)


# In[89]:


# drop first 'resbase42010' from df_population
df_population1.drop('resbase42010', axis=1, inplace=True)


# In[90]:


# drop first 'GEO.id' from df_population
df_population1.drop('GEO.id', axis=1, inplace=True)


# In[91]:


# drop first 'GEO.id2' from df_population
df_population1.drop('GEO.id2', axis=1, inplace=True)
df_population1


# In[92]:


# Make the state column the index
df_population1.set_index("State", inplace = True)
df_population1


# In[93]:


# Convert to int
df_population2 = df_population1.apply(pd.to_numeric)


# ## Check

# In[94]:


# Check info for df_homeless
df_homeless4.info()


# In[95]:


# Check info for df_population
df_population2.info()


# In[96]:


# Calculate percentage homeless
df_percentage_homeless = df_homeless4/df_population2
df_percentage_homeless


# In[97]:


# Write object to a comma-separated values (csv) file.
df_percentage_homeless.to_csv('df_percentage_homeless.csv')


# ### `df_homeless_measures `

# In[98]:


# remove commas from Count column
df_homeless_measures['Count'] = df_homeless_measures['Count'].str.replace(',', '')


# In[99]:


# convert all entries in Count column from string to integer
df_homeless_measures['Count'] = pd.to_numeric(df_homeless_measures['Count'])


# In[100]:


# sum Count by state, year, and measures
d = {'Count': 'sum'}
df_homeless_measures1 = df_homeless_measures.groupby(['Year', 'State', 'Measures']).aggregate(d)
df_homeless_measures1


# In[101]:


# Write object to a comma-separated values (csv) file.
df_homeless_measures1.to_csv('diff_homeless_measures.csv')


# ### `df_homeless_percent`

# In[102]:


# Transpose data set
df_percentage_homeless = df_percentage_homeless.T
df_percentage_homeless


# In[103]:


# Difference in percent homeless from 2010-2016
df_percentage_homeless.loc['Diff'] = df_percentage_homeless.loc['2016'] - df_percentage_homeless.loc['2010']
diff_homeless_percent = df_percentage_homeless.loc['Diff'].sort_values()
diff_homeless_percent


# In[104]:


# Convert diff_homeless_percent to data set
diff_homeless_percent_1 = diff_homeless_percent.reset_index()
diff_homeless_percent_1


# In[105]:


# Write object to a comma-separated values (csv) file.
diff_homeless_percent.to_csv('diff_homeless.csv')


# ## Visualize

# ### United States Change in Homeless Population from 2010 to 2016

# In[106]:


# Import Tableau Dashboard to Jupyter Notebooks (Change in Homelessness by State)


# In[107]:


get_ipython().run_cell_magic('HTML', '', "<div class='tableauPlaceholder' id='viz1560960628541' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Un&#47;UnitedStatesChangeinHomelessPopulation2010-2016&#47;Dashboard2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='UnitedStatesChangeinHomelessPopulation2010-2016&#47;Dashboard2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Un&#47;UnitedStatesChangeinHomelessPopulation2010-2016&#47;Dashboard2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1560960628541');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>")


# In[108]:


# Import Tableau Dashboard to Jupyter Notebooks (Change in Homelessness by State Bar Graph)


# In[109]:


get_ipython().run_cell_magic('HTML', '', "<div class='tableauPlaceholder' id='viz1560906912716' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ch&#47;ChangeinHomelessnessbyStateBarGraph&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='ChangeinHomelessnessbyStateBarGraph&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ch&#47;ChangeinHomelessnessbyStateBarGraph&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1560906912716');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>")


# In[110]:


# Convert diff_homeless_percent to data set
diff_homeless_percent_1 = diff_homeless_percent.reset_index()
diff_homeless_percent_1


# In[111]:


get_ipython().run_cell_magic('HTML', '', "<div class='tableauPlaceholder' id='viz1560913331810' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ch&#47;ChangeinHomelessPopulationHeatMap&#47;Dashboard3&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='ChangeinHomelessPopulationHeatMap&#47;Dashboard3' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ch&#47;ChangeinHomelessPopulationHeatMap&#47;Dashboard3&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1560913331810');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>")


# #### Results
# - 26 states have decreased the percentage of homeless people in their state.
# - 26 states have increased the percentage of homeless people in their state.

# #### Ranking: States that have decreased the rate of homelessness the most
# 1. Louisiana -0.8609%
# 2. Florida -0.4739%
# 3. Nevada -0.4161%
# 4. Oregon -0.3337%
# 5. Colorado -0.2807%
# 6. Georgia -0.2659%
# 7. Arizona -0.1966%
# 8. Nebraska -0.1948%
# 9. Texas -0.1839%
# 10.	Kentucky -0.1703%
# 11.	Maryland -0.1685%
# 12.	West Virginia -0.1607%
# 13.	New Jersey -0.1537%
# 14.	Alabama	-0.1357%
# 15.	New Mexico -0.1273%
# 16.	Virginia -0.1185%
# 17.	Mississippi -0.1119%
# 18.	Michigan -0.0956%
# 19.	North Carolina -0.0712%
# 20.	Utah -0.0639%
# 21.	Ohio -0.0383%
# 22.	Illinois -0.0322%
# 23.	Oklahoma -0.0309%
# 24.	Tennessee -0.0291%
# 25.	Missouri -0.0204%
# 26.	Montana	-0.0021%
# 27.	Connecticut	0.0004%
# 28.	Washington 0.0056%
# 29.	Wisconsin 0.0079%
# 30.	Indiana	0.0154%
# 31.	New Hampshire 0.0271%
# 32.	Arkansas 0.0363%
# 33.	Minnesota 0.0415%
# 34.	Rhode Island 0.0455%
# 35.	Iowa 0.0598%
# 36.	Delaware 0.0749%
# 37.	Maine 0.0787%
# 38.	Kansas 0.0797%
# 39.	Idaho 0.0803%
# 40.	Vermont	0.1005%
# 41.	Pennsylvania 0.1150%
# 42.	South Carolina 0.1300%
# 43.	North Dakota 0.1389%
# 44.	Alaska 0.1683%
# 45.	Puerto Rico	0.1945%
# 46.	South Dakota 0.2088%
# 47.	California 0.2129%
# 48.	Wyoming	0.2686%
# 49.	Massachusetts 0.3155%
# 50.	New York 0.6215%
# 51.	Hawaii 1.1532%
# 52.	District of Columbia 1.5600%

# In[112]:


# Import Tableau Dashboard to Jupyter Notebooks (Percentage Homeless in 2016)


# In[113]:


get_ipython().run_cell_magic('HTML', '', "<div class='tableauPlaceholder' id='viz1560960701231' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Pe&#47;PercentofStatePopulationHomelessin2016&#47;Dashboard4&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='PercentofStatePopulationHomelessin2016&#47;Dashboard4' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Pe&#47;PercentofStatePopulationHomelessin2016&#47;Dashboard4&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1560960701231');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>")


# In[114]:


# Import Tableau Bar Chart to Jupyter Notebook (Percentage Homeless in 2016)


# In[115]:


get_ipython().run_cell_magic('HTML', '', "<div class='tableauPlaceholder' id='viz1560963028192' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Pe&#47;PercentofStatePopulationHomelessin2016BarChart&#47;Dashboard5&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='PercentofStatePopulationHomelessin2016BarChart&#47;Dashboard5' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Pe&#47;PercentofStatePopulationHomelessin2016BarChart&#47;Dashboard5&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1560963028192');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='1709px';vizElement.style.height='931px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>")


# # Breakdown of Homelessness

# In[116]:


# Import Tableau Treemap to Jupyter Notebook (Breakdown of State Homelessness by Year)


# In[117]:


get_ipython().run_cell_magic('HTML', '', "<div class='tableauPlaceholder' id='viz1561052669382' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Br&#47;BreakdownofStateHomelessnessbyYear&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='BreakdownofStateHomelessnessbyYear&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Br&#47;BreakdownofStateHomelessnessbyYear&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1561052669382');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>")


# In[118]:


# Import Tableau Line Graph to Jupyter Notebook (Changes in Homelessness Over the Years)


# In[119]:


get_ipython().run_cell_magic('HTML', '', "<div class='tableauPlaceholder' id='viz1561175150476' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ch&#47;ChangesinHomelessnessOvertheYears&#47;Dashboard2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='ChangesinHomelessnessOvertheYears&#47;Dashboard2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ch&#47;ChangesinHomelessnessOvertheYears&#47;Dashboard2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1561175150476');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>")
