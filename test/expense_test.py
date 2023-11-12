from src.expense import Expense


def test_can_initialize_expense():
    config = {
        "Description": "Living"
    }

    expense = Expense(config)
    assert expense.get_name() == "Living"


def test_can_get_expense_for_year():
    config = {
        "Year Starts": 2000,
        "Every x Year(s)": 1,
        "Cost": 100
    }

    expense = Expense(config)
    assert expense.get_expense(1999) == 0
    assert expense.get_expense(2000) == 100
    assert expense.get_expense(2001) == 100
    assert expense.get_expense(2010) == 100


def test_can_get_different_expense_for_year():
    config = {
        "Year Starts": 2004,
        "Every x Year(s)": 3,
        "Cost": 200
    }

    expense = Expense(config)
    assert expense.get_expense(2003) == 0
    assert expense.get_expense(2004) == 200
    assert expense.get_expense(2005) == 0
    assert expense.get_expense(2006) == 0
    assert expense.get_expense(2007) == 200


def test_expense_expires():
    config = {
        "Year Starts": 2004,
        "Year Ends": 2007,
        "Every x Year(s)": 1,
        "Cost": 200
    }

    expense = Expense(config)
    assert expense.get_expense(2003) == 0
    assert expense.get_expense(2004) == 200
    assert expense.get_expense(2005) == 200
    assert expense.get_expense(2006) == 200
    assert expense.get_expense(2007) == 200
    assert expense.get_expense(2008) == 0
