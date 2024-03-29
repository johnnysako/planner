from src.plan import Plan
from src.account import Account
from src.owner import Owner
from src.expense import Expense
from src.expenses import Expenses
from src.rmd import Rmd
from src.tax import Tax

empty_tax = {
    "single": [{
        "max_tax_previous": 0,
        "rate": 0,
        "cutoff": None
    }]
}
no_tax = Tax(empty_tax)

rates = {"s": [6, 6, 6], "b": [3, 3, 3]}

default_trial = {"Social Security": True, "rmd": False, "bad_timing": False}


def test_can_initialize_plan():
    rmd_table = []
    rmd = Rmd(rmd_table)

    accounts = []
    owners = []
    expense_table = []
    expenses = Expenses(expense_table)

    Plan(2076, owners, accounts, expenses, rmd, no_tax, default_trial)


def test_can_get_header():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "Name": "Jerry Roth",
        "Balance": 4000,
        "Annual Additions": 2000,
        "Type": "Investment",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))
    owners = []
    expense_table = []
    expenses = Expenses(expense_table)

    plan = Plan(2076, owners, accounts, expenses, rmd, no_tax, default_trial)
    assert plan.get_header() == ['Year', 'Stock Returns', 'Bond Returns',
                                 'Income', 'Rmd', 'Expenses', 'Taxes',
                                 'Reinvested', 'Jerry Roth', '% Withdrawn',
                                 'Sum of Accounts']


def test_can_fill_table_for_one_year():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "Name": "Jerry's Roth",
        "Balance": 4000,
        "Annual Additions": 2000,
        "Type": "Roth",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))
    accounts.append(Account({
        "Name": "Jill's Investment",
        "Balance": 10000,
        "Annual Additions": 5000,
        "Type": "Investment",
        "Owner Name": "Jill",
        "Test as Tax Deferred": False
    }))

    owners = []
    owners.append(Owner({
        "Name": "Jill",
        "Year of Birth": 1977,
        "Pre-retirement Take Home Pay": 0,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
    }))
    owners.append(Owner({
        "Name": "Jerry",
        "Year of Birth": 1977,
        "Pre-retirement Take Home Pay": 0,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
    }))

    expense_table = []
    expense_table.append(Expense({
        "Name": "Travel",
        "Cost": 2000,
        "Year Starts": 2010,
        "Every x Year(s)": 1
    }))
    expense_table.append(Expense({
        "Name": "Car",
        "Cost": 200,
        "Year Starts": 2007,
        "Every x Year(s)": 5
    }))
    expenses = Expenses(expense_table)

    plan = Plan(2022, owners, accounts, expenses, rmd, no_tax, default_trial)
    assert plan.process_plan(0, rates) == \
        [[2022, 6, 3, 0, 0, 2200, 0.0, 0.0, 1800.0, 10000, 18.64, 11800.0]]


def test_can_fill_table_for_two_years():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "Name": "Jerry's Roth",
        "Balance": 4000,
        "Annual Additions": 2000,
        "Type": "Roth",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))
    accounts.append(Account({
        "Name": "Jill's Investment",
        "Balance": 10000,
        "Annual Additions": 5000,
        "Type": "Investment",
        "Owner Name": "Jill",
        "Test as Tax Deferred": False
    }))

    owners = []
    owners.append(Owner({
        "Name": "Jill",
        "Year of Birth": 1977,
        "Pre-retirement Take Home Pay": 0,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
    }))
    owners.append(Owner({
        "Name": "Jerry",
        "Year of Birth": 1977,
        "Pre-retirement Take Home Pay": 0,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
    }))

    expense_table = []
    expense_table.append(Expense({
        "Name": "Travel",
        "Cost": 2000,
        "Year Starts": 2010,
        "Every x Year(s)": 1
    }))
    expense_table.append(Expense({
        "Name": "Car",
        "Cost": 200,
        "Year Starts": 2007,
        "Every x Year(s)": 5
    }))
    expenses = Expenses(expense_table)

    plan = Plan(2022, owners, accounts, expenses, rmd, no_tax, default_trial)
    assert plan.process_plan(1, rates) == \
        [[2022, 6, 3, 0, 0, 2200, 0.0, 0.0, 1800.0, 10000, 18.64, 11800.0],
         [2023, 6, 3, 0, 0, 2000, 0.0, 0.0, 1908.0, 15600.0, 11.42, 17508.0]]


def test_owners_do_not_match_accounts():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "Name": "Jerry's Roth",
        "Balance": 4000,
        "Annual Additions": 2000,
        "Type": "Roth",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))

    bad_owners = []
    bad_owners.append(Owner({
        "Name": "Babs",
        "Year of Birth": 1977,
        "Pre-retirement Take Home Pay": 56789,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
    }))

    expense_table = []
    expenses = Expenses(expense_table)
    plan = Plan(2076, bad_owners, accounts, expenses, rmd, no_tax, default_trial)
    assert plan.verify_config() is False


def test_owners_match_accounts():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "Name": "Jerry's Roth",
        "Balance": 4000,
        "Annual Additions": 2000,
        "Type": "Roth",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))
    accounts.append(Account({
        "Name": "Jill's Investment",
        "Balance": 10000,
        "Annual Additions": 5000,
        "Type": "Investment",
        "Owner Name": "Jill",
        "Test as Tax Deferred": False
    }))

    owners = []
    owners.append(Owner({
        "Name": "Jill",
        "Year of Birth": 1977,
        "Pre-retirement Take Home Pay": 2000,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
    }))
    owners.append(Owner({
        "Name": "Jerry",
        "Year of Birth": 1977,
        "Pre-retirement Take Home Pay": 1000,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
    }))

    expense_table = []
    expense_table.append(Expense({
        "Name": "Travel",
        "Cost": 2000,
        "Year Starts": 2010,
        "Every x Year(s)": 1
    }))
    expense_table.append(Expense({
        "Name": "Car",
        "Cost": 20000,
        "Year Starts": 2007,
        "Every x Year(s)": 5
    }))
    expenses = Expenses(expense_table)

    plan = Plan(2076, owners, accounts, expenses, rmd, no_tax, default_trial)
    assert plan.verify_config() is True


def test_expenses_can_be_empty():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "Name": "Jerry's Roth",
        "Balance": 4000,
        "Annual Additions": 2000,
        "Type": "Roth",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))
    accounts.append(Account({
        "Name": "Jill's Investment",
        "Balance": 10000,
        "Annual Additions": 5000,
        "Type": "Investment",
        "Owner Name": "Jill",
        "Test as Tax Deferred": False
    }))

    owners = []
    owners.append(Owner({
        "Name": "Jill",
        "Year of Birth": 1977,
        "Pre-retirement Take Home Pay": 2000,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
    }))
    owners.append(Owner({
        "Name": "Jerry",
        "Year of Birth": 1977,
        "Pre-retirement Take Home Pay": 1000,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
    }))
    empty_expense_table = []
    empty_expenses = Expenses(empty_expense_table)
    plan = Plan(2022, owners, accounts, empty_expenses, rmd, no_tax,
                default_trial)
    assert plan.process_plan(0, rates) == \
        [[2022, 6, 3, 3000, 0, 0, 0.0, 3000.0, 7000.0, 10000, 0.0, 17000.0]]


def test_account_growth_only_interest_when_owner_retired():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "Name": "Jerry's Roth",
        "Balance": 4000,
        "Annual Additions": 2000,
        "Type": "Investment",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))
    owners = []
    owners.append(Owner({
        "Name": "Jerry",
        "Year of Birth": 1950,
        "Pre-retirement Take Home Pay": 1000,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70,
        "Tax Status": "single"
    }))
    empty_expense_table = []
    empty_expenses = Expenses(empty_expense_table)
    plan = Plan(2015, owners, accounts, empty_expenses, rmd, no_tax, default_trial)
    assert plan.process_plan(1, rates) == \
        [[2015, 6, 3, 1000, 0, 0, 0.0, 1000.0, 5000.0, 0.0, 5000.0],
         [2016, 6, 3, 0, 0, 0, 0.0, 0.0, 5300.0, 0.0, 5300.0]]


def test_calculates_rmds_of_accounts():
    accounts = []
    accounts.append(Account({
        "Name": "Jerry's Roth",
        "Balance": 4000,
        "Annual Additions": 2000,
        "Type": "Roth",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))
    accounts.append(Account({
        "Name": "Jerry's IRA",
        "Balance": 8000,
        "Annual Additions": 2000,
        "Type": "IRA",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))
    accounts.append(Account({
        "Name": "Jill's Investment",
        "Balance": 10000,
        "Annual Additions": 5000,
        "Type": "Investment",
        "Owner Name": "Jill",
        "Test as Tax Deferred": False
    }))
    accounts.append(Account({
        "Name": "Jill's 401k",
        "Balance": 20000,
        "Annual Additions": 5000,
        "Type": "401K",
        "Owner Name": "Jill",
        "Test as Tax Deferred": False
    }))
    owners = []
    owners.append(Owner({
        "Name": "Jill",
        "Year of Birth": 1950,
        "Pre-retirement Take Home Pay": 2000,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
    }))
    owners.append(Owner({
        "Name": "Jerry",
        "Year of Birth": 1949,
        "Pre-retirement Take Home Pay": 1000,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
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
    plan = Plan(2015, owners, accounts, empty_expenses, rmd, no_tax, default_trial)
    assert plan.process_plan(0, rates) == \
        [[2015, 6, 3, 2000, 2666.67, 0, 0.0, 4666.67, 8666.67,
            7333.33, 10000, 18000.0, 0.0, 44000.0]]


def test_calculates_rmds_of_accounts_several_years():
    accounts = []
    accounts.append(Account({
        "Name": "Jerry's Roth",
        "Balance": 4000,
        "Annual Additions": 2000,
        "Type": "Roth",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))
    accounts.append(Account({
        "Name": "Jerry's IRA",
        "Balance": 8000,
        "Annual Additions": 2000,
        "Type": "IRA",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))
    accounts.append(Account({
        "Name": "Jill's Investment",
        "Balance": 10000,
        "Annual Additions": 5000,
        "Type": "Investment",
        "Owner Name": "Jill",
        "Test as Tax Deferred": False
    }))
    accounts.append(Account({
        "Name": "Jill's 401k",
        "Balance": 20000,
        "Annual Additions": 5000,
        "Type": "401K",
        "Owner Name": "Jill",
        "Test as Tax Deferred": False
    }))
    owners = []
    owners.append(Owner({
        "Name": "Jill",
        "Year of Birth": 1950,
        "Pre-retirement Take Home Pay": 2000,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
    }))
    owners.append(Owner({
        "Name": "Jerry",
        "Year of Birth": 1949,
        "Pre-retirement Take Home Pay": 1000,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
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
    plan = Plan(2014, owners, accounts, empty_expenses, rmd, no_tax, default_trial)
    assert plan.process_plan(1, rates) == \
        [[2014, 6, 3, 3000, 800.0, 0, 0.0, 3800.0, 7800.0, 7200.0, 10000, 20000, 0.0, 45000.0],
         [2015, 6, 3, 2000, 2600.0, 0, 0.0, 4600.0, 12868.0, 6996.0, 15600.0, 24080.0, 0.0, 59544.0]]


def test_can_include_tax_on_account_growth():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "Name": "Jerry's Roth",
        "Balance": 4000,
        "Annual Additions": 2000,
        "Type": "Roth",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))
    accounts.append(Account({
        "Name": "Jerry's Investment",
        "Balance": 10000,
        "Annual Additions": 5000,
        "Type": "Investment",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))

    owners = []
    owners.append(Owner({
        "Name": "Jerry",
        "Year of Birth": 1977,
        "Pre-retirement Take Home Pay": 0,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
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

    plan = Plan(2022, owners, accounts, expenses, rmd, tax, default_trial)
    assert plan.process_plan(1, rates) == \
        [[2022, 6, 3, 0, 0, 0, 0, 0.0, 4000, 10000, 0.0, 14000],
         [2023, 6, 3, 0, 0, 0, 0, 0.0, 6240.0, 15600.0, 0.0, 21840.0]]


def test_no_tax_on_negative_growth():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "Name": "Jerry's Roth",
        "Balance": 4000,
        "Annual Additions": 2000,
        "Type": "Roth",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))
    accounts.append(Account({
        "Name": "Jerry's Investment",
        "Balance": 10000,
        "Annual Additions": 5000,
        "Type": "Investment",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))

    owners = []
    owners.append(Owner({
        "Name": "Jerry",
        "Year of Birth": 1977,
        "Pre-retirement Take Home Pay": 1000,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
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

    negative_growth = {"s": [-1, -1], "b": [0, 0]}

    plan = Plan(2022, owners, accounts, expenses, rmd, tax, default_trial)
    assert plan.process_plan(1, negative_growth) == \
        [[2022, -1, 0, 1000, 0, 0, 0.0, 1000.0, 5000.0, 10000, 0.0, 15000.0],
         [2023, -1, 0, 1000, 0, 0, 0.0, 1000.0, 7950.0, 14900.0, 0.0, 22850.0]]


def test_calculates_tax_including_rmds():
    accounts = []
    accounts.append(Account({
        "Name": "Jerry's Roth",
        "Balance": 4000,
        "Annual Additions": 2000,
        "Type": "Roth",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))
    accounts.append(Account({
        "Name": "Jerry's IRA",
        "Balance": 8000,
        "Annual Additions": 2000,
        "Type": "IRA",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))
    accounts.append(Account({
        "Name": "Jill's Investment",
        "Balance": 10000,
        "Annual Additions": 5000,
        "Type": "Investment",
        "Owner Name": "Jill",
        "Test as Tax Deferred": False
    }))
    accounts.append(Account({
        "Name": "Jill's 401k",
        "Balance": 20000,
        "Annual Additions": 5000,
        "Type": "401K",
        "Owner Name": "Jill",
        "Test as Tax Deferred": False
    }))
    owners = []
    owners.append(Owner({
        "Name": "Jill",
        "Year of Birth": 1950,
        "Pre-retirement Take Home Pay": 0,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
    }))
    owners.append(Owner({
        "Name": "Jerry",
        "Year of Birth": 1949,
        "Pre-retirement Take Home Pay": 0,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
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
    plan = Plan(2014, owners, accounts, empty_expenses, rmd, tax, default_trial)
    assert plan.process_plan(1, rates) == \
        [[2014, 6, 3, 0, 800.0, 0, 0, 800.0, 4800.0, 7200.0, 10000, 20000, 0.0, 42000.0],
         [2015, 6, 3, 0, 2600.0, 0, 0, 2600.0, 7688.0, 6996.0, 15600.0, 24080.0, 0.0, 54364.0]]


def test_expenses_pulls_from_account():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "Name": "Investment Priority 1",
        "Balance": 4000,
        "Annual Additions": 2000,
        "Type": "Investment",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))

    owners = []
    owners.append(Owner({
        "Name": "Jerry",
        "Year of Birth": 1977,
        "Pre-retirement Take Home Pay": 0,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
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
        "Name": "Travel",
        "Cost": 1000,
        "Year Starts": 2022,
        "Every x Year(s)": 1
    }))
    expenses = Expenses(expense_table)

    plan = Plan(2022, owners, accounts, expenses, rmd, tax, default_trial)
    assert plan.process_plan(1, rates) == \
        [[2022, 6, 3, 0, 0, 1000, 0, 0.0, 3000, 33.33, 3000],
         [2023, 6, 3, 0, 0, 1000, 0, 0.0, 4180.0, 23.92, 4180.0]]


def test_expenses_pulls_from_income():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "Name": "Investment Priority 1",
        "Balance": 4000,
        "Annual Additions": 2000,
        "Type": "Investment",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))

    owners = []
    owners.append(Owner({
        "Name": "Jerry",
        "Year of Birth": 1977,
        "Pre-retirement Take Home Pay": 10000,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
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
        "Name": "Travel",
        "Cost": 1000,
        "Year Starts": 2022,
        "Every x Year(s)": 1
    }))
    expenses = Expenses(expense_table)

    plan = Plan(2022, owners, accounts, expenses, rmd, tax, default_trial)
    assert plan.process_plan(1, rates) == \
        [[2022, 6, 3, 10000, 0, 1000, 0, 9000, 13000, 0.0, 13000],
         [2023, 6, 3, 10000, 0, 1000, 0, 9000, 24780.0, 0.0, 24780.0]]


def test_expenses_when_non_sufficient_pulls_from_next_account():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "Name": "Investment Priority 1",
        "Balance": 4000,
        "Annual Additions": 2000,
        "Type": "Investment",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))
    accounts.append(Account({
        "Name": "Investment Priority 2",
        "Balance": 10000,
        "Annual Additions": 2000,
        "Type": "Investment",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))

    owners = []
    owners.append(Owner({
        "Name": "Jerry",
        "Year of Birth": 1977,
        "Pre-retirement Take Home Pay": 0,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
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
        "Name": "Travel",
        "Cost": 5000,
        "Year Starts": 2022,
        "Every x Year(s)": 1
    }))
    expenses = Expenses(expense_table)

    plan = Plan(2022, owners, accounts, expenses, rmd, tax, default_trial)
    assert plan.process_plan(1, rates) == \
        [[2022, 6, 3, 0, 0, 5000, 0, 0.0, 0, 9000, 55.56, 9000],
         [2023, 6, 3, 0, 0, 5000, 0, 0.0, 0.0, 8540.0, 58.55, 8540.0]]


def test_pulls_plan_fails_when_no_money_left():
    rmd_table = []
    rmd = Rmd(rmd_table)
    accounts = []
    accounts.append(Account({
        "Name": "Investment Priority 1",
        "Balance": 4000,
        "Annual Additions": 0,
        "Type": "Investment",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))
    accounts.append(Account({
        "Name": "Investment Priority 2",
        "Balance": 10000,
        "Annual Additions": 1000,
        "Type": "Investment",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))

    owners = []
    owners.append(Owner({
        "Name": "Jerry",
        "Year of Birth": 1977,
        "Pre-retirement Take Home Pay": 0,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
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
        "Name": "Travel",
        "Cost": 6000,
        "Year Starts": 2022,
        "Every x Year(s)": 1
    }))
    expenses = Expenses(expense_table)

    plan = Plan(2022, owners, accounts, expenses, rmd, tax, default_trial)
    assert plan.process_plan(2, rates) == \
        [[2022, 6, 3, 0, 0, 6000, 0, 0.0, 0, 8000, 75.0, 8000],
         [2023, 6, 3, 0, 0, 6000, 0, 0.0, 0.0, 3480.0, 172.41, 3480.0],
         [2024, 6, 3, 0, 0, 6000, 0, 0.0, 0.0, 0.0, 0.0, 0.0]]


def test_pulls_rmd_can_cover_expense_and_tax():
    accounts = []
    accounts.append(Account({
        "Name": "Jerry's IRA",
        "Balance": 8000,
        "Annual Additions": 0,
        "Type": "IRA",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))
    accounts.append(Account({
        "Name": "Jerry's 401k",
        "Balance": 20000,
        "Annual Additions": 0,
        "Type": "401K",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))
    owners = []
    owners.append(Owner({
        "Name": "Jerry",
        "Year of Birth": 1949,
        "Pre-retirement Take Home Pay": 0,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70,
        "Tax Status": "single"
    }))

    rmd_table = [
        {"rate": 10,
         "age": 65},
        {"rate": 12,
         "age": 66}
    ]
    rmd = Rmd(rmd_table)

    tax_table = {
        "single": [{
            "max_tax_previous": 0,
            "rate": 10,
            "cutoff": 100000
        }]
    }
    tax = Tax(tax_table)

    expense_table = []
    expense_table.append(Expense({
        "Name": "Travel",
        "Cost": 500,
        "Year Starts": 2022,
        "Every x Year(s)": 1
    }))
    expenses = Expenses(expense_table)

    plan = Plan(2014, owners, accounts, expenses, rmd, tax, default_trial)
    assert plan.process_plan(1, rates) == \
        [[2014, 6, 3, 0, 2800.0, 0, 0, 2800.0, 10000.0, 18000.0, 0.0, 28000.0],
         [2015, 6, 3, 0, 2333.33, 0, 233.33, 0.0, 9716.67, 17490.0, 0.0, 27206.67]]


def test_does_not_include_social_security_when_config():
    accounts = []
    accounts.append(Account({
        "Name": "Jerry's IRA",
        "Balance": 8000,
        "Annual Additions": 0,
        "Type": "IRA",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))
    accounts.append(Account({
        "Name": "Jerry's 401k",
        "Balance": 20000,
        "Annual Additions": 0,
        "Type": "401K",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": False
    }))
    owners = []
    owners.append(Owner({
        "Name": "Jerry",
        "Year of Birth": 1949,
        "Pre-retirement Take Home Pay": 0,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 65,
        "Tax Status": "single"
    }))

    rmd_table = [
        {"rate": 10,
         "age": 65},
        {"rate": 12,
         "age": 66}
    ]
    rmd = Rmd(rmd_table)

    tax_table = {
        "single": [{
            "max_tax_previous": 0,
            "rate": 10,
            "cutoff": 100000
        }]
    }
    tax = Tax(tax_table)

    expense_table = []
    expense_table.append(Expense({
        "Name": "Travel",
        "Cost": 500,
        "Year Starts": 2022,
        "Every x Year(s)": 1
    }))
    expenses = Expenses(expense_table)

    trial = {"Social Security": False, "rmd": False, "bad_timing": False}

    plan = Plan(2014, owners, accounts, expenses, rmd, tax, trial)
    assert plan.process_plan(1, rates) == \
        [[2014, 6, 3, 0, 2800.0, 0, 0, 2800.0, 10000.0, 18000.0, 0.0, 28000.0],
         [2015, 6, 3, 0, 2333.33, 0, 233.33, 0.0, 9716.67, 17490.0, 0.0, 27206.67]]


def test_roth_has_rmd_when_config():
    accounts = []
    accounts.append(Account({
        "Name": "Jerry's IRA",
        "Balance": 8000,
        "Annual Additions": 0,
        "Type": "Roth",
        "Owner Name": "Jerry",
        "Test as Tax Deferred": True
    }))
    owners = []
    owners.append(Owner({
        "Name": "Jerry",
        "Year of Birth": 1949,
        "Pre-retirement Take Home Pay": 0,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 65,
        "Tax Status": "single"
    }))

    rmd_table = [
        {"rate": 10,
         "age": 65},
        {"rate": 12,
         "age": 66}
    ]
    rmd = Rmd(rmd_table)

    tax_table = {
        "single": [{
            "max_tax_previous": 0,
            "rate": 10,
            "cutoff": 100000
        }]
    }
    tax = Tax(tax_table)

    expense_table = []
    expense_table.append(Expense({
        "Name": "Travel",
        "Cost": 500,
        "Year Starts": 2022,
        "Every x Year(s)": 1
    }))
    expenses = Expenses(expense_table)

    trial = {"Social Security": False, "rmd": True, "bad_timing": False}

    plan = Plan(2014, owners, accounts, expenses, rmd, tax, trial)
    assert plan.process_plan(1, rates) == \
        [[2014, 6, 3, 0, 800.0, 0, 0, 800.0, 8000.0, 0.0, 8000.0],
         [2015, 6, 3, 0, 666.67, 0, 66.67, 0.0, 7773.33, 0.0, 7773.33]]
