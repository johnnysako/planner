
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.plan import Plan
from src.rmd import Rmd
from src.tax import Tax
from src.expenses import Expenses
from src.expense import Expense
from src.account import Account
from src.owner import Owner

import json
import csv
import numpy as np
import pandas as pd
import datetime

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, StrMethodFormatter
from matplotlib.backends.backend_pdf import PdfPages
import asyncio
import time

years_to_process = 64
iterations = 1020
iterations_per_thread = int(iterations/10)
remove = 10
actual_iterations = int(iterations-remove*2)
mean_rate_of_return = 3.5
standard_deviation_of_return = 7
include_tables = False

def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

    return wrapped

def your_function(argument, other_argument): # Added another argument
    time.sleep(5)
    print(f"function finished for {argument=} and {other_argument=}")
    
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

def sort_data(data_for_analysis):
    sorted_data = sorted(data_for_analysis, key=lambda x: x.iloc[-1]['Sum of Accounts'], reverse=True)
    return sorted_data[remove:-remove]

def _draw_as_table(df, pagesize, rowlabels):
    alternating_colors = [['white'] * len(df.columns), ['lightgray'] * len(df.columns)] * len(df)
    alternating_colors = alternating_colors[:len(df)]
    fig, ax = plt.subplots(figsize=pagesize)
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df.values,
                        colLabels=df.columns,
                        rowLabels=rowlabels,
                        rowColours=['lightblue']*len(df),
                        colColours=['lightblue']*len(df.columns),
                        cellColours=alternating_colors,
                        cellLoc='center',
                        loc='center')
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(6)
    return fig
 
def plot_data_table(data, pdf, rowlabels, numpages=(1, 1), pagesize=(11, 8.5)):
    nh, nv = numpages
    rows_per_page = len(data) // nh
    cols_per_page = len(data.columns) // nv
    for i in range(0, nh):
        for j in range(0, nv):
            pagelabels = rowlabels[(i*rows_per_page):min((i+1)*rows_per_page, len(rowlabels))]
            page = data.iloc[(i*rows_per_page):min((i+1)*rows_per_page, len(data)),
                           (j*cols_per_page):min((j+1)*cols_per_page, len(data.columns))]
            fig = _draw_as_table(page, pagesize, pagelabels)
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()

def plot_failed_plans(failed_plans, pdf):
    for index, data in enumerate(failed_plans):
        fails_in_year = data['Year'].where(data['Sum of Accounts'] == 0).min()
        data.set_index('Year').plot.line(figsize=(10,6), fontsize=12)
        ax = plt.gca()
        plt.ticklabel_format(useOffset=False, style='plain')
        ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
        plt.title('Failed Iteration ' + str(index+1) + ' in year ' + str(fails_in_year))
        pdf.savefig()
        plt.close()

        if include_tables: 
            labels = data['Year'].values.astype(int)
            data.drop('Year', axis=1, inplace=True)
            data.update(data.astype(float))
            data.update(data.applymap('{:,.0f}'.format))
            plot_data_table(data, pdf, labels, numpages=(2,1))

def plot_monte_carlos_summary(data_for_analysis, pdf):
    data = []
    range = [int(actual_iterations/100), int(actual_iterations/4), int(actual_iterations/2), int(actual_iterations*3/4), int(actual_iterations*99/100)]
    for i in range:
        data.append([i, 
                     data_for_analysis[i]['Sum of Accounts'][5], 
                     data_for_analysis[i]['Sum of Accounts'][10], 
                     data_for_analysis[i]['Sum of Accounts'][15], 
                     data_for_analysis[i]['Sum of Accounts'][20], 
                     data_for_analysis[i]['Sum of Accounts'][25], 
                     data_for_analysis[i]['Sum of Accounts'][years_to_process]])

    summary = pd.DataFrame(np.array(data), columns=['Trial', 'Year 5', 'Year 10', 'Year 15', 'Year 20', 'Year 25', 'End of Plan'])
    labels = summary['Trial'].values.astype(int)
    summary.drop('Trial', axis=1, inplace=True)
    summary.update(summary.astype(float))
    summary.update(summary.applymap('{:,.0f}'.format))
    plot_data_table(summary, pdf, labels)

def plot_monte_carlos(data_for_analysis, failed_plans, pdf):
    fig = plt.figure(figsize=(10,6), dpi=300)
    for data in data_for_analysis:
        plt.plot(data['Year'], data['Sum of Accounts'])
        if data.iloc[-1]['Sum of Accounts']==0:
            failed_plans.append(data)
    
    ax = plt.gca()
    plt.ticklabel_format(useOffset=False, style='plain')
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    plt.xlabel('Year', fontsize=12)
    plt.xticks(fontsize=12)
    plt.ylabel('Net Worth', fontsize=12)
    plt.yticks(fontsize=12)
    plt.title('Monte Carlo Analysis')
    pdf.savefig()
    plt.close(fig)

    return failed_plans

def plot_results(data_for_analysis):
    with PdfPages('financial_analysis.pdf') as pdf:
        failed_plans = []
        plot_monte_carlos(data_for_analysis, failed_plans, pdf)
        plot_monte_carlos_summary(data_for_analysis, pdf)
        plot_failed_plans(failed_plans, pdf)

        d = pdf.infodict()
        d['Title'] = 'Financial Plan'
        d['Author'] = u'John Chapman'
        d['CreationDate'] = datetime.datetime.today()

@background
def process_run(iteration, rmd, tax, owners, expenses, data_for_analysis):
    rates = np.random.normal(mean_rate_of_return, standard_deviation_of_return, years_to_process+1)
    f = open('accounts.json')
    accounts = []
    for a in json.load(f)["accounts"]:
        accounts.append(Account(a))

    plan = Plan(owners, accounts, expenses, rmd, tax)

    data = pd.DataFrame(np.array(plan.process_plan(2023, years_to_process, rates)), columns = plan.get_header())
    data_for_analysis.append(data)

def main():
    rmd, tax, owners, expenses = load_constants()

    data_for_analysis = []

    loop = asyncio.get_event_loop()                                              

    group1 = asyncio.gather(*[process_run(i, rmd, tax, owners, expenses, data_for_analysis) for i in range(iterations_per_thread)])
    group2 = asyncio.gather(*[process_run(i, rmd, tax, owners, expenses, data_for_analysis) for i in range(iterations_per_thread)])
    group3 = asyncio.gather(*[process_run(i, rmd, tax, owners, expenses, data_for_analysis) for i in range(iterations_per_thread)])
    group4 = asyncio.gather(*[process_run(i, rmd, tax, owners, expenses, data_for_analysis) for i in range(iterations_per_thread)])
    group5 = asyncio.gather(*[process_run(i, rmd, tax, owners, expenses, data_for_analysis) for i in range(iterations_per_thread)])
    group6 = asyncio.gather(*[process_run(i, rmd, tax, owners, expenses, data_for_analysis) for i in range(iterations_per_thread)])
    group7 = asyncio.gather(*[process_run(i, rmd, tax, owners, expenses, data_for_analysis) for i in range(iterations_per_thread)])
    group8 = asyncio.gather(*[process_run(i, rmd, tax, owners, expenses, data_for_analysis) for i in range(iterations_per_thread)])
    group9 = asyncio.gather(*[process_run(i, rmd, tax, owners, expenses, data_for_analysis) for i in range(iterations_per_thread)])
    group10 = asyncio.gather(*[process_run(i, rmd, tax, owners, expenses, data_for_analysis) for i in range(iterations_per_thread)])

    all_groups = asyncio.gather(group1, group2, group3, group4, group5, group6, group7, group8, group9, group10)                                
    results = loop.run_until_complete(all_groups)

    sorted_data = sort_data(data_for_analysis)
    plot_results(sorted_data)

    return 0

if __name__ == "__main__":
    main()