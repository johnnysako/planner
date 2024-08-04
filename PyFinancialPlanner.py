#!/usr/bin/env python
# -*- coding: utf-8 -*-
from src.plan import Plan
from src.rmd import Rmd
from src.tax import Tax
from src.expenses import Expenses
from src.expense import Expense
from src.account import Account
from src.owner import Owner
from src.generate_pdf import plot_pdf
from src.sort import sort_data

import sys
import os
import json
import numpy as np
import pandas as pd

import asyncio

basedir = os.path.dirname(__file__)

start_year = 2024
iterations = 1000
num_groups = 10
iterations_per_thread = int(iterations/num_groups)


def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(
            None, f, *args, **kwargs)

    return wrapped


def load_constants(personal_path):
    with open(os.path.join(basedir, '_internal', 'rmd.json')) as f:
        rmd = Rmd(json.load(f)["rmd"])

    with open(os.path.join(basedir, '_internal', 'tax.json')) as f:
        tax = Tax(json.load(f)["tax"])

    with open(os.path.join(personal_path, 'owners.json')) as f:
        owners_data = json.load(f).get("owners", [])
        if len(owners_data) > 2:
            raise ValueError("Owners exceeds two")

        owners = [Owner(owner_data) for owner_data in owners_data]

    years_to_process = max(o.years_to_live(start_year) for o in owners)

    with open(os.path.join(personal_path, 'expenses.json')) as f:
        expense_data = json.load(f).get("expenses", [])
        expenses = Expenses([Expense(expense) for expense in expense_data])

    with open(os.path.join(personal_path, 'accounts.json')) as f:
        account_data = json.load(f).get("accounts", [])
        account_base = [Account(account_data) for account_data in account_data]

    return rmd, tax, owners, expenses, years_to_process, account_base


@background
def process_run(iteration,
                loop,
                rmd,
                tax,
                owners,
                expenses,
                trial,
                data_for_analysis,
                years_to_process,
                personal_path):

    def load_returns(data, iteration, years_to_process):
        rate_iteration = data[iteration]
        return rate_iteration[:years_to_process]*100

    full_iteration = loop*iterations_per_thread+iteration
    stock_rates = load_returns(trial["dist"]["stocks"],
                               full_iteration,
                               years_to_process+1)

    bond_rates = load_returns(trial["dist"]["bonds"],
                              full_iteration,
                              years_to_process+1)

    with open(os.path.join(personal_path, 'accounts.json')) as f:
        account_data = json.load(f).get("accounts", [])
        accounts = [Account(account_data) for account_data in account_data]

    plan = Plan(start_year, owners, accounts, expenses, rmd, tax, trial)

    combined_rates = {"s": stock_rates, "b": bond_rates}
    data = pd.DataFrame(np.array(
        plan.process_plan(years_to_process,
                          combined_rates)), columns=plan.get_header())
    data_for_analysis.append(data)


async def run_monte_carlos(data_for_analysis,
                           rmd,
                           tax,
                           owners,
                           expenses,
                           trial,
                           years_to_process,
                           personal_path):
    groups = [
        asyncio.gather(
            *[process_run(i, j, rmd, tax, owners, expenses, trial,
                          data_for_analysis, years_to_process, personal_path)
              for i in range(iterations_per_thread)]
        )
        for j in range(num_groups)
    ]

    await asyncio.gather(*groups)


def load_returns(stock_file, bond_file):
    def load_all_returns(file):
        with open(file, 'r') as f:
            data = json.load(f)
            return np.array(data)

    stock_rates = load_all_returns(stock_file)
    bond_rates = load_all_returns(bond_file)

    returns = {"stocks": stock_rates, "bonds": bond_rates}
    return returns


def run_trials(personal_path="", with_social=False,
               with_rmd_trial=False, with_bad_timing=False):
    rmd, tax, owners, expenses, years_to_process, account_base = \
        load_constants(personal_path)

    stock_file = os.path.join('_internal', 'stock_returns.json')
    bond_file = os.path.join('_internal', 'bond_returns.json')

    returns = load_returns(stock_file, bond_file)

    trials = [
        {"Social Security": True, "rmd": False, "bad_timing": False,
         "dist": returns}]

    if with_social:
        trials.append({"Social Security": False, "rmd": False,
                       "bad_timing": False, "dist": returns})

    if with_rmd_trial:
        trials.append({"Social Security": True, "rmd": True,
                       "bad_timing": False, "dist": returns})

    if with_bad_timing:
        trials.append({"Social Security": True, "rmd": False,
                       "bad_timing": True, "dist": returns})

    trials_data = []

    for trial in trials:
        data_for_analysis = []

        asyncio.run(run_monte_carlos(data_for_analysis, rmd, tax, owners,
                                     expenses, trial, years_to_process,
                                     personal_path))

        sorted_data, failed_plans = sort_data(data_for_analysis)

        trial_data = {'sorted_data': sorted_data,
                      'failed_plans': failed_plans,
                      'trial': trial}
        trials_data.append(trial_data)

    data_to_return = {'trials_data': trials_data,
                      'owners': owners,
                      'expenses': expenses,
                      'account_base': account_base,
                      'start_year': start_year,
                      'years_to_process': years_to_process}
    return data_to_return


if __name__ == "__main__":
    personal_path = '_internal'
    if len(sys.argv) > 1:
        personal_path = sys.argv[1]

    results = run_trials(personal_path, True, True, True)
    plot_pdf(results['trials_data'], results['owners'], results['expenses'],
             results['start_year'], results['years_to_process'],
             personal_path, personal_path)
