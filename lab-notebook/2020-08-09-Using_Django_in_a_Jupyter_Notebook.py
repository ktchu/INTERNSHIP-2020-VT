#!/usr/bin/env python
# coding: utf-8

# ## 2020-08-09: Using Django in a Jupyter Notebook
# 
# *Last Updated*: 2020-08-09
# 
# ### Authors
# * Kevin Chu (kevin@velexi.com)
# 
# ### Overview
# This Jupyter notebook provides demonstrate how to use Django within a Jupyter notebook.
# 
# ### Instructions
# 
# * __Configure Jupyter notebook to use the "Django Shell-Plus" kernel__
# 
#     * The currently active kernel is displayed in the upper right hand corner of the Jupyter
#       noteook.
# 
#     * To change the kernel, navigate to Kernel > "Change kernel" from the main navigation bar.
#       Select "Django Shell-Plus". If "Django Shell-Plus" is not available as an option, the
#       environment variables the shell probably need to be modified.
# 
# * __Initialize Django before accessing Django models__
# 
#     * There are two ways to initialize Django.
#         
#         * Start Jupyter notebook using an alternate shell command that automatically
#           initializes Django.
#         
#           ```
#           $ python $LIB_DIR/upside/manage.py shell_plus --notebook
#           ```
#            
#           As a convenience, add an alias to the `.env` file.
#            
#           ```
#           alias jndjango='python $LIB_DIR/lib/upside/manage.py shell_plus --notebook'
#           ```
#         
#         * Manually initialize Django in Python code before importing Django data models.
#         
#           ```python
#           os.environ.setdefault("DJANGO_SETTINGS_MODULE",
#                                 "upside.db.django_config.settings")
#           django.setup()
#           ```
#     
# * __Allow Django to operate in an asynchronize environment (such as Jupyter notebook)__
# 
#     * Set the environment variable `DJANGO_ALLOW_ASYNC_UNSAFE` to "true" before using Django
#       queries to access data.
# 
#         ```
#         os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
#         ```
#     
#     * _Reference_. https://docs.djangoproject.com/en/3.0/topics/async/

# In[1]:


# --- Imports

# Standard library
import logging
import os

# Configure Django
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "upside.db.django_config.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

# Upside
from upside.db.data_store.models import Company  # noqa


# In[2]:


# --- Preparations

# Initialize data records
tickers_with_data = []
fundamental_data = {
    'company_info': {},
    'balance_sheet': {},
    'cash_flow_statement': {},
    'income_statement': {},
    }
fundamental_data = {}
market_data = {}
screening_metrics = {}

# Initialize results records
candidates = []
business_analysis_data = {}


# In[3]:


# --- Perform Django queries to access data

# Retrieve all Company records from database
companies = Company.objects.all()

print("Number of companies: {}".format(len(companies)))
print("First 5 companies")
for company in companies[0:5]:
    print("   {}".format(company))

