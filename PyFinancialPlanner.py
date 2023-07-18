
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

import matplotlib.pyplot as plt

years_to_process = 64

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
    return sorted_data[5:]

def plot_year(data):
    data.set_index('Year').plot.line()
    plt.ticklabel_format(useOffset=False, style='plain')
    plt.show()

def plot_results(data_for_analysis):
    failed_plans = 0
    for data in data_for_analysis:
        plt.plot(data['Year'], data['Sum of Accounts'])
        if data.iloc[-1]['Sum of Accounts']==0:
            failed_plans+=1
    
    print("Failed Plans:", failed_plans)
    plt.ticklabel_format(useOffset=False, style='plain')
    plt.xlabel('Year')
    plt.ylabel('Net Worth')
    plt.show()

def main():
    rmd, tax, owners, expenses = load_constants()

    data_for_analysis = []

    for i in range(10):
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