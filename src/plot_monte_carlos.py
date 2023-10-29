from src.draw_table import plot_data_table

import numpy as np
import pandas as pd
import math

import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

include_failed_plans = False
include_tables = True


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


def _plot_summary(data_for_analysis, pdf):
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
                     fails_in_year])

    summary = pd.DataFrame(np.array(data), columns=[
                           'Trial', 'Year 5', 'Year 10', 'Year 15',
                           'Year 20', 'Year 25', 'End of Plan', 'Money to $0'])

    labels = summary['Trial'].values.astype(int)
    summary.drop('Trial', axis=1, inplace=True)
    summary.update(summary[['Year 5', 'Year 10', 'Year 15',
                   'Year 20', 'Year 25', 'End of Plan']].astype(float))
    summary.update(summary[['Year 5', 'Year 10', 'Year 15', 'Year 20',
                   'Year 25', 'End of Plan']].applymap('{:,.0f}'.format))
    print(summary)
    plot_data_table(summary, pdf, labels, "Monte Carlos Summary")

    median_result = pd.DataFrame(data_for_analysis[int(iterations/2)])
    labels = median_result['Year'].values.astype(int)
    median_result.drop('Year', axis=1, inplace=True)
    median_result.update(median_result.astype(float))

    cols = median_result.columns.tolist()
    for col in cols:
        if col == '% Withdrawn':
            median_result[col] = median_result[col].map('{:,.2f}%'.format)
        else:
            median_result[col] = median_result[col].map('${:,.0f}'.format)

    num_rows, num_columns = median_result.shape
    plot_data_table(median_result, pdf, labels,
                    'Median Data Table', numpages=(
                        math.ceil(num_rows / 33), math.ceil(num_columns / 10)))


def plot_monte_carlos(data_for_analysis, failed_plans, pdf, owners, trial):
    iterations = len(data_for_analysis)
    start_year = data_for_analysis[0]['Year'][0]
    years_to_process = len(data_for_analysis[0].index)
    analysis = np.empty([iterations, years_to_process])
    fig = plt.figure(figsize=(10, 6), dpi=300)
    for i, data in enumerate(data_for_analysis):
        analysis[i] = data['Sum of Accounts'].values
        if i % 20 == 0:
            plt.plot(data['Year'], data['Sum of Accounts'], color='lavender')

    average_plot = analysis.mean(axis=0)
    plt.plot(data_for_analysis[0]['Year'], average_plot, color='black')
    median = round(np.median(analysis, axis=0)[-1], 2)
    print('Median EoP: ${:,.0f}'.format(median))
    print('Mean EoP: ${:,.0f}'.format(average_plot[-1]))
    ax = plt.gca()
    plt.ticklabel_format(useOffset=False, style='plain')
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    ticks, _ = plt.yticks()
    for owner in owners:
        if not owner.is_retired(start_year):
            retire_year = start_year + owner.get_retirement_age() \
                - owner.get_age(start_year)
            label = owner.get_name() + ' Retires\n' + \
                '{:.0f}'.format(retire_year)
            ax.annotate(label, xy=(retire_year, ticks[-2]*1.01), fontsize=5)
            plt.vlines(x=retire_year,
                       ymin=ticks[1], ymax=ticks[-2], colors='purple')

    trial_label = 'Include Social Security: ' + \
        str(trial["social_security"]) + \
        '\nSelected roths have RMDs: ' + str(trial["rmd"])
    print(trial_label)
    ax.annotate(trial_label, xy=(start_year, ticks[0]/5), fontsize=5)

    plt.xlabel('Year', fontsize=12)
    plt.xticks(fontsize=6)
    plt.ylabel('Net Worth', fontsize=12)
    plt.yticks(fontsize=6)
    plt.title('Monte Carlo Analysis', fontsize=14)

    results_to_include = 'Average EoP: ' \
                         + '${:,.0f}\n'.format(average_plot[-1]) \
                         + "Median EoP: " \
                         + '${:,.0f}\n'.format(median) \
                         + '{:.1f}%'.format(len(failed_plans)/iterations*100) \
                         + ' Plans failed'
    box_props = dict(boxstyle='round', facecolor='white', edgecolor='blue')
    plt.text(0.025, 0.9, results_to_include,
             transform=plt.gca().transAxes, fontsize=8, bbox=box_props)

    pdf.savefig()
    plt.close(fig)

    _plot_summary(data_for_analysis, pdf)

    if include_failed_plans:
        _plot_failed_plans(failed_plans, pdf)

    return failed_plans
