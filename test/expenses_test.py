from src.expense import Expense
from src.expenses import Expenses
from src.expenses import plot_expenses_summary
from src.expenses import generate_expense_over_time
import pandas as pd
import matplotlib.pyplot as plt

table = []
table.append(Expense({
    "Description": "Travel",
    "Cost": 2000,
    "Year Starts": 2010,
    "Every x Year(s)": 1
}))
table.append(Expense({
    "Description": "Car",
    "Cost": 20000,
    "Year Starts": 2007,
    "Every x Year(s)": 5
}))


def test_can_initialize_expenses():
    expenses = Expenses(table)
    assert expenses.get_names() == ["Travel", "Car"]


def test_can_get_expenses():
    expenses = Expenses(table)
    assert expenses.get_expenses(2007) == 20000
    assert expenses.get_expenses(2008) == 0
    assert expenses.get_expenses(2009) == 0
    assert expenses.get_expenses(2010) == 2000
    assert expenses.get_expenses(2011) == 2000
    assert expenses.get_expenses(2012) == 22000
    assert expenses.get_expenses(2013) == 2000


def test_can_get_expense_breakdown():
    expenses = Expenses(table)
    assert expenses.get_year(2012) == [2000, 20000]


def test_generate_expense_over_time():
    expenses = Expenses(table)
    start_year = 2007
    years_to_process = 7
    data = generate_expense_over_time(expenses, start_year, years_to_process)

    expected_data = {
        'Year': [2007, 2008, 2009, 2010, 2011, 2012, 2013],
        'Travel': [0, 0, 0, 2000, 2000, 2000, 2000],
        'Car': [20000, 0, 0, 0, 0, 20000, 0]
    }
    expected_df = pd.DataFrame(expected_data)

    pd.testing.assert_frame_equal(data, expected_df)


def test_plot_expenses_summary():
    expenses = Expenses(table)
    start_year = 2007
    years_to_process = 7
    data = generate_expense_over_time(expenses, start_year, years_to_process)

    fig, _ = plt.subplots()
    canvas = fig.canvas

    plot_expenses_summary(data, canvas)

    ax = canvas.figure.axes[0]

    assert ax.get_title() == 'Expenses over Time'
    assert ax.get_xlabel() == 'Year'
    assert ax.get_ylabel() == 'Expenses'

    legend_labels = [text.get_text() for text in ax.get_legend().get_texts()]
    assert legend_labels == ['Travel', 'Car']

    x_labels = [int(label.get_text()) for label in ax.get_xticklabels()]
    assert x_labels == [2007, 2008, 2009, 2010, 2011, 2012, 2013]

    num_bars = len(ax.patches)
    assert num_bars == 14  # 7 years * 2 bars per year (Travel and Car)
