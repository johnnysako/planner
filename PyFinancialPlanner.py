
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
iterations = 105
remove_top = 5

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
    return sorted_data[remove_top:]

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

def main():
    rmd, tax, owners, expenses = load_constants()

    data_for_analysis = []

    for i in range(iterations):
        rates = np.random.normal(6.0, 12.0, years_to_process+1)

        f = open('accounts.json')
        accounts = []
        for a in json.load(f)["accounts"]:
            accounts.append(Account(a))

        plan = Plan(owners, accounts, expenses, rmd, tax)

        df = pd.DataFrame(np.array(plan.process_plan(2023, years_to_process, rates)), columns = plan.get_header())
        data_for_analysis.append(df)

    sorted_data = sort_data(data_for_analysis)
    plot_results(sorted_data)

    return 0

if __name__ == "__main__":
    main()