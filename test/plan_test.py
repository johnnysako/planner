from src.plan import Plan
from src.account import Account

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
    "average_growth": 6
}

def test_can_initialize_plan():
    plan = Plan(config, accounts)
    assert plan.get_growth() == 6

def test_can_get_header():
    plan = Plan(config, accounts)
    assert plan.get_header() == "Jerry's Roth,Jill's Investment"

def test_can_fill_table_for_one_year():
    plan = Plan(config, accounts)
    assert plan.process_growth(0) == [[4000, 10000]]

def test_can_fill_table_for_two_years():
    plan = Plan(config, accounts)
    assert plan.process_growth(1) == [[4000, 10000], [6240.0, 15600.0]]