from src.expenses import Expenses
from src.expense import Expense

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
