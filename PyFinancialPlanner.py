
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.plan import Plan
from src.rmd import Rmd
from src.tax import Tax
from src.expenses import Expenses
from src.account import Account
from src.owner import Owner

import json

def main():
    """ Main program """
    f = open('config.json')
    config = json.load(f)

    f = open('accounts.json')
    accounts = []
    for a in json.load(f)["accounts"]:
        accounts.append(Account(a))

    f = open('rmd.json')
    rmd = Rmd(json.load(f)["rmd"])

    f = open('tax.json')
    tax = Tax(json.load(f)["tax"])

    f = open('owners.json')
    owners = []
    for o in json.load(f)["owners"]:
        owners.append(Owner(o))

    empty_expense_table = []
    empty_expenses = Expenses(empty_expense_table)

    plan = Plan(config, owners, accounts, empty_expenses, rmd, tax)

    print(plan.get_header())
    print(plan.process_growth(2023, 5))

    return 0

if __name__ == "__main__":
    main()