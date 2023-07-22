
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
mean_rate_of_return = 4.19
standard_deviation_of_return = 10.94
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
        plt.title('Failed Iteration ' + str(index+1) + ' in year ' + '{:.0f}'.format(fails_in_year))
        plt.legend(prop={'size': 6})
        plt.xticks(fontsize=6)
        plt.yticks(fontsize=6)
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
    range = [int(iterations/100), int(iterations/4), int(iterations/2), int(iterations*3/4), int(iterations*99/100)]
    for i in range:
        fails_in_year = ""
        if data_for_analysis[i]['Sum of Accounts'][years_to_process] == 0:
            fails_in_year = '{:.0f}'.format(data_for_analysis[i]['Year'].where(data_for_analysis[i]['Sum of Accounts'] == 0).min())
        data.append([i, 
                     data_for_analysis[i]['Sum of Accounts'][5], 
                     data_for_analysis[i]['Sum of Accounts'][10], 
                     data_for_analysis[i]['Sum of Accounts'][15], 
                     data_for_analysis[i]['Sum of Accounts'][20], 
                     data_for_analysis[i]['Sum of Accounts'][25], 
                     data_for_analysis[i]['Sum of Accounts'][years_to_process],
                     fails_in_year])

    summary = pd.DataFrame(np.array(data), columns=['Trial', 'Year 5', 'Year 10', 'Year 15', 'Year 20', 'Year 25', 'End of Plan', 'Money to $0'])

    labels = summary['Trial'].values.astype(int)
    summary.drop('Trial', axis=1, inplace=True)

    summary.update(summary[['Year 5', 'Year 10', 'Year 15', 'Year 20', 'Year 25', 'End of Plan']].astype(float))
    summary.update(summary[['Year 5', 'Year 10', 'Year 15', 'Year 20', 'Year 25', 'End of Plan']].applymap('{:,.0f}'.format))

    plot_data_table(summary, pdf, labels)

def plot_monte_carlos(data_for_analysis, failed_plans, pdf, owners):
    analysis = np.empty([iterations, years_to_process+1])
    fig = plt.figure(figsize=(10,6), dpi=300)
    for i, data in enumerate(data_for_analysis):
        analysis[i] = data['Sum of Accounts'].values
        plt.plot(data['Year'], data['Sum of Accounts'])
    
    average_plot = analysis.mean(axis=0)
    plt.plot(data_for_analysis[0]['Year'], average_plot, color='black')
    print('{:,.0f}'.format(round(np.median(analysis, axis=0)[-1], 2)))
    
    ax = plt.gca()
    plt.ticklabel_format(useOffset=False, style='plain')
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    for owner in owners:
        if not owner.is_retired(start_year):
            ticks, _ = plt.yticks()
            retire_year = start_year + owner.get_retirement_age()-owner.get_age(start_year)
            label = owner.get_name() + ' Retires\n' + str(retire_year)
            ax.annotate(label, xy=(retire_year, ticks[-2]*1.01), fontsize=5)
            plt.vlines(x = retire_year, ymin = ticks[1], ymax = ticks[-2], colors = 'purple')   

    plt.xlabel('Year', fontsize=12)
    plt.xticks(fontsize=6)
    plt.ylabel('Net Worth', fontsize=12)
    plt.yticks(fontsize=6)
    plt.title('Monte Carlo Analysis\nAverage EoP: ' 
              + '${:,.0f}\n'.format(average_plot[-1])
              + '{:.2f}%'.format(len(failed_plans)/iterations*100)
              + ' Plans failed')
    pdf.savefig()
    plt.close(fig)

    return failed_plans

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
    plot_data_table(data, pdf, labels, numpages=(2,2))

def plot_results(data_for_analysis, failed_plans, expenses, owners):
    with PdfPages('financial_analysis.pdf') as pdf:
        plot_expense_table(expenses, pdf)
        plot_monte_carlos(data_for_analysis, failed_plans, pdf, owners)
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

    data = pd.DataFrame(np.array(plan.process_plan(start_year, years_to_process, rates)), columns = plan.get_header())
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

    sorted_data, failed_plans = sort_data(data_for_analysis)
    plot_results(sorted_data, failed_plans, expenses, owners)

    return 0

if __name__ == "__main__":
    main()