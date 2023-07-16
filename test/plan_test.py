from src.plan import Plan
from src.account import Account
from src.owner import Owner
from src.expense import Expense
from src.expenses import Expenses

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

config = {
    "average_growth": 6,
    "plan_start": 2023,
}

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

def test_can_initialize_plan():
    plan = Plan(config, owners, accounts, expenses)
    assert plan.get_growth() == 6

def test_can_get_header():
    plan = Plan(config, owners, accounts, expenses)
    assert plan.get_header() == ["Year", "Income", "Expenses", "Jerry's Roth", "Jill's Investment"]

def test_can_fill_table_for_one_year():
    plan = Plan(config, owners, accounts, expenses)
    assert plan.process_growth(2022, 0) == [[2022, 3000, 22000, 4000, 10000]]

def test_can_fill_table_for_two_years():
    plan = Plan(config, owners, accounts, expenses)
    assert plan.process_growth(2022, 1) == [[2022, 3000, 22000, 4000, 10000], [2023, 3000, 2000, 6240.0, 15600.0]]

def test_owners_do_not_match_accounts():
    bad_owners = []
    bad_owners.append(Owner({
        "name": "Babs",
        "birth_year": 1977,
        "income": 56789,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }))
    plan = Plan(config, bad_owners, accounts, expenses)
    assert plan.verify_config() == False

def test_owners_match_accounts():
    plan = Plan(config, owners, accounts, expenses)
    assert plan.verify_config() == True