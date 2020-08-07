#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
"""
# TODO: update docstring

Script for (1) running a screen for companies using the NTAV screen and
(2) performing basic business sanalysis.
"""

# --- Imports

# Standard library
import collections
import logging
import os
import re
import sys 
import time

# Database packages
import django

# External packages
import click
import pandas as pd
from tqdm import tqdm

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "upside.db.django_config.settings")
django.setup()

# pylint: disable=wrong-import-position

# Upside
from upside.db.data_store.models import Company  # noqa
from upside.db.data_store.models import FinancialReport  # noqa


# --- Constants

# Script name
_SCRIPT_NAME = os.path.basename("Magic Formula")
_SCREENING_TYPE = _SCRIPT_NAME.split('-')[-1]

# Error codes
RETURN_CODE_SUCCESS = 0
RETURN_CODE_INVALID_LOG_LEVEL = 1


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

    # Start timer
    start_time = time.time()


# In[ ]:


# --- Calculate screening metrics

   print("Calculating screening metrics...")

   companies = Company.objects.all()
   with tqdm(total=len(companies), unit="tickers") as progress_bar:
       for company in companies:

           # --- Preparations

           # Get ticker
           ticker = company.ticker

           # Update postfix in progress bar
           progress_bar.set_postfix(ticker=ticker, refresh=True)

           # Skip companies without financial reports or stock snapshots
           if company.financial_reports.count() == 0 or                    company.stock_snapshots.count() == 0:

               # Update progress bar and skip to next company
               progress_bar.update()
               continue

           # Get most recent financial report data and financial statements
           financial_report =                company.financial_reports.order_by('-date')[0]

           balance_sheet_data = financial_report.balance_sheet
           cash_flow_statement_data = financial_report.cash_flow_statement
           income_statement_data = financial_report.income_statement

           # Skip companies with invalid balance sheet data
           expected_stockholder_equity =                balance_sheet_data.get('total_assets', 0) -                balance_sheet_data.get('total_liab', 0)
           if balance_sheet_data.get('total_stockholder_equity', 0) !=                    expected_stockholder_equity:

               message =                    "Invalid balance sheet for {}. Skipping...".format(ticker)
               logging.warning(message)

               # Update progress bar and skip to next company
               progress_bar.update()
               continue

           # Get most recent stock snapshot
           stock_snapshot = company.stock_snapshots.order_by('-date')[0]

           # Initialize fundamentals, stock data, and metrics
           fundamentals = {}
           stock_data = {}
           metrics = {}


# In[ ]:


# TODO: update to retrieve data required for magic formula
           # Calculation 1
           
               # Needed data: Net Earnings (E), Taxes, Interest, Enterprise/Asset Value (EV), 
               
           
           # Calculation 2
               # Needed data: Net Earnings, Taxes, Interest, Depreciation + Amortization (DA)
               

# Get basic company data
           company_info = {}
           company_info['company_name'] = company.name
           company_info['currency'] = financial_report.currency
           company_info['average_shares_outstanding'] =                financial_report.avg_shares_outstanding
           fundamentals['company_info'] = company_info


# In[ ]:


# Get balance sheet data
            balance_sheet = {}
            balance_sheet['cash'] = balance_sheet_data.get('cash', 0)

            balance_sheet['total_debt'] =                 balance_sheet_data.get('short_long_term_debt', 0) +                 balance_sheet_data.get('long_term_debt', 0)

            balance_sheet['net_cash'] =                 balance_sheet['cash'] - balance_sheet['total_debt']

            balance_sheet['net_current_assets'] =                 balance_sheet_data.get('total_current_assets', 0) -                 balance_sheet_data.get('total_liabilities', 0)

            balance_sheet['stockholder_equity'] =                 balance_sheet_data.get('total_stockholder_equity', 0)

            balance_sheet['NTAV'] =                 balance_sheet_data.get('net_tangible_assets', 0)

            fundamentals['balance_sheet'] = balance_sheet


# In[ ]:


# Get cash flow statement data
           cash_flow_statement = {}
           cash_flow_statement[
               'total_cash_from_operating_activities'] = \
               cash_flow_statement_data.get(
                   'total_cash_from_operating_activities', 0)

           cash_flow_statement['capital_expenditures'] =                cash_flow_statement_data.get('capital_expenditures', 0)

           fundamentals['cash_flow_statement'] = cash_flow_statement


# In[ ]:


# Get income statement data
            income_statement = {}
            income_statement['EBIT'] = income_statement_data.get('ebit', 0)

            fundamentals['income_statement'] = income_statement


# In[ ]:


# Get market data
            stock_data['market_capitalization'] =                 stock_snapshot.market_capitalization

            stock_data['average_volume'] = stock_snapshot.avg_volume


# In[ ]:


# --- Compute screening metrics

            # TODO: update to compute desired metrics and perform desired
            # business analysis
        
        
        

            # NTAV
            metrics['NTAV'] = balance_sheet['NTAV']

            # Free cash flow
            metrics['free_cash_flow'] =                 cash_flow_statement['total_cash_from_operating_activities']                 - cash_flow_statement['capital_expenditures']

            # Compute price-to-EBIT ratio
            if income_statement['EBIT'] > 0:
                metrics['P/EBIT'] = stock_data['market_capitalization'] /                                     income_statement['EBIT']
            else:
                metrics['P/EBIT'] = None

            # Compute price-to-book ratio
            if balance_sheet['stockholder_equity'] > 0:
                metrics['P/B'] = stock_data['market_capitalization'] /                                  balance_sheet['stockholder_equity']
            else:
                metrics['P/B'] = None

            # Compute debt-to-equity ratio
            if balance_sheet['stockholder_equity'] > 0:
                metrics['Debt/Equity'] =                     balance_sheet['total_debt'] /                     balance_sheet['stockholder_equity']
            else:
                metrics['Debt/Equity'] = None

            # Save results
            tickers_with_data.append(ticker)
            fundamental_data[ticker] = fundamentals
            market_data[ticker] = stock_data
            screening_metrics[ticker] = metrics

            # --- Update progress bar

            progress_bar.update()


# In[ ]:


# --- Perform NTAV screen for companies in the database

   # Screening parameters
   #
   # TODO: update comments to reflect magic formula screening metrics
   #
   # * NTAV > market capitalization
   # * market capitalization > US$100M
   # * average volume > 100,000
   # * price-to-EBIT > 1
   # * price-to-book < 1
   # * debt-to-equity < 0.3

   min_market_capitalization = 100e6
   min_average_volume = 100000
   min_price_to_EBIT = 1
   max_price_to_book = 1
   max_debt_to_equity = 0.3

   print("Performing NTAV screen...")

   candidates_unsorted = []
   with tqdm(total=len(tickers_with_data), unit="tickers") as progress_bar:
       for ticker in tickers_with_data:
           # --- Preparations

           # Extract data for current ticker
           fundamentals = fundamental_data[ticker]
           stock_data = market_data[ticker]
           metrics = screening_metrics[ticker]
           market_capitalization = stock_data['market_capitalization']

           # --- Skip companies to that do not meet screening criteria

           # TODO: update to use magic formula screening criteria

           # NTAV > market capitalization
           if metrics['NTAV'] < market_capitalization:
               # Update progress bar and skip to next company
               progress_bar.update()
               continue

           # market capitalization > US$100M 
               #remember to use enterprise value when calculating earnings yield, not market cap
           if fundamentals['company_info']['currency'] == 'USD'                    and market_capitalization < min_market_capitalization:
               # Update progress bar and skip to next company
               progress_bar.update()
               continue

           # average volume
           if stock_data['average_volume'] < min_average_volume:
               # Update progress bar and skip to next company
               progress_bar.update()
               continue

           # price-to-EBIT > 1
           P_to_EBIT = metrics['P/EBIT']
           if P_to_EBIT is None or P_to_EBIT < min_price_to_EBIT:
               # Update progress bar and skip to next company
               progress_bar.update()
               continue

           # price-to-book < 1
           P_to_B = metrics['P/B']
           if P_to_B is None or P_to_B > max_price_to_book:
               # Update progress bar and skip to next company
               progress_bar.update()
               continue

           # debt-to-equity < 0.3
           D_to_E = metrics['Debt/Equity']
           if D_to_E is None or D_to_E > max_debt_to_equity:
               # Update progress bar and skip to next company
               progress_bar.update()
               continue

           # --- Save data for candidates

           candidates_unsorted.append(
               (ticker, metrics['NTAV']/market_capitalization,
                metrics['free_cash_flow']))

           # --- Update progress bar

           progress_bar.update()
           


# In[ ]:


# TODO: update sort to return companies in desired order
   # Sort candidates by (NTAV - market_capitalization)
   candidates = [item[0] for item
                 in sorted(candidates_unsorted, key=lambda x: (x[1], x[2]),
                           reverse=True)
                 ]


# In[ ]:


# --- Perform business analysis

    print("Performing business analysis...")

    with tqdm(total=len(candidates), unit="tickers") as progress_bar:
        for ticker in candidates:

            # --- Preparations

            # Extract data for current ticker
            fundamentals = fundamental_data[ticker]
            balance_sheet = fundamentals['balance_sheet']
            cash_flow_statement = fundamentals['cash_flow_statement']
            stock_data = market_data[ticker]
            metrics = screening_metrics[ticker]

            # Initialize business analysis results for current ticker
            business_analysis = {}

            # --- Business analysis

            # TODO: update to perform desired business analysis

            # Enterprise value
            business_analysis['enterprise_value'] =                 stock_data['market_capitalization']                 - balance_sheet['cash'] + balance_sheet['total_debt']

            # Free cash flow
            business_analysis['free_cash_flow'] =                 cash_flow_statement['total_cash_from_operating_activities']                 - cash_flow_statement['capital_expenditures']

            # Tangible assets
            business_analysis['NTAV'] = balance_sheet['NTAV']

            # Financial strength
            business_analysis['cash'] = balance_sheet['cash']
            business_analysis['debt'] = balance_sheet['total_debt']

            # --- Save business results

            business_analysis_data[ticker] = business_analysis

            # --- Update progress bar

            progress_bar.update()


# In[ ]:


# --- Write screening results to file

    print("Writing screening results to file...")

    # TODO: update data fields/columns to write to file
    columns = ['ticker', 'company_name',
               'NTAV/market_cap',
               'free_cash_flow', 'enterprise_value',
               'market_capitalization', 'NTAV',
               'cash', 'debt',
               ]
    screening_results_df = pd.DataFrame(columns=columns)

    with tqdm(total=len(candidates), unit="tickers") as progress_bar:
        for ticker in candidates:
            # --- Preparations

            fundamentals = fundamental_data[ticker]
            stock_data = market_data[ticker]
            business_analysis = business_analysis_data[ticker]

            # --- Append row to DataFrame

            # TODO: update data to write to file
            ntav_to_market_cap =                 business_analysis['NTAV'] / stock_data['market_capitalization']
            row = {
                'ticker': ticker,
                'company_name': fundamentals['company_info']['company_name'],
                'NTAV/market_cap': ntav_to_market_cap,
                'market_capitalization': stock_data['market_capitalization'],
                **business_analysis,
                }
            screening_results_df = screening_results_df.append(
                row, ignore_index=True)

            # --- Update progress bar

            progress_bar.update()

    # Write results to file
    outfile = '{}-screening-results.csv'.format(_SCREENING_TYPE)
    screening_results_df.to_csv(outfile, index=False)

    # --- Print results

    # Stop timer
    stop_time = time.time()

    print('Number of Screening Results', len(screening_results_df.index))

    print('Running Time: {:1g}s'.format(stop_time - start_time))


if __name__ == '__main__':
    main()

