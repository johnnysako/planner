
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

years_to_process = 64
iterations = 210
remove = 5
mean_rate_of_return = 4
standard_deviation_of_return = 6

import asyncio
import time

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

def _draw_as_table(df, pagesize):
    alternating_colors = [['white'] * len(df.columns), ['lightgray'] * len(df.columns)] * len(df)
    alternating_colors = alternating_colors[:len(df)]
    fig, ax = plt.subplots(figsize=pagesize)
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df.values,
                        colLabels=df.columns,
                        rowColours=['lightblue']*len(df),
                        colColours=['lightblue']*len(df.columns),
                        cellColours=alternating_colors,
                        loc='center')
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(4)
    return fig
 
def plot_failed_plan_data_table(df, pdf, numpages=(1, 1), pagesize=(11, 8.5)):
    nh, nv = numpages
    rows_per_page = len(df) // nh
    cols_per_page = len(df.columns) // nv
    for i in range(0, nh):
        for j in range(0, nv):
            page = df.iloc[(i*rows_per_page):min((i+1)*rows_per_page, len(df)),
                           (j*cols_per_page):min((j+1)*cols_per_page, len(df.columns))]
            fig = _draw_as_table(page, pagesize)
            if nh > 1 or nv > 1:
                # Add a part/page number at bottom-center of page
                fig.text(0.5, 0.5/pagesize[0],
                         "Part-{}x{}: Page-{}".format(i+1, j+1, i*nv + j + 1),
                         ha='center', fontsize=8)
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()

def plot_failed_plans(failed_plans, pdf):
    for index, data in enumerate(failed_plans):
        fails_in_year = data['Year'].where(data['Sum of Accounts'] == 0).min()
        data.set_index('Year').plot.line(figsize=(10,6), fontsize=12)
        ax = plt.gca()
        plt.ticklabel_format(useOffset=False, style='plain')
        ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,}'))
        plt.title('Failed Iteration ' + str(index+1) + ' in year ' + str(fails_in_year))
        pdf.savefig()
        plt.close()
        plot_failed_plan_data_table(data, pdf, numpages=(2,1))

def plot_monte_carlo(data_for_analysis, failed_plans, pdf):
    fig = plt.figure(figsize=(10,6), dpi=300)
    for data in data_for_analysis:
        plt.plot(data['Year'], data['Sum of Accounts'])
        if data.iloc[-1]['Sum of Accounts']==0:
            failed_plans.append(data)
    
    ax = plt.gca()
    plt.ticklabel_format(useOffset=False, style='plain')
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,}'))
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
        plot_monte_carlo(data_for_analysis, failed_plans, pdf)
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

    df = pd.DataFrame(np.array(plan.process_plan(2023, years_to_process, rates)), columns = plan.get_header())
    data_for_analysis.append(df)

def main():
    rmd, tax, owners, expenses = load_constants()

    data_for_analysis = []

    loop = asyncio.get_event_loop()                                              # Have a new event loop

    looper = asyncio.gather(*[process_run(i, rmd, tax, owners, expenses, data_for_analysis) for i in range(iterations)])         # Run the loop
                                
    results = loop.run_until_complete(looper)

    sorted_data = sort_data(data_for_analysis)
    plot_results(sorted_data)

    return 0

if __name__ == "__main__":
    main()