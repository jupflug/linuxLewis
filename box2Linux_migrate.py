#!/usr/bin/env python
# coding: utf-8

# In[2]:


from boxMigrate import boxMigrate

from pyproj import Proj
from pandas import DataFrame
import numpy as np

id = '4stt8wd7hn5c19obxhh2kpnf7419pni6'
secret = 'UfS1HnLjbgGeQuh4dtIXBJRT2kVdQC4M'
token = 'QrJrO9Z5hg7DtrAjKrHITQTiCawR97Kn'

target_dir = 'Rocky_Pflug'

subdirs = ['N40_0W106_0_agg_16','WY2020']

out_path = '/scratch/summit/jupf7869/500m/'

keys = ['Ta_Post','PPT_Post','SWE_Post','SCA_Post']

xMin = 410000; xMax = 463500
yMin = 4414000; yMax = 4495000


# In[3]:


x = [xMin, xMax, xMax, xMin]
y = [yMin, yMin, yMax, yMax]
df = DataFrame(np.c_[x,y],columns = ['Meters East','Meters South'])
project = Proj("+proj=utm +zone=13N")

lon, lat = project(df['Meters East'].values, df['Meters South'].values,
                  inverse=True)


# In[4]:


client, root_directory = boxMigrate.target_directory(id,secret,token,target_dir)
print(root_directory)


# In[9]:


yrRange = range(1985,2021)
for year in yrRange:
    subdirs = ['N40_0W106_0_agg_16','WY'+str(year)]
#     print(subdirs)
    boxMigrate.download_data(root_directory,subdirs,client,out_path,
                         filter='latlon',lon = lon,lat = lat,keys = keys)

