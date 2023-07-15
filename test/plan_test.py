from src.plan import Plan
from src.account import Account
from src.owner import Owner

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
    "income": 56789,
    "retirement_age": 65,
    "social_security": 5678,
    "start_social_security": 70
}))
owners.append(Owner({
    "name": "Jerry",
    "birth_year": 1977,
    "income": 56789,
    "retirement_age": 65,
    "social_security": 5678,
    "start_social_security": 70
}))


def test_can_initialize_plan():
    plan = Plan(config, owners, accounts)
    assert plan.get_growth() == 6

def test_can_get_header():
    plan = Plan(config, owners, accounts)
    assert plan.get_header() == "Jerry's Roth,Jill's Investment"

def test_can_fill_table_for_one_year():
    plan = Plan(config, owners, accounts)
    assert plan.process_growth(0) == [[4000, 10000]]

def test_can_fill_table_for_two_years():
    plan = Plan(config, owners, accounts)
    assert plan.process_growth(1) == [[4000, 10000], [6240.0, 15600.0]]

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
    plan = Plan(config, bad_owners, accounts)
    assert plan.verify_config() == False

def test_owners_match_accounts():
    plan = Plan(config, owners, accounts)
    assert plan.verify_config() == True