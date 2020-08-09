#!/usr/bin/env python
# coding: utf-8

# ## 2020-08-09: Using Progress Bars in Jupyter Notebooks
# 
# *Last Updated*: 2020-08-09
# 
# ### Authors
# * Kevin Chu (kevin@velexi.com)
# 
# ### Overview
# This Jupyter notebook demonstrates how to use progress bars in Jupyter notebook.

# In[1]:


# -- Imports

# Standard library
import time

# External packages
import tqdm.notebook


# In[2]:


# --- Loop over a range

with tqdm.notebook.trange(1, 100) as progress_bar:
    for i in progress_bar:
        progress_bar.set_description("Processing i={}".format(i))
        time.sleep(0.1)
        
# --- Loop over a list of items

items = ['a', 'b', 'c', 'd', 'e']*10
for item in tqdm.notebook.tqdm(items, unit='items', desc="Looping over 'items'"):
    time.sleep(0.5)

