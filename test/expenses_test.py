from src.expenses import Expenses
from src.expense import Expense

table = []
table.append(Expense({
    "name": "Travel",
    "need": False,
    "ammount": 2000,
    "starting_year": 2010,
    "frequency": 1
}))
table.append(Expense({
    "name": "Car",
    "need": True,
    "ammount": 20000,
    "starting_year": 2007,
    "frequency": 5
}))


def test_can_initialize_expenses():
    expenses = Expenses(table)
    assert expenses.get_names() == [ "Travel", "Car" ]

def test_can_get_needs():
    expenses = Expenses(table)
    assert expenses.get_needs_names() == [ "Car" ]

def test_can_get_wants():
    expenses = Expenses(table)
    assert expenses.get_wants_names() == [ "Travel" ]

def test_can_get_expenses():
    expenses = Expenses(table)
    assert expenses.get_expenses(2007) == 20000
    assert expenses.get_expenses(2008) == 0
    assert expenses.get_expenses(2009) == 0
    assert expenses.get_expenses(2010) == 2000
    assert expenses.get_expenses(2011) == 2000
    assert expenses.get_expenses(2012) == 22000
    assert expenses.get_expenses(2013) == 2000

def test_can_get_needs():
    expenses = Expenses(table)
    assert expenses.get_needs(2007) == 20000
    assert expenses.get_needs(2008) == 0
    assert expenses.get_needs(2009) == 0
    assert expenses.get_needs(2010) == 0
    assert expenses.get_needs(2011) == 0
    assert expenses.get_needs(2012) == 20000
    assert expenses.get_needs(2013) == 0
