from src.draw_table import plot_data_table

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.ticker import StrMethodFormatter

include_failed_plans = False
include_tables = False


def _plot_failed_plans(failed_plans, pdf):
    for index, data in enumerate(failed_plans):
        fails_in_year = data['Year'].where(data['Sum of Accounts'] == 0).min()
        data.set_index('Year').plot.line(figsize=(10, 6), fontsize=12)
        ax = plt.gca()
        plt.ticklabel_format(useOffset=False, style='plain')
        ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
        plt.title('Failed Iteration ' + str(index+1) +
                  ' in year ' + '{:.0f}'.format(fails_in_year))
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
            plot_data_table(data, pdf, labels,
                            'Failed Plan Data Table', numpages=(2, 1))


def get_years_to_process(start_year, owners):
    years_to_process = [start_year]
    for o in owners:
        years_to_process.append(o.retired_year())
        years_to_process.append(o.dies_in())
    return sorted(set(years_to_process))


def get_taxable_breakdown(year, data, accounts):
    taxable = 0
    tax_deferred = 0
    tax_free = 0
    index = int(year - data['Year'][0])
    for account in accounts:
        column_name = account.get_name()
        if account.is_taxable():
            taxable += data[column_name][index]
        if account.is_taxable_deferred():
            tax_deferred += data[column_name][index]
        if account.is_taxable_free():
            tax_free += data[column_name][index]
    return taxable, tax_deferred, tax_free


def summarize_tax_data(data, owners, accounts):
    summary_list = []

    start_year = data['Year'].iloc[0]
    years_to_process = get_years_to_process(start_year, owners)

    for year in years_to_process:
        taxable, tax_deferred, tax_free = get_taxable_breakdown(year, data,
                                                                accounts)
        total = taxable + tax_deferred + tax_free
        summary_dict = {'Year': year,
                        'Taxable': taxable,
                        'Tax Deferred': tax_deferred,
                        'Tax Sheltered': tax_free,
                        'Total': total}
        summary_list.append(pd.DataFrame([summary_dict]))

    summary = pd.concat(summary_list, ignore_index=True)
    summary = summary.round(2)
    return summary


def average_tax_data(data_for_analysis, owners, accounts):
    data = []

    for df in data_for_analysis:
        data.append(summarize_tax_data(df, owners, accounts))

    concatenated_data = pd.concat(data, ignore_index=True)

    averaged_data = concatenated_data.groupby('Year').mean().reset_index()
    averaged_data = averaged_data.round(2)
    print(averaged_data)

    return averaged_data


def summarize_data(data_for_analysis):
    data = []
    iterations = len(data_for_analysis)
    range = [int(iterations/100), int(iterations/4), int(iterations/2),
             int(iterations*3/4), int(iterations*99/100)]

    for i in range:
        fails_in_year = ""
        if data_for_analysis[i].iloc[-1]['Sum of Accounts'] == 0:
            fails_in_year = '{:.0f}'.format(data_for_analysis[i]['Year'].where(
                data_for_analysis[i]['Sum of Accounts'] == 0).min())
        data.append([i,
                     data_for_analysis[i]['Sum of Accounts'][5],
                     data_for_analysis[i]['Sum of Accounts'][10],
                     data_for_analysis[i]['Sum of Accounts'][15],
                     data_for_analysis[i]['Sum of Accounts'][20],
                     data_for_analysis[i]['Sum of Accounts'][25],
                     data_for_analysis[i].iloc[-1]['Sum of Accounts'],
                     data_for_analysis[i]['% Withdrawn'].mean(),
                     data_for_analysis[i]['Stock Returns'].mean(),
                     data_for_analysis[i]['Bond Returns'].mean(),
                     fails_in_year])

    summary = pd.DataFrame(np.array(data), columns=[
                           'Trial', 'Year 5', 'Year 10', 'Year 15',
                           'Year 20', 'Year 25', 'End of Plan',
                           'Average Withdrawn', 'Stock Returns',
                           'Bond Returns', 'Money to $0'])

    labels = summary['Trial'].values.astype(int)
    summary.drop('Trial', axis=1, inplace=True)
    summary.update(summary[['Year 5', 'Year 10', 'Year 15',
                   'Year 20', 'Year 25', 'Average Withdrawn',
                            'Stock Returns', 'Bond Returns',
                            'End of Plan']].astype(float))
    summary.update(summary[['Year 5', 'Year 10', 'Year 15', 'Year 20',
                   'Year 25', 'End of Plan']].applymap('${:,.0f}'.format))
    summary.update(
        summary[['Average Withdrawn', 'Stock Returns', 'Bond Returns']]
        .applymap('{:.2f}%'.format))

    return summary, labels


def _plot_summary(data_for_analysis, pdf):
    summary, labels = summarize_data(data_for_analysis)
    print(summary)
    plot_data_table(summary, pdf, labels, "Monte Carlos Summary")


def process_average(data_for_analysis):
    iterations = len(data_for_analysis)
    years_to_process = len(data_for_analysis[0].index)
    analysis = np.empty([iterations, years_to_process])
    analysis_stock = np.empty([iterations, years_to_process])
    analysis_bond = np.empty([iterations, years_to_process])
    for i, data in enumerate(data_for_analysis):
        analysis[i] = data['Sum of Accounts'].values
        analysis_stock[i] = data['Stock Returns'].values
        analysis_bond[i] = data['Bond Returns'].values
    average_plot = analysis.mean(axis=0)
    average_stock_plot = analysis_stock.mean(axis=0)
    average_bond_plot = analysis_stock.mean(axis=0)
    median = round(np.median(analysis, axis=0)[-1], 2)

    return average_plot, average_stock_plot, average_bond_plot, median


def plot_gains_losses(x_label, stock, bond, canvas):
    positive_values = [val if val > 0 else 0 for val in stock]
    negative_values = [val if val < 0 else 0 for val in stock]

    canvas.figure.clear()
    ax = canvas.figure.subplots()
    ax.bar(x_label, positive_values, color='green')
    ax.bar(x_label, negative_values, color='red')

    ax.set_ylabel('% Gain/Loss')
    ax.set_xticks([])

    canvas.draw()


def plot_trial_box(trial, ax, box_props):
    trial_label = 'Include Social Security: ' + \
        str(trial["Social Security"]) + \
        '\nSelected Roths have RMDs: ' + str(trial["rmd"]) + \
        '\nBad Timing: ' + str(trial["bad_timing"])
    ax.annotate(trial_label, xy=(0.025, .15), xycoords='axes fraction',
                fontsize=5, bbox=box_props, ha='left', va='top', color='black')


def plot_owner_lines(ax, start_year, max_y, min_y,
                     y_coordinate, box_props, owner):
    if not owner.is_retired(start_year):
        retire_year = owner.retired_year()
        label = owner.get_name() + ' Retires:\n' + \
            '{:.0f}'.format(retire_year)

        ax.annotate(label, xy=(retire_year+.5, y_coordinate), fontsize=5,
                    bbox=box_props, ha='left', va='top', color='black')
        ax.vlines(x=retire_year, ymin=min_y, ymax=max_y, colors='purple')

    death_year = owner.dies_in()
    label = owner.get_name() + ' EoP\n' + '{:.0f}'.format(death_year)
    ax.annotate(label, xy=(death_year+.5, y_coordinate), fontsize=5,
                bbox=box_props, ha='left', va='top', color='black')
    ax.vlines(x=death_year, ymin=min_y, ymax=max_y, colors='red')
    return max_y*0.1


def plot_single(data, owners, trial, index, canvas):
    canvas.figure.clear()
    ax = canvas.figure.subplots()
    start_year = data['Year'][0]

    max_y = data.values.max()
    min_y = data['Sum of Accounts'].values.min()

    ax.plot(data['Year'], data['Sum of Accounts'])
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    y_coordinate = max_y*0.05
    box_props = dict(boxstyle='round', facecolor='white', edgecolor='blue')

    for owner in owners:
        y_coordinate = plot_owner_lines(ax, start_year, max_y,
                                        min_y, y_coordinate, box_props, owner)

    plot_trial_box(trial, ax, box_props)

    ax.set_xlabel('Year', fontsize=12)
    ax.tick_params(axis='x', labelsize=6)
    ax.set_ylabel('Net Worth', fontsize=12)
    ax.tick_params(axis='y', labelsize=6)
    ax.set_title('Index ' + str(index), fontsize=14)
    results_to_include = 'EoP: ' \
        + '${:,.0f}'.format(data['Sum of Accounts'].iloc[-1])
    ax.annotate(results_to_include, xy=(0.025, 0.95), xycoords='axes fraction',
                fontsize=8, bbox=box_props, ha='left', va='top', color='black')

    plt.tight_layout()

    canvas.draw()


def plot_monte_carlos(data_for_analysis, failed_plans, owners, trial, canvas):
    canvas.figure.clear()
    ax = canvas.figure.subplots()
    start_year = data_for_analysis[0]['Year'][0]
    average_plot, _, _, median = process_average(data_for_analysis)

    max_y = float('-inf')
    min_y = float('+inf')

    for i, data in enumerate(data_for_analysis):
        max_y = max(max_y, max(data['Sum of Accounts']))
        min_y = min(min_y, min(data['Sum of Accounts']))
        if i % 20 == 0:
            ax.plot(data['Year'], data['Sum of Accounts'], color='lavender')

    ax.plot(data_for_analysis[0]['Year'], average_plot, color='black')
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    y_coordinate = max_y*0.05
    box_props = dict(boxstyle='round', facecolor='white', edgecolor='blue')

    for owner in owners:
        y_coordinate = plot_owner_lines(ax, start_year, max_y,
                                        min_y, y_coordinate, box_props, owner)

    plot_trial_box(trial, ax, box_props)

    ax.set_xlabel('Year', fontsize=12)
    ax.tick_params(axis='x', labelsize=6)
    ax.set_ylabel('Net Worth', fontsize=12)
    ax.tick_params(axis='y', labelsize=6)
    ax.set_title('Monte Carlo Analysis', fontsize=14)

    iterations = len(data_for_analysis)
    results_to_include = 'Average EoP: ' \
        + '${:,.0f}\n'.format(average_plot[-1]) \
        + "Median EoP: " \
        + '${:,.0f}\n'.format(median) \
        + '{:.1f}%'.format(len(failed_plans)/iterations*100) \
        + ' Plans failed'
    ax.annotate(results_to_include, xy=(0.025, 0.95), xycoords='axes fraction',
                fontsize=8, bbox=box_props, ha='left', va='top', color='black')

    plt.tight_layout()

    canvas.draw()


def pdf_monte_carlos(data_for_analysis, failed_plans, pdf,
                     owners, trial):
    plt.clf()
    fig, _ = plt.subplots(figsize=(11, 8.5))
    canvas = FigureCanvasQTAgg(fig)
    plot_monte_carlos(data_for_analysis, failed_plans, owners, trial, canvas)

    pdf.savefig(canvas.figure, orientation='landscape')
    plt.close(canvas.figure)

    _plot_summary(data_for_analysis, pdf)

    if include_failed_plans:
        _plot_failed_plans(failed_plans, pdf)

    return failed_plans
