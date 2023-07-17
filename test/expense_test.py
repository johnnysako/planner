from src.expense import Expense


def test_can_initialize_expense():
    config = {
        "name": "Living"
    }

    expense = Expense(config)
    assert expense.get_name() == "Living"

def test_need_or_want():
    config = {
        "need": True
    }

    expense = Expense(config)
    assert expense.is_need() == True

def test_can_get_expense_for_year():
    config = {
        "starting_year": 2000,
        "frequency": 1,
        "ammount": 100
    }

    expense = Expense(config)
    assert expense.get_expense(1999) == 0
    assert expense.get_expense(2000) == 100
    assert expense.get_expense(2001) == 100
    assert expense.get_expense(2010) == 100

def test_can_get_different_expense_for_year():
    config = {
        "starting_year": 2004,
        "frequency": 3,
        "ammount": 200
    }

    expense = Expense(config)
    assert expense.get_expense(2003) == 0
    assert expense.get_expense(2004) == 200
    assert expense.get_expense(2005) == 0
    assert expense.get_expense(2006) == 0
    assert expense.get_expense(2007) == 200

def test_expense_expires():
    config = {
        "starting_year": 2004,
        "end_year": 2007,
        "frequency": 1,
        "ammount": 200
    }

    expense = Expense(config)
    assert expense.get_expense(2003) == 0
    assert expense.get_expense(2004) == 200
    assert expense.get_expense(2005) == 200
    assert expense.get_expense(2006) == 200
    assert expense.get_expense(2007) == 200
    assert expense.get_expense(2008) == 0