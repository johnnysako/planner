
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.plan import Plan
from src.rmd import Rmd
from src.tax import Tax
from src.expenses import Expenses
from src.account import Account
from src.owner import Owner

import json
import csv
import numpy as np

def load_constants():
    f = open('rmd.json')
    rmd = Rmd(json.load(f)["rmd"])

    f = open('tax.json')
    tax = Tax(json.load(f)["tax"])

    f = open('config.json')
    config = json.load(f)

    f = open('owners.json')
    owners = []
    for o in json.load(f)["owners"]:
        owners.append(Owner(o))

    return rmd, tax, config, owners 

def main():
    rmd, tax, config, owners = load_constants()

    rates = np.random.normal(config["average_growth"], 12.0, 100)

    empty_expense_table = []
    empty_expenses = Expenses(empty_expense_table)

    data_for_analysis = []

    for rate in rates:
        config["average_growth"] = rate

        f = open('accounts.json')
        accounts = []
        for a in json.load(f)["accounts"]:
            accounts.append(Account(a))

        plan = Plan(config, owners, accounts, empty_expenses, rmd, tax)

        data = []
        data.append(plan.get_header())
        data += plan.process_growth(2023, 64)

        data_for_analysis.append(data)

    return 0

if __name__ == "__main__":
    main()