from src.plan import Plan
from src.account import Account
from src.owner import Owner
from src.expense import Expense
from src.expenses import Expenses
from src.rmd import Rmd
from src.tax import Tax

import pytest

expty_tax = [
    {
        "max_tax_previous": 0,
        "rate": 0,
        "cutoff": 22000
    }
]
no_tax = Tax(expty_tax)

rates = [6, 6]

def test_can_initialize_plan():
    rmd_table = []
    rmd = Rmd(rmd_table)

    accounts = []
    owners = []
    expense_table = []
    expenses = Expenses(expense_table)

    plan = Plan(owners, accounts, expenses, rmd, no_tax)

def test_can_get_header():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions":2000,
        "type": "Investment",
        "withdrawl priority": 1,
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    owners = []
    expense_table = []
    expenses = Expenses(expense_table)

    plan = Plan(owners, accounts, expenses, rmd, no_tax)
    assert plan.get_header() == ["Year", "Income", "Rmd", "Expenses", "Jerry's Roth", "Taxes", "Sum of Accounts"]

def test_can_fill_table_for_one_year():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions":2000,
        "type": "Roth",
        "withdrawl priority": 1,
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jill's Investment",
        "balance": 10000,
        "annual_additions": 5000,
        "type": "Investment",
        "withdrawl priority": 3,
        "owner": "Jill",
        "trail_with_rmd": False
    }))

    owners = []
    owners.append(Owner({
        "name": "Jill",
        "birth_year": 1977,
        "income": 2000,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))
    owners.append(Owner({
        "name": "Jerry",
        "birth_year": 1977,
        "income": 1000,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))

    expense_table = []
    expense_table.append(Expense({
        "name": "Travel",
        "need": False,
        "ammount": 2000,
        "starting_year": 2010,
        "frequency": 1
    }))
    expense_table.append(Expense({
        "name": "Car",
        "need": True,
        "ammount": 200,
        "starting_year": 2007,
        "frequency": 5
    }))
    expenses = Expenses(expense_table)

    plan = Plan(owners, accounts, expenses, rmd, no_tax)
    assert plan.process_plan(2022, 0, rates) == [[2022, 3000, 0, 2200, 1800.0, 10000, 0.0, 11800.0]]

def test_can_fill_table_for_two_years():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions":2000,
        "type": "Roth",
        "withdrawl priority": 1,
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jill's Investment",
        "balance": 10000,
        "annual_additions": 5000,
        "type": "Investment",
        "withdrawl priority": 3,
        "owner": "Jill",
        "trail_with_rmd": False
    }))

    owners = []
    owners.append(Owner({
        "name": "Jill",
        "birth_year": 1977,
        "income": 2000,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))
    owners.append(Owner({
        "name": "Jerry",
        "birth_year": 1977,
        "income": 1000,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))

    expense_table = []
    expense_table.append(Expense({
        "name": "Travel",
        "need": False,
        "ammount": 2000,
        "starting_year": 2010,
        "frequency": 1
    }))
    expense_table.append(Expense({
        "name": "Car",
        "need": True,
        "ammount": 200,
        "starting_year": 2007,
        "frequency": 5
    }))
    expenses = Expenses(expense_table)

    plan = Plan(owners, accounts, expenses, rmd, no_tax)
    assert plan.process_plan(2022, 1, rates) == [[2022, 3000, 0, 2200, 1800.0, 10000, 0.0, 11800.0], [2023, 3000, 0, 2000, 1908.0, 15600.0, 0.0, 17508.0]]

def test_owners_do_not_match_accounts():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions":2000,
        "type": "Roth",
        "withdrawl priority": 1,
        "owner": "Jerry",
        "trail_with_rmd": False
    }))

    bad_owners = []
    bad_owners.append(Owner({
        "name": "Babs",
        "birth_year": 1977,
        "income": 56789,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))

    expense_table = []
    expenses = Expenses(expense_table)
    plan = Plan(bad_owners, accounts, expenses, rmd, no_tax)
    assert plan.verify_config() == False

def test_owners_match_accounts():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions":2000,
        "type": "Roth",
        "withdrawl priority": 1,
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jill's Investment",
        "balance": 10000,
        "annual_additions": 5000,
        "type": "Investment",
        "withdrawl priority": 3,
        "owner": "Jill",
        "trail_with_rmd": False
    }))

    owners = []
    owners.append(Owner({
        "name": "Jill",
        "birth_year": 1977,
        "income": 2000,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))
    owners.append(Owner({
        "name": "Jerry",
        "birth_year": 1977,
        "income": 1000,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))

    expense_table = []
    expense_table.append(Expense({
        "name": "Travel",
        "need": False,
        "ammount": 2000,
        "starting_year": 2010,
        "frequency": 1
    }))
    expense_table.append(Expense({
        "name": "Car",
        "need": True,
        "ammount": 20000,
        "starting_year": 2007,
        "frequency": 5
    }))
    expenses = Expenses(expense_table)

    plan = Plan(owners, accounts, expenses, rmd, no_tax)
    assert plan.verify_config() == True

def test_expenses_can_be_empty():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions":2000,
        "type": "Roth",
        "withdrawl priority": 1,
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jill's Investment",
        "balance": 10000,
        "annual_additions": 5000,
        "type": "Investment",
        "withdrawl priority": 3,
        "owner": "Jill",
        "trail_with_rmd": False
    }))

    owners = []
    owners.append(Owner({
        "name": "Jill",
        "birth_year": 1977,
        "income": 2000,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))
    owners.append(Owner({
        "name": "Jerry",
        "birth_year": 1977,
        "income": 1000,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))
    empty_expense_table = []
    empty_expenses = Expenses(empty_expense_table)
    plan = Plan(owners, accounts, empty_expenses, rmd, no_tax)
    assert plan.process_plan(2022, 0, rates) == [[2022, 3000, 0, 0, 4000, 10000, 0, 14000]]

def test_account_growth_only_interest_when_owner_retired():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions":2000,
        "type": "Investment",
        "withdrawl priority": 1,
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    owners = []
    owners.append(Owner({
        "name": "Jerry",
        "birth_year": 1950,
        "income": 1000,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))
    empty_expense_table = []
    empty_expenses = Expenses(empty_expense_table)
    plan = Plan(owners, accounts, empty_expenses, rmd, no_tax)
    assert plan.process_plan(2015, 1, rates) == [[2015, 1000, 0, 0, 4000, 0, 4000], [2016, 0, 0, 0, 4240, 0, 4240]]

def test_calculates_rmds_of_accounts():
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions":2000,
        "type": "Roth",
        "withdrawl priority": 1,
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jerry's IRA",
        "balance": 8000,
        "annual_additions":2000,
        "type": "IRA",
        "withdrawl priority": 4,
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jill's Investment",
        "balance": 10000,
        "annual_additions": 5000,
        "type": "Investment",
        "withdrawl priority": 2,
        "owner": "Jill",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jill's 401k",
        "balance": 20000,
        "annual_additions": 5000,
        "type": "401K",
        "withdrawl priority": 3,
        "owner": "Jill",
        "trail_with_rmd": False
    }))
    owners = []
    owners.append(Owner({
        "name": "Jill",
        "birth_year": 1950,
        "income": 2000,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))
    owners.append(Owner({
        "name": "Jerry",
        "birth_year": 1949,
        "income": 1000,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))

    rmd_table = [
        {"rate": 10,
         "age": 65},
        {"rate": 12,
         "age": 66}
    ]
    rmd = Rmd(rmd_table)

    empty_expense_table = []
    empty_expenses = Expenses(empty_expense_table)
    plan = Plan(owners, accounts, empty_expenses, rmd, no_tax)
    assert plan.process_plan(2015, 0, rates) == [[2015, 2000, 2960, 0, 4000, 7040.0, 10000, 18000, 0, 39040.0]]

def test_calculates_rmds_of_accounts_several_years():
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions":2000,
        "type": "Roth",
        "withdrawl priority": 1,
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jerry's IRA",
        "balance": 8000,
        "annual_additions":2000,
        "type": "IRA",
        "withdrawl priority": 4,
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jill's Investment",
        "balance": 10000,
        "annual_additions": 5000,
        "type": "Investment",
        "withdrawl priority": 2,
        "owner": "Jill",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jill's 401k",
        "balance": 20000,
        "annual_additions": 5000,
        "type": "401K",
        "withdrawl priority": 3,
        "owner": "Jill",
        "trail_with_rmd": False
    }))
    owners = []
    owners.append(Owner({
        "name": "Jill",
        "birth_year": 1950,
        "income": 2000,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))
    owners.append(Owner({
        "name": "Jerry",
        "birth_year": 1949,
        "income": 1000,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))

    rmd_table = [
        {"rate": 10,
         "age": 65},
        {"rate": 12,
         "age": 66}
    ]
    rmd = Rmd(rmd_table)

    empty_expense_table = []
    empty_expenses = Expenses(empty_expense_table)
    plan = Plan(owners, accounts, empty_expenses, rmd, no_tax)
    assert plan.process_plan(2014, 1, rates) == [[2014, 3000, 800.0, 0, 4000, 7200.0, 10000, 20000.0, 0, 41200.0], [2015, 2000, 2864.0, 0, 4240.0, 6716.16, 15600, 24080.0, 0, 50636.16]]

def test_can_include_tax_on_account_growth():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions":2000,
        "type": "Roth",
        "withdrawl priority": 1,
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jerry's Investment",
        "balance": 10000,
        "annual_additions": 5000,
        "type": "Investment",
        "withdrawl priority": 3,
        "owner": "Jerry",
        "trail_with_rmd": False
    }))

    owners = []
    owners.append(Owner({
        "name": "Jerry",
        "birth_year": 1977,
        "income": 1000,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))

    tax_table = [
        {
            "max_tax_previous": 0,
            "rate": 10,
            "cutoff": 100000
        }
    ]
    tax = Tax(tax_table)
    expense_table = []
    expenses = Expenses(expense_table)

    plan = Plan(owners, accounts, expenses, rmd, tax)
    assert plan.process_plan(2022, 1, rates) == [[2022, 1000, 0, 0, 3940.0, 10000, 60.0, 13940.0], [2023, 1000, 0, 0, 6116.4, 15600.0, 60.0, 21716.4]]

def test_calculates_tax_including_rmds():
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions":2000,
        "type": "Roth",
        "withdrawl priority": 1,
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jerry's IRA",
        "balance": 8000,
        "annual_additions":2000,
        "type": "IRA",
        "withdrawl priority": 4,
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jill's Investment",
        "balance": 10000,
        "annual_additions": 5000,
        "type": "Investment",
        "withdrawl priority": 2,
        "owner": "Jill",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jill's 401k",
        "balance": 20000,
        "annual_additions": 5000,
        "type": "401K",
        "withdrawl priority": 3,
        "owner": "Jill",
        "trail_with_rmd": False
    }))
    owners = []
    owners.append(Owner({
        "name": "Jill",
        "birth_year": 1950,
        "income": 2000,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))
    owners.append(Owner({
        "name": "Jerry",
        "birth_year": 1949,
        "income": 1000,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))

    rmd_table = [
        {"rate": 10,
         "age": 65},
        {"rate": 12,
         "age": 66}
    ]
    rmd = Rmd(rmd_table)

    tax_table = [
        {
            "max_tax_previous": 0,
            "rate": 10,
            "cutoff": 100000
        }
    ]
    tax = Tax(tax_table)
    empty_expense_table = []
    empty_expenses = Expenses(empty_expense_table)
    plan = Plan(owners, accounts, empty_expenses, rmd, tax)
    assert plan.process_plan(2014, 1, rates) == [[2014, 3000, 800.0, 0, 3860.0, 7200.0, 10000, 20000.0, 140.0, 41060.0], [2015, 2000, 2864.0, 0, 3745.2, 6716.16, 15600.0, 24080.0, 346.4, 50141.36]]

def test_expenses_pulls_from_account():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "name": "Investment Priority 1",
        "balance": 4000,
        "annual_additions":2000,
        "type": "Investment",
        "withdrawl priority": 1,
        "owner": "Jerry",
        "trail_with_rmd": False
    }))

    owners = []
    owners.append(Owner({
        "name": "Jerry",
        "birth_year": 1977,
        "income": 0,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))

    tax_table = [
        {
            "max_tax_previous": 0,
            "rate": 10,
            "cutoff": 100000
        }
    ]
    tax = Tax(tax_table)
    expense_table = []
    expense_table.append(Expense({
        "name": "Travel",
        "need": True,
        "ammount": 1000,
        "starting_year": 2022,
        "frequency": 1
    }))
    expenses = Expenses(expense_table)

    plan = Plan(owners, accounts, expenses, rmd, tax)
    assert plan.process_plan(2022, 1, rates) == [[2022, 0, 0, 1000, 2976, 24.0, 2976], [2023, 0, 0, 1000, 4136.7, 17.86, 4136.7]]

@pytest.mark.skip()
def test_expenses_when_non_sufficient_pulls_from_next_account():
    assert True

@pytest.mark.skip()
def test_expenses_when_non_sufficient_pulls_from_next_account():
    assert True

@pytest.mark.skip()
def test_pulls_equally_from_all_accounts_at_same_priority():
    assert True

@pytest.mark.skip()
def test_pulls_plan_fails_when_no_money_left():
    assert True