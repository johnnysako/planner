from src.plan import Plan
from src.account import Account
from src.owner import Owner
from src.expense import Expense
from src.expenses import Expenses
from src.rmd import Rmd
from src.tax import Tax

empty_tax = [
    {
        "max_tax_previous": 0,
        "rate": 0,
        "cutoff": 22000
    }
]
no_tax = Tax(empty_tax)

rates = [6, 6, 6]

default_trial = {"social_security": True, "rmd": False}


def test_can_initialize_plan():
    rmd_table = []
    rmd = Rmd(rmd_table)

    accounts = []
    owners = []
    expense_table = []
    expenses = Expenses(expense_table)

    Plan(owners, accounts, expenses, rmd, no_tax, default_trial)


def test_can_get_header():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions": 2000,
        "type": "Investment",
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    owners = []
    expense_table = []
    expenses = Expenses(expense_table)

    plan = Plan(owners, accounts, expenses, rmd, no_tax, default_trial)
    assert plan.get_header() == ["Year", "Income", "Rmd", "Expenses",
                                 "Taxes", "Reinvested", "Jerry's Roth", "% Withdrawn", "Sum of Accounts"]


def test_can_fill_table_for_one_year():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions": 2000,
        "type": "Roth",
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jill's Investment",
        "balance": 10000,
        "annual_additions": 5000,
        "type": "Investment",
        "owner": "Jill",
        "trail_with_rmd": False
    }))

    owners = []
    owners.append(Owner({
        "name": "Jill",
        "birth_year": 1977,
        "income": 0,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))
    owners.append(Owner({
        "name": "Jerry",
        "birth_year": 1977,
        "income": 0,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))

    expense_table = []
    expense_table.append(Expense({
        "name": "Travel",
        "need": False,
        "amount": 2000,
        "starting_year": 2010,
        "frequency": 1
    }))
    expense_table.append(Expense({
        "name": "Car",
        "need": True,
        "amount": 200,
        "starting_year": 2007,
        "frequency": 5
    }))
    expenses = Expenses(expense_table)

    plan = Plan(owners, accounts, expenses, rmd, no_tax, default_trial)
    assert plan.process_plan(2022, 0, rates) == \
        [[2022, 0, 0, 2200, 0.0, 0.0, 1800.0, 10000, 18.64, 11800.0]]


def test_can_fill_table_for_two_years():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions": 2000,
        "type": "Roth",
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jill's Investment",
        "balance": 10000,
        "annual_additions": 5000,
        "type": "Investment",
        "owner": "Jill",
        "trail_with_rmd": False
    }))

    owners = []
    owners.append(Owner({
        "name": "Jill",
        "birth_year": 1977,
        "income": 0,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))
    owners.append(Owner({
        "name": "Jerry",
        "birth_year": 1977,
        "income": 0,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))

    expense_table = []
    expense_table.append(Expense({
        "name": "Travel",
        "need": False,
        "amount": 2000,
        "starting_year": 2010,
        "frequency": 1
    }))
    expense_table.append(Expense({
        "name": "Car",
        "need": True,
        "amount": 200,
        "starting_year": 2007,
        "frequency": 5
    }))
    expenses = Expenses(expense_table)

    plan = Plan(owners, accounts, expenses, rmd, no_tax, default_trial)
    assert plan.process_plan(2022, 1, rates) == \
        [[2022, 0, 0, 2200, 0.0, 0.0, 1800.0, 10000, 18.64, 11800.0],
         [2023, 0, 0, 2000, 0.0, 0.0, 1908.0, 15600.0, 11.42, 17508.0]]


def test_owners_do_not_match_accounts():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions": 2000,
        "type": "Roth",
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
    plan = Plan(bad_owners, accounts, expenses, rmd, no_tax, default_trial)
    assert plan.verify_config() is False


def test_owners_match_accounts():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions": 2000,
        "type": "Roth",
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jill's Investment",
        "balance": 10000,
        "annual_additions": 5000,
        "type": "Investment",
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
        "amount": 2000,
        "starting_year": 2010,
        "frequency": 1
    }))
    expense_table.append(Expense({
        "name": "Car",
        "need": True,
        "amount": 20000,
        "starting_year": 2007,
        "frequency": 5
    }))
    expenses = Expenses(expense_table)

    plan = Plan(owners, accounts, expenses, rmd, no_tax, default_trial)
    assert plan.verify_config() is True


def test_expenses_can_be_empty():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions": 2000,
        "type": "Roth",
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jill's Investment",
        "balance": 10000,
        "annual_additions": 5000,
        "type": "Investment",
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
    plan = Plan(owners, accounts, empty_expenses, rmd, no_tax, default_trial)
    assert plan.process_plan(2022, 0, rates) == \
        [[2022, 3000, 0, 0, 0.0, 3000.0, 7000.0, 10000, -17.65, 17000.0]]


def test_account_growth_only_interest_when_owner_retired():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions": 2000,
        "type": "Investment",
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
    plan = Plan(owners, accounts, empty_expenses, rmd, no_tax, default_trial)
    assert plan.process_plan(2015, 1, rates) == \
        [[2015, 1000, 0, 0, 0.0, 1000.0, 5000.0, -20.0, 5000.0],
         [2016, 0, 0, 0, 0.0, 0.0, 5300.0, 0.0, 5300.0]]


def test_calculates_rmds_of_accounts():
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions": 2000,
        "type": "Roth",
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jerry's IRA",
        "balance": 8000,
        "annual_additions": 2000,
        "type": "IRA",
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jill's Investment",
        "balance": 10000,
        "annual_additions": 5000,
        "type": "Investment",
        "owner": "Jill",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jill's 401k",
        "balance": 20000,
        "annual_additions": 5000,
        "type": "401K",
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
    plan = Plan(owners, accounts, empty_expenses, rmd, no_tax, default_trial)
    assert plan.process_plan(2015, 0, rates) == \
        [[2015, 2000, 2666.67, 0, 0.0, 4666.67, 8666.67, 7333.33, 10000, 18000.0, -10.61, 44000.0]]


def test_calculates_rmds_of_accounts_several_years():
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions": 2000,
        "type": "Roth",
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jerry's IRA",
        "balance": 8000,
        "annual_additions": 2000,
        "type": "IRA",
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jill's Investment",
        "balance": 10000,
        "annual_additions": 5000,
        "type": "Investment",
        "owner": "Jill",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jill's 401k",
        "balance": 20000,
        "annual_additions": 5000,
        "type": "401K",
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
    plan = Plan(owners, accounts, empty_expenses, rmd, no_tax, default_trial)
    assert plan.process_plan(2014, 1, rates) == \
        [[2014, 3000, 800.0, 0, 0.0, 3800.0, 7800.0, 7200.0, 10000, 20000, -8.44, 45000.0],
         [2015, 2000, 2600.0, 0, 0.0, 4600.0, 12868.0, 6996.0, 15600.0, 24080.0, -7.73, 59544.0]]


def test_can_include_tax_on_account_growth():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions": 2000,
        "type": "Roth",
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jerry's Investment",
        "balance": 10000,
        "annual_additions": 5000,
        "type": "Investment",
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
    expenses = Expenses(expense_table)

    plan = Plan(owners, accounts, expenses, rmd, tax, default_trial)
    assert plan.process_plan(2022, 1, rates) == \
        [[2022, 0, 0, 0, 60.0, 0.0, 3940.0, 10000, 0.43, 13940.0],
         [2023, 0, 0, 0, 60.0, 0.0, 6116.4, 15600.0, 0.28, 21716.4]]


def test_no_tax_on_negative_growth():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions": 2000,
        "type": "Roth",
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jerry's Investment",
        "balance": 10000,
        "annual_additions": 5000,
        "type": "Investment",
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

    negative_growth = [-1, -1]

    plan = Plan(owners, accounts, expenses, rmd, tax, default_trial)
    assert plan.process_plan(2022, 1, negative_growth) == \
        [[2022, 1000, 0, 0, 0.0, 1000.0, 5000.0, 10000, -6.67, 15000.0],
         [2023, 1000, 0, 0, 0.0, 1000.0, 7950.0, 14900.0, -4.38, 22850.0]]


def test_calculates_tax_including_rmds():
    accounts = []
    accounts.append(Account({
        "name": "Jerry's Roth",
        "balance": 4000,
        "annual_additions": 2000,
        "type": "Roth",
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jerry's IRA",
        "balance": 8000,
        "annual_additions": 2000,
        "type": "IRA",
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jill's Investment",
        "balance": 10000,
        "annual_additions": 5000,
        "type": "Investment",
        "owner": "Jill",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jill's 401k",
        "balance": 20000,
        "annual_additions": 5000,
        "type": "401K",
        "owner": "Jill",
        "trail_with_rmd": False
    }))
    owners = []
    owners.append(Owner({
        "name": "Jill",
        "birth_year": 1950,
        "income": 0,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))
    owners.append(Owner({
        "name": "Jerry",
        "birth_year": 1949,
        "income": 0,
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
    plan = Plan(owners, accounts, empty_expenses, rmd, tax, default_trial)
    assert plan.process_plan(2014, 1, rates) == \
        [[2014, 0, 800.0, 0, 140.0, 660.0, 4660.0, 7200.0, 10000, 20000, -1.58, 41860.0],
         [2015, 0, 2600.0, 0, 320.0, 2280.0, 7219.6, 6996.0, 15600.0, 24080.0, -4.23, 53895.6]]


def test_expenses_pulls_from_account():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "name": "Investment Priority 1",
        "balance": 4000,
        "annual_additions": 2000,
        "type": "Investment",
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
        "amount": 1000,
        "starting_year": 2022,
        "frequency": 1
    }))
    expenses = Expenses(expense_table)

    plan = Plan(owners, accounts, expenses, rmd, tax, default_trial)
    assert plan.process_plan(2022, 1, rates) == \
        [[2022, 0, 0, 1000, 24.0, 0.0, 2976.0, 34.41, 2976.0],
         [2023, 0, 0, 1000, 17.86, 0.0, 4136.7, 24.61, 4136.7]]


def test_expenses_pulls_from_income():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "name": "Investment Priority 1",
        "balance": 4000,
        "annual_additions": 2000,
        "type": "Investment",
        "owner": "Jerry",
        "trail_with_rmd": False
    }))

    owners = []
    owners.append(Owner({
        "name": "Jerry",
        "birth_year": 1977,
        "income": 10000,
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
        "amount": 1000,
        "starting_year": 2022,
        "frequency": 1
    }))
    expenses = Expenses(expense_table)

    plan = Plan(owners, accounts, expenses, rmd, tax, default_trial)
    assert plan.process_plan(2022, 1, rates) == \
        [[2022, 10000, 0, 1000, 24.0, 8976.0, 12976.0, -69.17, 12976.0],
         [2023, 10000, 0, 1000, 77.86, 8922.14, 24676.7, -36.16, 24676.7]]


def test_expenses_when_non_sufficient_pulls_from_next_account():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "name": "Investment Priority 1",
        "balance": 4000,
        "annual_additions": 2000,
        "type": "Investment",
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Investment Priority 2",
        "balance": 10000,
        "annual_additions": 2000,
        "type": "Investment",
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
        "amount": 5000,
        "starting_year": 2022,
        "frequency": 1
    }))
    expenses = Expenses(expense_table)

    plan = Plan(owners, accounts, expenses, rmd, tax, default_trial)
    assert plan.process_plan(2022, 1, rates) == \
        [[2022, 0, 0, 5000, 84.0, 0.0, 0, 8916.0, 57.02, 8916.0],
         [2023, 0, 0, 5000, 53.5, 0.0, 0.0, 8397.46, 60.18, 8397.46]]


def test_pulls_plan_fails_when_no_money_left():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "name": "Investment Priority 1",
        "balance": 4000,
        "annual_additions": 0,
        "type": "Investment",
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Investment Priority 2",
        "balance": 10000,
        "annual_additions": 1000,
        "type": "Investment",
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
        "amount": 6000,
        "starting_year": 2022,
        "frequency": 1
    }))
    expenses = Expenses(expense_table)

    plan = Plan(owners, accounts, expenses, rmd, tax, default_trial)
    assert plan.process_plan(2022, 2, rates) == \
        [[2022, 0, 0, 6000, 84.0, 0.0, 0, 7916.0, 76.86, 7916.0],
         [2023, 0, 0, 6000, 47.5, 0.0, 0.0, 3343.46, 180.88, 3343.46],
         [2024, 0, 0, 6000, 20.06, 0.0, 0.0, 0.0, 0, 0.0]]


def test_pulls_rmd_can_cover_expense_and_tax():
    accounts = []
    accounts.append(Account({
        "name": "Jerry's IRA",
        "balance": 8000,
        "annual_additions": 0,
        "type": "IRA",
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jerry's 401k",
        "balance": 20000,
        "annual_additions": 0,
        "type": "401K",
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    owners = []
    owners.append(Owner({
        "name": "Jerry",
        "birth_year": 1949,
        "income": 0,
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

    expense_table = []
    expense_table.append(Expense({
        "name": "Travel",
        "need": True,
        "amount": 500,
        "starting_year": 2022,
        "frequency": 1
    }))
    expenses = Expenses(expense_table)

    plan = Plan(owners, accounts, expenses, rmd, tax, default_trial)
    assert plan.process_plan(2014, 1, rates) == \
        [[2014, 0, 2800.0, 0, 280.0, 2520.0, 9720.0, 18000.0, -9.09, 27720.0],
         [2015, 0, 2310.0, 0, 231.0, 2079.0, 11523.6, 17490.0, -7.17, 29013.6]]


def test_does_not_include_social_security_when_config():
    accounts = []
    accounts.append(Account({
        "name": "Jerry's IRA",
        "balance": 8000,
        "annual_additions": 0,
        "type": "IRA",
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    accounts.append(Account({
        "name": "Jerry's 401k",
        "balance": 20000,
        "annual_additions": 0,
        "type": "401K",
        "owner": "Jerry",
        "trail_with_rmd": False
    }))
    owners = []
    owners.append(Owner({
        "name": "Jerry",
        "birth_year": 1949,
        "income": 0,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 65
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

    expense_table = []
    expense_table.append(Expense({
        "name": "Travel",
        "need": True,
        "amount": 500,
        "starting_year": 2022,
        "frequency": 1
    }))
    expenses = Expenses(expense_table)

    trial = {"social_security": False, "rmd": False}

    plan = Plan(owners, accounts, expenses, rmd, tax, trial)
    assert plan.process_plan(2014, 1, rates) == \
        [[2014, 0, 2800.0, 0, 280.0, 2520.0, 9720.0, 18000.0, -9.09, 27720.0],
         [2015, 0, 2310.0, 0, 231.0, 2079.0, 11523.6, 17490.0, -7.17, 29013.6]]


def test_roth_has_rmd_when_config():
    accounts = []
    accounts.append(Account({
        "name": "Jerry's IRA",
        "balance": 8000,
        "annual_additions": 0,
        "type": "Roth",
        "owner": "Jerry",
        "trail_with_rmd": True
    }))
    owners = []
    owners.append(Owner({
        "name": "Jerry",
        "birth_year": 1949,
        "income": 0,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 65
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

    expense_table = []
    expense_table.append(Expense({
        "name": "Travel",
        "need": True,
        "amount": 500,
        "starting_year": 2022,
        "frequency": 1
    }))
    expenses = Expenses(expense_table)

    trial = {"social_security": False, "rmd": True}

    plan = Plan(owners, accounts, expenses, rmd, tax, trial)
    assert plan.process_plan(2014, 1, rates) == \
        [[2014, 0, 800.0, 0, 80.0, 720.0, 7920.0, -9.09, 7920.0],
         [2015, 0, 660.0, 0, 66.0, 594.0, 8289.6, -7.17, 8289.6]]
