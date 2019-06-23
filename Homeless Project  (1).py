#!/usr/bin/env python
# coding: utf-8

# # How has Homelessness Changed in the US from 2010 to 2016?

# This dataset reports the national estimates of homelessness by state from 2007 - 2018. Estimates of homeless veterans are included from the beginning of 2011. This dataset was obtained from [**HUD EXCHANGE**](https://www.hudexchange.info/resource/3031/pit-and-hic-data-since-2007/).
# 

# ## Gather

# In[1]:


import pandas as pd
import zipfile
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


with zipfile.ZipFile('homelessness.zip', 'r') as myzip:
    myzip.extractall()


# In[3]:


df_homeless = pd.read_csv('2007-2016-Homelessnewss-USA.csv')
df_homeless


# ## Assess

# In[4]:


df_homeless.info()


# In[5]:


df_population = pd.read_csv('Population-by-state.csv')
df_population.head()


# In[6]:


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

# In[7]:


# make copy of data set
df_homeless1 = df_homeless.copy()


# In[8]:


# drop 'CoC Number' from df_homeless
df_homeless1.drop('CoC Number', axis=1, inplace=True)


# > **Fix year column in df_homeless to fit YYYY format.**

# In[9]:


# Use only year values for the Year column.
df_homeless1['Year'] = df_homeless1['Year'].str[4:]


# > **States are abbreviated for df_homeless but are in full in df_population.**

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

# In[11]:


# drop "VI" entries in State column
df_homeless2.drop(df_homeless2[df_homeless2.State == "VI"].index, inplace=True)


# In[12]:


# drop "GU" entries in State column
df_homeless2.drop(df_homeless2[df_homeless2.State == "GU"].index, inplace=True)


# In[13]:


# find all unique entries in State column
df_homeless2.State.unique()


# In[14]:


# reset index
df_homeless2.reset_index(drop=True)


# In[15]:


# ensure that unwanted entries have been removed
df_homeless2.shape


# > **Data organized by cities/counties in `df_homeless`.**

# In[16]:


# drop CoC Name column
df_homeless2.drop('CoC Name', axis=1, inplace=True)


# In[17]:


# make copy of df_homeless2
df_homeless_measures = df_homeless2.copy()


# > **Multiple Measures for each state in `df_homeless`.**

# In[18]:


# drop Measures column
df_homeless2.drop('Measures', axis=1, inplace=True)


# > **Convert 'Count' column from str to int in `df_homeless`.**

# In[19]:


# remove commas from Count column
df_homeless2['Count'] = df_homeless2['Count'].str.replace(',', '')


# In[20]:


# convert all entries in Count column from string to integer
df_homeless2['Count'] = pd.to_numeric(df_homeless2['Count'])


# In[21]:


# sum Count by state and year
d = {'Count': 'sum'}
df_homeless3 = df_homeless2.groupby(['Year', 'State']).aggregate(d)
df_homeless3


# In[22]:


# pivot table
df_homeless4 = pd.pivot_table(df_homeless3, values='Count', index=['State'], columns=['Year'], aggfunc=np.sum)
df_homeless4


# > **Drop 2007-2009 columns in df_homeless**

# In[23]:


# drop columns due df_population data set 
df_homeless4.drop(['2007', '2008', '2009'], axis=1, inplace=True)
df_homeless4


# 
# ### `df_population`

# > **Rename columns in `df_population`.**

# In[24]:


# rename columns
df_population1 = df_population.rename(columns={'GEO.display-label': 'State', 'respop72010': '2010', 'respop72011': '2011', 'respop72012': '2012', 'respop72013': '2013', 'respop72014': '2014', 'respop72015': '2015', 'respop72016': '2016'})


# > **Delete 0 index row for `df_population`**.

# In[25]:


# drop first row [0] of df_population
df_population1.drop([0], inplace=True)


# In[26]:


# drop first 'rescen42010' from df_population
df_population1.drop('rescen42010', axis=1, inplace=True)


# In[27]:


# drop first 'resbase42010' from df_population
df_population1.drop('resbase42010', axis=1, inplace=True)


# In[28]:


# drop first 'GEO.id' from df_population
df_population1.drop('GEO.id', axis=1, inplace=True)


# In[29]:


# drop first 'GEO.id2' from df_population
df_population1.drop('GEO.id2', axis=1, inplace=True)
df_population1


# In[30]:


# Make the state column the index
df_population1.set_index("State", inplace = True)
df_population1


# In[31]:


# Convert to int
df_population2 = df_population1.apply(pd.to_numeric)


# ## Check

# In[32]:


# Check info for df_homeless
df_homeless4.info()


# In[33]:


# Check info for df_population
df_population2.info()


# In[34]:


# Calculate percentage homeless
df_percentage_homeless = df_homeless4/df_population2
df_percentage_homeless


# In[35]:


# Write object to a comma-separated values (csv) file.
df_percentage_homeless.to_csv('df_percentage_homeless.csv')


# ### `df_homeless_measures `

# In[36]:


# remove commas from Count column
df_homeless_measures['Count'] = df_homeless_measures['Count'].str.replace(',', '')


# In[37]:


# convert all entries in Count column from string to integer
df_homeless_measures['Count'] = pd.to_numeric(df_homeless_measures['Count'])


# In[38]:


# sum Count by state, year, and measures
d = {'Count': 'sum'}
df_homeless_measures1 = df_homeless_measures.groupby(['Year', 'State', 'Measures']).aggregate(d)
df_homeless_measures1


# In[39]:


# Write object to a comma-separated values (csv) file.
df_homeless_measures1.to_csv('diff_homeless_measures.csv')


# ### `df_homeless_percent`

# In[40]:


# Transpose data set
df_percentage_homeless1 = df_percentage_homeless.T
df_percentage_homeless1


# In[41]:


# Difference in percent homeless from 2010-2016
df_percentage_homeless1.loc['Diff'] = df_percentage_homeless1.loc['2016'] - df_percentage_homeless1.loc['2010']
diff_homeless_percent = df_percentage_homeless1.loc['Diff'].sort_values()
diff_homeless_percent


# In[42]:


# Convert diff_homeless_percent to data set
diff_homeless_percent_1 = diff_homeless_percent.reset_index()
diff_homeless_percent_1


# In[43]:


# Write object to a comma-separated values (csv) file.
diff_homeless_percent.to_csv('diff_homeless.csv')


# ## Visualize

# ### United States Change in Homeless Population from 2010 to 2016

# In[44]:


# Import Tableau Dashboard to Jupyter Notebooks (Change in Homelessness by State)


# In[45]:


get_ipython().run_cell_magic('HTML', '', "<div class='tableauPlaceholder' id='viz1560960628541' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Un&#47;UnitedStatesChangeinHomelessPopulation2010-2016&#47;Dashboard2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='UnitedStatesChangeinHomelessPopulation2010-2016&#47;Dashboard2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Un&#47;UnitedStatesChangeinHomelessPopulation2010-2016&#47;Dashboard2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1560960628541');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>")


# In[46]:


# Import Tableau Dashboard to Jupyter Notebooks (Change in Homelessness by State Bar Graph)


# In[47]:


get_ipython().run_cell_magic('HTML', '', "<div class='tableauPlaceholder' id='viz1560906912716' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ch&#47;ChangeinHomelessnessbyStateBarGraph&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='ChangeinHomelessnessbyStateBarGraph&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ch&#47;ChangeinHomelessnessbyStateBarGraph&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1560906912716');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>")


# In[48]:


# Convert diff_homeless_percent to data set
diff_homeless_percent_1 = diff_homeless_percent.reset_index()
diff_homeless_percent_1


# In[49]:


get_ipython().run_cell_magic('HTML', '', "<div class='tableauPlaceholder' id='viz1560913331810' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ch&#47;ChangeinHomelessPopulationHeatMap&#47;Dashboard3&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='ChangeinHomelessPopulationHeatMap&#47;Dashboard3' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ch&#47;ChangeinHomelessPopulationHeatMap&#47;Dashboard3&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1560913331810');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>")


# #### Results
# - 26 states have decreased the percentage of homeless people in their state.
# - 26 states have increased the percentage of homeless people in their state.

# #### Ranking: States that have decreased the rate of homelessness the most
# | **Ranking** | **State** | **Change** |
# | --- | --- | --- |
# | 1. | Louisiana | -0.8609% |
# | 2. | Florida | -0.4739% |
# | 3. | Nevada | -0.4161% |
# | 4. | Oregon | -0.3337% |
# | 5. | Colorado | -0.2807% |
# | 6. | Georgia | -0.2659% |
# | 7. | Arizona | -0.1966% |
# | 8. | Nebraska | -0.1948% |
# | 9. | Texas | -0.1839% |
# | 10. | Kentucky | -0.1703% |
# | 11. | Maryland | -0.1685% |
# | 12. | West Virginia | -0.1607% |
# | 13. | New Jersey | -0.1537% |
# | 14. | Alabama	| -0.1357% |
# | 15. | New Mexico | -0.1273% |
# | 16. | Virginia | -0.1185% |
# | 17. | Mississippi | -0.1119% |
# | 18. | Michigan | -0.0956% |
# | 19. | North Carolina | -0.0712% |
# | 20. | Utah | -0.0639% |
# | 21. | Ohio | -0.0383% |
# | 22. | Illinois | -0.0322% |
# | 23. | Oklahoma | -0.0309% |
# | 24. | Tennessee | -0.0291% |
# | 25. | Missouri | -0.0204% |
# | 26. | Montana	| -0.0021% |
# | 27. | Connecticut	| 0.0004% |
# | 28. | Washington | 0.0056% |
# | 29. | Wisconsin | 0.0079% |
# | 30. | Indiana	| 0.0154% |
# | 31. | New Hampshire | 0.0271% |
# | 32. | Arkansas | 0.0363% |
# | 33. | Minnesota | 0.0415% |
# | 34. | Rhode Island | 0.0455% |
# | 35. | Iowa | 0.0598% |
# | 36. | Delaware | 0.0749% |
# | 37. | Maine | 0.0787% |
# | 38. | Kansas | 0.0797% |
# | 39. |Idaho | 0.0803% |
# | 40. |Vermont | 0.1005% |
# | 41. | Pennsylvania | 0.1150% |
# | 42. | South Carolina | 0.1300% |
# | 43. | North Dakota | 0.1389% |
# | 44. | Alaska | 0.1683% |
# | 45. | Puerto Rico | 0.1945% |
# | 46. | South Dakota | 0.2088% |
# | 47. | California | 0.2129% |
# | 48. |Wyoming | 0.2686% |
# | 49. | Massachusetts | 0.3155% |
# | 50. | New York | 0.6215% |
# | 51. | Hawaii | 1.1532% |
# | 52. | District of Columbia | 1.5600% |

# ### Percent of State Population Homeless in 2016

# In[50]:


# Import Tableau Dashboard to Jupyter Notebooks (Percentage Homeless in 2016)


# In[51]:


get_ipython().run_cell_magic('HTML', '', "<div class='tableauPlaceholder' id='viz1560960701231' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Pe&#47;PercentofStatePopulationHomelessin2016&#47;Dashboard4&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='PercentofStatePopulationHomelessin2016&#47;Dashboard4' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Pe&#47;PercentofStatePopulationHomelessin2016&#47;Dashboard4&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1560960701231');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>")


# In[52]:


# Import Tableau Bar Chart to Jupyter Notebook (Percentage Homeless in 2016)


# In[53]:


get_ipython().run_cell_magic('HTML', '', "<div class='tableauPlaceholder' id='viz1560963028192' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Pe&#47;PercentofStatePopulationHomelessin2016BarChart&#47;Dashboard5&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='PercentofStatePopulationHomelessin2016BarChart&#47;Dashboard5' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Pe&#47;PercentofStatePopulationHomelessin2016BarChart&#47;Dashboard5&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1560963028192');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='1709px';vizElement.style.height='931px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>")


# In[54]:


# convert to data frame
df_2016 = df_percentage_homeless['2016'].reset_index()
df_2016


# In[55]:


# sort values
df_2016.sort_values(by=['2016']).reset_index()


# #### Results
# - No state have a homeless population of over 7% of their total population in 2016.
# - The District of Columbia had over double the rate of homelessness than any other state in this study in 2016.
# - Mississippi had the lowest rate of homelessness out of all the states in 2016.
# 
# #### Ranking
# | **Ranking** | **State** | **Percentage Homeless** |
# | --- | --- | --- |
# | 1. | Mississippi | 0.2815% |
# | 2. | Kansas | 0.3442% |
# | 3. | Virginia	| 0.3716% |
# | 4. | West Virginia | 0.3834% |
# | 5. | Alabama | 0.4133% |
# | 6. | Texas | 0.4242% |
# | 7. | Ohio	| 0.4361% |
# | 8. | Indiana | 0.4369% |
# | 9. | Utah	| 0.4387% |
# | 10. | Arkansas  | 0.4414% |
# | 11. |	Illinois | 0.4494% |
# | 12. | Louisiana | 0.4495% |
# | 13. | North Carolina | 0.4699% |
# | 14. | Michigan | 0.4702% |
# | 15. | Kentucky | 0.4708% |
# | 16. | Iowa | 0.4713% |
# | 17. | Wisconsin | 0.4786% |
# | 18. | New Jersey | 0.4904% |
# | 19. | Connecticut | 0.5261% |
# | 20. | Delaware | 0.5329% |
# | 21. | South Carolina | 0.5450% |
# | 22. | Rhode Island | 0.5486 %  |
# | 23. | New Hampshire | 0.5547% |
# | 24. | Oklahoma | 0.5584% |
# | 25. | Missouri | 0.5796% |
# | 26. | South Dakota | 0.5937% |
# | 27. | Pennsylvania | 0.5957% |
# | 28. | New Mexico | 0.6213% |
# | 29. | Georgia | 0.6257% |
# | 30. | North Dakota | 0.6317% |
# | 31. | Maryland | 0.6562% |
# | 32. | Montana | 0.6793% |
# | 33. | Minnesota | 0.6903% |
# | 34. | Idaho | 0.6918% |
# | 35. | Tennessee | 0.6960% |
# | 36. | Nebraska | 0.7111% |
# | 37. | Wyoming	| 0.7146% |
# | 38. | Arizona	| 0.7197% |
# | 39. | Puerto Rico	| 0.7597% |
# | 40. | Maine | 0.8295% |
# | 41. | Florida	| 0.8453% |
# | 42. | Vermont | 0.9225% |
# | 43. | Colorado | 1.0026% |
# | 44. | Alaska | 1.2579% |
# | 45. |	Nevada | 1.3466% | 
# | 46. | Massachusetts | 1.3908% |
# | 47. | Washington | 1.4251% |
# | 48. | California | 1.7032% |
# | 49. | Oregon | 1.8333% |
# | 50. | New York | 2.0179% |
# | 51. | Hawaii | 2.9816% |
# | 52. | District of Columbia | 6.5793% |

# ### Breakdown of Homelessness

# In[56]:


# Import Tableau Treemap to Jupyter Notebook (Breakdown of State Homelessness by Year)


# In[60]:


get_ipython().run_cell_magic('HTML', '', "<div class='tableauPlaceholder' id='viz1561320599475' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Br&#47;BreakdownofStateHomelessnessbyYear&#47;Sheet2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='BreakdownofStateHomelessnessbyYear&#47;Sheet2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Br&#47;BreakdownofStateHomelessnessbyYear&#47;Sheet2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1561320599475');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>")


# #### Results
# - Sheltered homeless and homeless individuals make up the highest portion of the homeless population nationwide on average between 2007 to 2016.
# - Youth homelessness make up the lowest portion of the homeless population nationwide on average between 2007 to 2016.

# ### Changes in Homelessness Over the Years

# In[58]:


# Import Tableau Line Graph to Jupyter Notebook (Changes in Homelessness Over the Years)


# In[59]:


get_ipython().run_cell_magic('HTML', '', "<div class='tableauPlaceholder' id='viz1561175150476' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ch&#47;ChangesinHomelessnessOvertheYears&#47;Dashboard2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='ChangesinHomelessnessOvertheYears&#47;Dashboard2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ch&#47;ChangesinHomelessnessOvertheYears&#47;Dashboard2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1561175150476');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>")


# #### Results
# - Total homelessness has decreased in the country from 2007 to 2016.
