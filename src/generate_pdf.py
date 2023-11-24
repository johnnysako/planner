import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd

import datetime
import os
import json

from src.draw_table import plot_data_table
from src.plot_monte_carlos import pdf_monte_carlos
from src.expenses import generate_expense_over_time
from src.account import Account


def plot_expense_table(expenses, start_year, years_to_process, pdf):
    data = generate_expense_over_time(expenses, start_year, years_to_process)
    data.plot.bar(x='Year', stacked=True, figsize=(10, 6))
    plt.xlabel('Year', fontsize=10)
    plt.xticks(fontsize=6)
    plt.ylabel('Expenses', fontsize=10)
    plt.yticks(fontsize=10)
    plt.title('Expenses over Time')
    plt.legend(prop={'size': 6})
    current_figure = plt.gcf().number
    pdf.savefig()
    plt.close(current_figure)

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


def plot_pdf(trials_data, owners, expenses, start_year, years_to_process,
             personal_path, save_path):
    with PdfPages(os.path.join(save_path,
                               'financial_analysis.pdf')) as pdf:
        plot_accounts_table(personal_path, pdf)

        for trial_data in trials_data:
            pdf_monte_carlos(trial_data['sorted_data'],
                             trial_data['failed_plans'], pdf,
                             owners, trial_data['trial'])

        plot_expense_table(expenses, start_year, years_to_process, pdf)

        d = pdf.infodict()
        d['Title'] = 'Financial Projection'
        d['Author'] = u'John Chapman'
        d['CreationDate'] = datetime.datetime.today()
