
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

def main():
    rmd, tax, owners, expenses = load_constants()

    data_for_analysis = []

    for i in range(100):
        rates = np.random.normal(7.0, 12.0, years_to_process+1)

        f = open('accounts.json')
        accounts = []
        for a in json.load(f)["accounts"]:
            accounts.append(Account(a))

        plan = Plan(owners, accounts, expenses, rmd, tax)

        data = []
        data.append(plan.get_header())
        data += plan.process_growth(2023, years_to_process, rates)

        data_for_analysis.append(data)

    for data in data_for_analysis:
        years = []
        total = []
        for year in data[1:]:
            years.append(year[0])
            total.append(year[-1])

        plt.plot(years, total)

    plt.xlabel('Year')
    plt.ylabel('Net Worth')
    plt.show()
    return 0

if __name__ == "__main__":
    main()