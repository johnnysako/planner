from src.account import Account


def test_can_initialize_Account():
    config = {
        "name": "Blah",
    }

    account = Account(config)
    assert account.get_name() == "Blah"


def test_can_get_balance():
    config = {
        "balance": 4000,
    }

    account = Account(config)
    assert account.get_balance() == 4000


def test_apply_growth():
    config = {
        "balance": 4000,
        "annual_additions": 2000,
    }

    account = Account(config)
    account.process_growth(6)
    assert account.get_balance() == 4000*1.06 + 2000


def test_different_values():
    config = {
        "name": "John's Roth",
        "balance": 5000,
        "annual_additions": 3000,
    }

    account = Account(config)
    assert account.get_name() == "John's Roth"
    account.process_growth(7)
    assert account.get_balance() == 5000*1.07 + 3000

def test_can_only_increase_by_interest():
    config = {
        "name": "John's Roth",
        "balance": 5000,
        "annual_additions": 3000,
    }

    account = Account(config)
    assert account.get_name() == "John's Roth"
    account.process_growth(7, True)
    assert account.get_balance() == 5000*1.07


def test_can_get_owner():
    config = {
        "owner": "John",
    }

    account = Account(config)
    assert account.get_owner() == "John"


def test_can_get_type():
    config = {
        "type": "Roth",
    }

    account = Account(config)
    assert account.get_type() == "Roth"


def test_can_get_priority():
    config = {
        "withdrawl_priority": 1,
    }

    account = Account(config)
    assert account.get_withdrawl_priority() == 1


def test_can_pull_funds():
    config = {
        "balance": 5000,
    }

    account = Account(config)
    account.withdrawl(1000)
    assert account.get_balance() == 4000


def test_balance_does_not_change_when_withrawl_fails():
    config = {
        "balance": 5000,
    }

    account = Account(config)
    assert account.withdrawl(6000) == False
    assert account.get_balance() == 5000
