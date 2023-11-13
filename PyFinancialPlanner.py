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

import sys
import os
import json
import numpy as np
import pandas as pd
import datetime
import yfinance as yf

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import asyncio

start_year = 2023
iterations = 1000
iterations_per_thread = int(iterations/10)


# Place holders. Values will be generated based on S&P performance
def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(
            None, f, *args, **kwargs)

    return wrapped


def load_constants(personal_path):
    with open(os.path.join(personal_path, 'rmd.json')) as f:
        rmd = Rmd(json.load(f)["rmd"])

    with open(os.path.join(personal_path, 'tax.json')) as f:
        tax = Tax(json.load(f)["tax"])

    with open(os.path.join(personal_path, 'owners.json')) as f:
        owners_data = json.load(f).get("owners", [])
        owners = [Owner(owner_data) for owner_data in owners_data]

    years_to_process = 0
    for o in owners:
        owner_years_to_process = o.years_to_live(start_year)
        if owner_years_to_process > years_to_process:
            years_to_process = owner_years_to_process

    with open(os.path.join(personal_path, 'expenses.json')) as f:
        expense_data = json.load(f).get("expenses", [])
        expenses = Expenses([Expense(expense) for expense in expense_data])

    return rmd, tax, owners, expenses, years_to_process


def sort_failed(failed_plans):
    return sorted(failed_plans,
                  key=lambda x:
                  x['Year'].where(x['Sum of Accounts'] == 0).min(),
                  reverse=True)


def sort_data(data_for_analysis):
    failed_plans = []
    remove_index = -1

    sorted_data = sorted(data_for_analysis,
                         key=lambda x: x.iloc[-1]['Sum of Accounts'],
                         reverse=True)

    for i, data in enumerate(sorted_data):
        if data.iloc[-1]['Sum of Accounts'] == 0:
            failed_plans.append(data)
            if remove_index == -1:
                remove_index = i

    del sorted_data[remove_index:]
    failed_plans = sort_failed(failed_plans)

    for data in failed_plans:
        sorted_data.append(data)

    return sorted_data, failed_plans


def plot_expense_table(expenses, years_to_process, pdf):
    expense_table = []
    for year in range(start_year, start_year+years_to_process):
        expense_table.append([year] + expenses.get_year(year))
    data = pd.DataFrame(expense_table, columns=['Year'] + expenses.get_names())

    data.plot.bar(x='Year', stacked=True, figsize=(10, 6))
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
    plot_data_table(data, pdf, labels, "Expense Table", numpages=(2, 2))


def plot_accounts_table(personal_path, pdf):
    with open(os.path.join(personal_path, 'accounts.json')) as f:
        account_data = json.load(f).get("accounts", [])
        accounts = [Account(account_data) for account_data in account_data]

    account_table = []
    total = 0
    for account in accounts:
        total = total + account.get_balance()
        account_table.append([account.get_name(),
                              account.get_balance(),
                              account.get_type(),
                              account.get_owner()])
    account_table.append(['Total', total, ''])
    data = pd.DataFrame(account_table,
                        columns=['Account', 'Balance', 'Type', 'Owner'])

    labels = data['Account']
    data.drop('Account', axis=1, inplace=True)
    data.update(data[['Balance']].astype(float))
    data.update(data[['Balance']].applymap('{:,.0f}'.format))
    plot_data_table(data, pdf, labels, "Account Summary")


def generate_returns(data_distribution, mean, std, years_to_process):
    randoms = [int(x) for x in np.floor(np
                                        .random.default_rng()
                                        .normal(mean,
                                                std,
                                                years_to_process+1))]
    randoms = np.clip(randoms, 0, len(data_distribution)-1)
    # print(randoms)
    returns = []
    for random in randoms:
        if random <= 0:
            returns.append(data_distribution[random])
        else:
            returns.append(np.random
                           .uniform(data_distribution[random-1],
                                    data_distribution[random]))
    return np.array(returns)


@background
def process_run(iteration,
                rmd,
                tax,
                owners,
                expenses,
                trial,
                data_for_analysis,
                average_stock_rates,
                average_bond_rates,
                years_to_process,
                personal_path):
    stock_rates = generate_returns(trial["dist"]["stocks"],
                                   26, 9, years_to_process)*100
    bond_rates = generate_returns(trial["dist"]["bonds"],
                                  6, 2, years_to_process)*100

    with open(os.path.join(personal_path, 'accounts.json')) as f:
        account_data = json.load(f).get("accounts", [])
        accounts = [Account(account_data) for account_data in account_data]

    plan = Plan(owners, accounts, expenses, rmd, tax, trial)

    combined_rates = {"s": stock_rates, "b": bond_rates}
    data = pd.DataFrame(np.array(
        plan.process_plan(start_year,
                          years_to_process,
                          combined_rates)), columns=plan.get_header())
    data_for_analysis.append(data)
    average_stock_rates.append(np.average(stock_rates))
    average_bond_rates.append(np.average(bond_rates))


def run_monte_carlos(data_for_analysis,
                     rmd,
                     tax,
                     owners,
                     expenses,
                     trial,
                     average_stock_rates,
                     average_bond_rates,
                     years_to_process,
                     personal_path):
    loop = asyncio.get_event_loop()

    group1 = asyncio.gather(*[process_run(i, rmd, tax, owners,
                            expenses, trial, data_for_analysis,
                            average_stock_rates, average_bond_rates,
                            years_to_process, personal_path)
                            for i in range(iterations_per_thread)])
    group2 = asyncio.gather(*[process_run(i, rmd, tax, owners,
                            expenses, trial, data_for_analysis,
                            average_stock_rates,  average_bond_rates,
                            years_to_process, personal_path)
                            for i in range(iterations_per_thread)])
    group3 = asyncio.gather(*[process_run(i, rmd, tax, owners,
                            expenses, trial, data_for_analysis,
                            average_stock_rates,  average_bond_rates,
                            years_to_process, personal_path)
                            for i in range(iterations_per_thread)])
    group4 = asyncio.gather(*[process_run(i, rmd, tax, owners,
                            expenses, trial, data_for_analysis,
                            average_stock_rates,  average_bond_rates,
                            years_to_process, personal_path)
                            for i in range(iterations_per_thread)])
    group5 = asyncio.gather(*[process_run(i, rmd, tax, owners,
                            expenses, trial, data_for_analysis,
                            average_stock_rates, average_bond_rates,
                            years_to_process, personal_path)
                            for i in range(iterations_per_thread)])
    group6 = asyncio.gather(*[process_run(i, rmd, tax, owners,
                            expenses, trial, data_for_analysis,
                            average_stock_rates, average_bond_rates,
                            years_to_process, personal_path)
                            for i in range(iterations_per_thread)])
    group7 = asyncio.gather(*[process_run(i, rmd, tax, owners,
                            expenses, trial, data_for_analysis,
                            average_stock_rates, average_bond_rates,
                            years_to_process, personal_path)
                            for i in range(iterations_per_thread)])
    group8 = asyncio.gather(*[process_run(i, rmd, tax, owners,
                            expenses, trial, data_for_analysis,
                            average_stock_rates, average_bond_rates,
                            years_to_process, personal_path)
                            for i in range(iterations_per_thread)])
    group9 = asyncio.gather(*[process_run(i, rmd, tax, owners,
                            expenses, trial, data_for_analysis,
                            average_stock_rates, average_bond_rates,
                            years_to_process, personal_path)
                            for i in range(iterations_per_thread)])
    group10 = asyncio.gather(*[process_run(i, rmd, tax, owners,
                             expenses, trial, data_for_analysis,
                             average_stock_rates, average_bond_rates,
                             years_to_process, personal_path)
                             for i in range(iterations_per_thread)])

    all_groups = asyncio.gather(
        group1, group2, group3, group4, group5,
        group6, group7, group8, group9, group10)
    loop.run_until_complete(all_groups)


def main(personal_path=""):
    rmd, tax, owners, expenses, years_to_process = \
        load_constants(personal_path)

    # Define the S&P 500 symbol and time period for historical data
    symbol = "^GSPC"
    start_date = "1950-01-01"
    end_date = "2021-12-31"

    # Download historical S&P 500 data using Yahoo Finance
    data = yf.download(symbol, start=start_date, end=end_date)

    # Calculate annual returns from historical data
    stock_annual_returns = data['Adj Close'].resample(
        'Y').ffill().pct_change().dropna()
    sorted_stock_annual_returns = sorted(stock_annual_returns)

    # Define the S&P 500 symbol and time period for historical data
    symbol = "LQD"
    start_date = "2002-07-29"
    end_date = "2021-12-31"

    # Download historical S&P 500 data using Yahoo Finance
    data = yf.download(symbol, start=start_date, end=end_date)

    # Calculate annual returns from historical data
    bond_annual_returns = data['Adj Close'].resample(
        'Y').ffill().pct_change().dropna()
    sorted_bond_annual_returns = sorted(bond_annual_returns)

    returns = {"stocks": sorted_stock_annual_returns,
               "bonds": sorted_bond_annual_returns}

    # Scenarios:
    # 1. As is
    # 2. Trial selected Roth with RMDs (aka 401K)
    # 3. No Social Security
    # 4. No Social Security and Trial selected Roth with RMDs
    trials = [
        {"Social Security": True, "rmd": False,
         "dist": returns},
        # {"Social Security": True, "rmd": True,
        #  "dist": returns},
        {"Social Security": False, "rmd": False,
         "dist": returns},
        # {"Social Security": False, "rmd": True,
        #  "dist": returns}
    ]

    with PdfPages(os.path.join(personal_path, 
                               'financial_analysis.pdf')) as pdf:
        plot_accounts_table(personal_path, pdf)

        for trial in trials:
            data_for_analysis = []
            average_stock_rates = []
            average_bond_rates = []

            run_monte_carlos(data_for_analysis, rmd, tax, owners,
                             expenses, trial, average_stock_rates,
                             average_bond_rates, years_to_process,
                             personal_path)

            sorted_data, failed_plans = sort_data(data_for_analysis)

            print('Average Rate of Return (Stocks): {:0.2f}%'.format(
                np.average(average_stock_rates)))
            print('Average Rate of Return (Bonds): {:0.2f}%'.format(
                np.average(average_bond_rates)))
            plot_monte_carlos(sorted_data, failed_plans, pdf, owners, trial)

        plot_expense_table(expenses, years_to_process, pdf)

        d = pdf.infodict()
        d['Title'] = 'Financial Projection'
        d['Author'] = u'John Chapman'
        d['CreationDate'] = datetime.datetime.today()

    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main('data')
