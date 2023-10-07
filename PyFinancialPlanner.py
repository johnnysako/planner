
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.plan import Plan
from src.rmd import Rmd
from src.tax import Tax
from src.expenses import Expenses
from src.expense import Expense
from src.account import Account
from src.owner import Owner
from src.draw_table import plot_data_table
from src.plot_monte_carlos import plot_monte_carlos

import json
import numpy as np
import pandas as pd
import datetime

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, StrMethodFormatter
from matplotlib.backends.backend_pdf import PdfPages
import asyncio
import time

years_to_process = 64
start_year = 2023
iterations = 1000
iterations_per_thread = int(iterations/10)

# Adjust rate of return assumption here. Currently not adjusted for inflation
mean_rate_of_return = 4.19
standard_deviation_of_return = 9.5

def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

    return wrapped

def load_constants():
    f = open('rmd.json')
    rmd = Rmd(json.load(f)["rmd"])

    f = open('tax.json')
    tax = Tax(json.load(f)["tax"])

    f = open('owners.json')
    owners = []
    for o in json.load(f)["owners"]:
        owners.append(Owner(o))

    f = open('expenses.json')
    expense = []
    for e in json.load(f)['expenses']:
        expense.append(Expense(e))
    expenses = Expenses(expense)

    return rmd, tax, owners, expenses

def sort_failed(failed_plans):
    return sorted(failed_plans, key=lambda x: x['Year'].where(x['Sum of Accounts'] == 0).min(), reverse=True)

def sort_data(data_for_analysis):
    failed_plans = []
    remove_index = -1

    sorted_data = sorted(data_for_analysis, key=lambda x: x.iloc[-1]['Sum of Accounts'], reverse=True)

    for i, data in enumerate(sorted_data):
        if data.iloc[-1]['Sum of Accounts']==0:
            failed_plans.append(data)
            if remove_index == -1:
                remove_index = i

    del sorted_data[remove_index:]
    failed_plans = sort_failed(failed_plans)

    for data in failed_plans:
        sorted_data.append(data)

    return sorted_data, failed_plans

def plot_expense_table(expenses, pdf):
    expense_table = []
    for year in range(start_year,start_year+years_to_process):
        expense_table.append([year] + expenses.get_year(year))
    data = pd.DataFrame(expense_table, columns = ['Year'] + expenses.get_names())

    data.plot.bar(x='Year', stacked=True, figsize=(10,6))
    plt.xlabel('Year', fontsize=10)
    plt.xticks(fontsize=6)
    plt.ylabel('Expenses', fontsize=10)
    plt.yticks(fontsize=10)
    plt.title('Expenses over Time')
    plt.legend(prop={'size': 6})
    pdf.savefig()
    plt.close()

    labels = data['Year'].values.astype(int)
    data.drop('Year', axis=1, inplace=True)
    data.update(data.astype(float))
    data.update(data.applymap('{:,.0f}'.format))
    plot_data_table(data, pdf, labels, "Expense Table", numpages=(2,2))

def plot_accounts_table(pdf):
    f = open('accounts.json')
    accounts = []
    for a in json.load(f)["accounts"]:
        accounts.append(Account(a))

    account_table = []
    total = 0
    for account in accounts:
        total = total + account.get_balance()
        account_table.append([account.get_name(), account.get_balance(), account.get_type(), account.get_owner()])
    account_table.append(['Total', total, ''])
    data = pd.DataFrame(account_table, columns = ['Account', 'Balance', 'Type', 'Owner'])

    labels = data['Account']
    data.drop('Account', axis=1, inplace=True)
    plot_data_table(data, pdf, labels, "Account Summary")

@background
def process_run(iteration, rmd, tax, owners, expenses, trial, data_for_analysis):
    rates = np.random.normal(mean_rate_of_return, standard_deviation_of_return, years_to_process+1)
    f = open('accounts.json')
    accounts = []
    for a in json.load(f)["accounts"]:
        accounts.append(Account(a))

    plan = Plan(owners, accounts, expenses, rmd, tax, trial)

    data = pd.DataFrame(np.array(plan.process_plan(start_year, years_to_process, rates)), columns = plan.get_header())
    data_for_analysis.append(data)

def run_monte_carlos(data_for_analysis, rmd, tax, owners, expenses, trial):
    loop = asyncio.get_event_loop()                                              

    group1 = asyncio.gather(*[process_run(i, rmd, tax, owners, expenses, trial, data_for_analysis) for i in range(iterations_per_thread)])
    group2 = asyncio.gather(*[process_run(i, rmd, tax, owners, expenses, trial, data_for_analysis) for i in range(iterations_per_thread)])
    group3 = asyncio.gather(*[process_run(i, rmd, tax, owners, expenses, trial, data_for_analysis) for i in range(iterations_per_thread)])
    group4 = asyncio.gather(*[process_run(i, rmd, tax, owners, expenses, trial, data_for_analysis) for i in range(iterations_per_thread)])
    group5 = asyncio.gather(*[process_run(i, rmd, tax, owners, expenses, trial, data_for_analysis) for i in range(iterations_per_thread)])
    group6 = asyncio.gather(*[process_run(i, rmd, tax, owners, expenses, trial, data_for_analysis) for i in range(iterations_per_thread)])
    group7 = asyncio.gather(*[process_run(i, rmd, tax, owners, expenses, trial, data_for_analysis) for i in range(iterations_per_thread)])
    group8 = asyncio.gather(*[process_run(i, rmd, tax, owners, expenses, trial, data_for_analysis) for i in range(iterations_per_thread)])
    group9 = asyncio.gather(*[process_run(i, rmd, tax, owners, expenses, trial, data_for_analysis) for i in range(iterations_per_thread)])
    group10 = asyncio.gather(*[process_run(i, rmd, tax, owners, expenses, trial, data_for_analysis) for i in range(iterations_per_thread)])

    all_groups = asyncio.gather(group1, group2, group3, group4, group5, group6, group7, group8, group9, group10)                                
    results = loop.run_until_complete(all_groups)

def main():
    # Scenerios:
    # 1. As is
    # 2. Trial selected Roth with RMDs (aka 401K)
    # 3. No Social Security
    # 4. No Social Security and Trial selected Roth with RMDs
    trials = [
        { "social_security": True, "rmd": False },
        { "social_security": True, "rmd": True },
        { "social_security": False, "rmd": False },
        { "social_security": False, "rmd": True }
    ]

    rmd, tax, owners, expenses = load_constants()

    with PdfPages('financial_analysis.pdf') as pdf:
        plot_accounts_table(pdf)
        
        for trial in trials:
            data_for_analysis = []

            run_monte_carlos(data_for_analysis, rmd, tax, owners, expenses, trial)

            sorted_data, failed_plans = sort_data(data_for_analysis)

            plot_monte_carlos(sorted_data, failed_plans, pdf, owners, trial)

        plot_expense_table(expenses, pdf)

        d = pdf.infodict()
        d['Title'] = 'Financial Projection'
        d['Author'] = u'John Chapman'
        d['CreationDate'] = datetime.datetime.today()

    return 0

if __name__ == "__main__":
    main()