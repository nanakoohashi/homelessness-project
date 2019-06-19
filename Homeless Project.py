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
# - Year in homeless dataframe should be a column not a row.
# - Change 'Geography' to 'State' for df_population.
# - Rename columns for df_population for better clarity.
# - Delete 0 index row for df_population.
# - Merge data frames.

# ## Clean
# ### df_homeless

# - make copy of data set


# In[]:


df_homeless1 = df_homeless.copy()



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

# drop "VI" entries from State column
df_homeless2.drop(df_homeless2[df_homeless2.State == "VI"].index, inplace=True)


# In[33]:

# drop "GU" entries in State column
df_homeless2.drop(df_homeless2[df_homeless2.State == "GU"].index, inplace=True)


# In[34]:

# find all unique entries in State column
df_homeless2.State.unique()


# In[35]:

# reset index
df_homeless2.reset_index(drop=True)


# In[41]:

# ensure that unwanted entries have been removed
df_homeless2.shape


# In[42]:

# drop CoC Name column
df_homeless2.drop('CoC Name', axis=1, inplace=True)


# In[44]:

# drop Measures column
df_homeless2.drop('Measures', axis=1, inplace=True)


# In[49]:

# remove commas from Count column
df_homeless2['Count'] = df_homeless2['Count'].str.replace(',', '')


# In[50]:

# convert all entries in Count column from string to integer
df_homeless2['Count'] = pd.to_numeric(df_homeless2['Count'])


# In[51]:

# sum Count by state and year
d = {'Count': 'sum'}
df_homeless3 = df_homeless2.groupby(['Year', 'State']).aggregate(d)
df_homeless3


# In[52]:

# pivot table
df_homeless4 = pd.pivot_table(df_homeless3, values='Count', index=['State'], columns=['Year'], aggfunc=np.sum)
df_homeless4


# In[53]:

# drop columns due df_population data set 
df_homeless4.drop(['2007', '2008', '2009'], axis=1, inplace=True)
df_homeless4

# ### df_population

# #### Define

# In[ ]:

# rename columns
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


# Make the state column the index
df_population1.set_index("State", inplace = True)
df_population1


# In[ ]:


#Convert to int
df_population2 = df_population1.apply(pd.to_numeric)


# In[ ]:

# Check info for df_homeless
df_homeless4.info()


# In[ ]:

# Check info for df_population
df_population2.info()


# In[ ]:

#calculate percentage homeless by state and year
df_percentage_homeless = df_homeless4/df_population2
df_percentage_homeless


# #### Visualize

# In[ ]:

# Transpose df_percentage_homeless
df_percentage_homeless = df_percentage_homeless.T
df_percentage_homeless


# In[ ]:

#Difference in percentage homeless from 2010 to 2016
df_combined.loc['Diff'] = df_combined.loc['2016'] - df_combined.loc['2010']
df_combined.loc['Diff'].sort_values()


# In[ ]:

# Write object to a comma-separated values (csv) file.
diff_homeless_percent.to_csv('diff_homeless.csv')


# ### United States Change in Homeless Population from 2010 to 2016


# In[ ]:

# convert to data set
df_percentage_homeless.loc['Diff'] = df_percentage_homeless.loc['2016'] - df_percentage_homeless.loc['2010']
diff_homeless_percent = df_percentage_homeless.loc['Diff'].sort_values()
diff_homeless_percent


# In[ ]:

#Import Tableau Dashboard to Jupyter Notebooks (Change in Homelessness from 2010-2016)
%%HTML 
<div class='tableauPlaceholder' id='viz1560913259034' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Un&#47;UnitedStatesChangeinHomelessPopulation2010-2016&#47;Dashboard2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='UnitedStatesChangeinHomelessPopulation2010-2016&#47;Dashboard2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Un&#47;UnitedStatesChangeinHomelessPopulation2010-2016&#47;Dashboard2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1560913259034');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>

# In[ ]:

# Import Tableau Dashboard to Jupyter Notebooks (Change in Homelessness by State Bar Graph)
%%HTML
<div class='tableauPlaceholder' id='viz1560906912716' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ch&#47;ChangeinHomelessnessbyStateBarGraph&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='ChangeinHomelessnessbyStateBarGraph&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ch&#47;ChangeinHomelessnessbyStateBarGraph&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1560906912716');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>


# In[ ]:

# Import Tableau Heatmap Table to Jupyter Notebook
%%HTML
<div class='tableauPlaceholder' id='viz1560913331810' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ch&#47;ChangeinHomelessPopulationHeatMap&#47;Dashboard3&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='ChangeinHomelessPopulationHeatMap&#47;Dashboard3' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ch&#47;ChangeinHomelessPopulationHeatMap&#47;Dashboard3&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1560913331810');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>


# #### Results
- 26 states have decreased the percentage of homeless people in their state.
- 26 states have increased the percentage of homeless people in their state.


# #### Ranking: States that have decreased the rate of homelessness the most
1. Louisiana -0.8609%
2. Florida -0.4739%
3. Nevada -0.4161%
4. Oregon -0.3337%
5. Colorado -0.2807%
6. Georgia -0.2659%
7. Arizona -0.1966%
8. Nebraska -0.1948%
9. Texas -0.1839%
10.	Kentucky -0.1703%
11.	Maryland -0.1685%
12.	West Virginia -0.1607%
13.	New Jersey -0.1537%
14.	Alabama	-0.1357%
15.	New Mexico -0.1273%
16.	Virginia -0.1185%
17.	Mississippi -0.1119%
18.	Michigan -0.0956%
19.	North Carolina -0.0712%
20.	Utah -0.0639%
21.	Ohio -0.0383%
22.	Illinois -0.0322%
23.	Oklahoma -0.0309%
24.	Tennessee -0.0291%
25.	Missouri -0.0204%
26.	Montana	-0.0021%
27.	Connecticut	0.0004%
28.	Washington 0.0056%
29.	Wisconsin 0.0079%
30.	Indiana	0.0154%
31.	New Hampshire 0.0271%
32.	Arkansas 0.0363%
33.	Minnesota 0.0415%
34.	Rhode Island 0.0455%
35.	Iowa 0.0598%
36.	Delaware 0.0749%
37.	Maine 0.0787%
38.	Kansas 0.0797%
39.	Idaho 0.0803%
40.	Vermont	0.1005%
41.	Pennsylvania 0.1150%
42.	South Carolina 0.1300%
43.	North Dakota 0.1389%
44.	Alaska 0.1683%
45.	Puerto Rico	0.1945%
46.	South Dakota 0.2088%
47.	California 0.2129%
48.	Wyoming	0.2686%
49.	Massachusetts 0.3155%
50.	New York 0.6215%
51.	Hawaii 1.1532%
52.	District of Columbia 1.5600%


# ### United States Homeless Population (as a Percent of Total Population) in 2010
# In[ ]:

#Import Tableau Dashboard to Jupyter Notebooks (Percentage Homeless in 2010)
%%HTML
<div class='tableauPlaceholder' id='viz1553101647917' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;US&#47;USHomelessPopulationasapercentofTotalStatePopulationin2010&#47;Dashboard2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='USHomelessPopulationasapercentofTotalStatePopulationin2010&#47;Dashboard2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;US&#47;USHomelessPopulationasapercentofTotalStatePopulationin2010&#47;Dashboard2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1553101647917');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.minWidth='420px';vizElement.style.maxWidth='1750px';vizElement.style.width='100%';vizElement.style.minHeight='1000px';vizElement.style.maxHeight='887px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>


# ### United States Homeless Population (as a Percent of Total Population) in 2011
# In[ ]:

#Import Tableau Dashboard to Jupyter Notebooks (Percentage Homeless in 2011)
%%HTML
<div class='tableauPlaceholder' id='viz1553108605725' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;US&#47;USHomelessPopulationasapercentofTotalStatePopulationin2011&#47;Dashboard3&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='USHomelessPopulationasapercentofTotalStatePopulationin2011&#47;Dashboard3' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;US&#47;USHomelessPopulationasapercentofTotalStatePopulationin2011&#47;Dashboard3&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1553108605725');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.minWidth='420px';vizElement.style.maxWidth='1750px';vizElement.style.width='100%';vizElement.style.minHeight='587px';vizElement.style.maxHeight='887px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>


### United States Homeless Population (as a Percent of Total Population) in 2012
# In[ ]:

#Import Tableau Dashboard to Jupyter Notebooks (Percentage Homeless in 2012)
%%HTML
<div class='tableauPlaceholder' id='viz1553185794246' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;US&#47;USHomelessPopulationasapercentofTotalStatePopulationin2012&#47;Dashboard4&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='USHomelessPopulationasapercentofTotalStatePopulationin2012&#47;Dashboard4' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;US&#47;USHomelessPopulationasapercentofTotalStatePopulationin2012&#47;Dashboard4&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1553185794246');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.minWidth='420px';vizElement.style.maxWidth='1650px';vizElement.style.width='100%';vizElement.style.minHeight='587px';vizElement.style.maxHeight='887px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>


# In[ ]:

#Import Tableau Dashboard to Jupyter Notebooks (Percentage Homeless in 2013)
%%HTML
<div class='tableauPlaceholder' id='viz1553186776446' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;US&#47;USHomelessPopulationasapercentofTotalStatePopulationin2013&#47;Dashboard5&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='USHomelessPopulationasapercentofTotalStatePopulationin2013&#47;Dashboard5' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;US&#47;USHomelessPopulationasapercentofTotalStatePopulationin2013&#47;Dashboard5&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1553186776446');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.minWidth='420px';vizElement.style.maxWidth='1750px';vizElement.style.width='100%';vizElement.style.minHeight='587px';vizElement.style.maxHeight='887px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>


# In[ ]:

#Import Tableau Dashboard to Jupyter Notebooks (Percentage Homeless in 2014)
%%HTML
<div class='tableauPlaceholder' id='viz1553187116093' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;US&#47;USHomelessPopulationasapercentofTotalStatePopulationin2014&#47;Dashboard6&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='USHomelessPopulationasapercentofTotalStatePopulationin2014&#47;Dashboard6' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;US&#47;USHomelessPopulationasapercentofTotalStatePopulationin2014&#47;Dashboard6&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1553187116093');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.minWidth='420px';vizElement.style.maxWidth='1750px';vizElement.style.width='100%';vizElement.style.minHeight='587px';vizElement.style.maxHeight='887px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>


# In[ ]:

#Import Tableau Dashboard to Jupyter Notebooks (Percentage Homeless in 2015)
%%HTML
<div class='tableauPlaceholder' id='viz1553188264397' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;US&#47;USHomelessPopulationasapercentofTotalStatePopulationin2015&#47;Dashboard7&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='USHomelessPopulationasapercentofTotalStatePopulationin2015&#47;Dashboard7' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;US&#47;USHomelessPopulationasapercentofTotalStatePopulationin2015&#47;Dashboard7&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1553188264397');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.minWidth='420px';vizElement.style.maxWidth='1750px';vizElement.style.width='100%';vizElement.style.minHeight='587px';vizElement.style.maxHeight='887px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>


# In[ ]:

#Import Tableau Dashboard to Jupyter Notebooks (Percentage Homeless in 2016)
%%HTML
<div class='tableauPlaceholder' id='viz1560960701231' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Pe&#47;PercentofStatePopulationHomelessin2016&#47;Dashboard4&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='PercentofStatePopulationHomelessin2016&#47;Dashboard4' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Pe&#47;PercentofStatePopulationHomelessin2016&#47;Dashboard4&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1560960701231');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
