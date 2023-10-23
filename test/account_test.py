from src.account import Account


def test_can_initialize_Account():
    config = {
        "name": "Blah",
        "type": "Roth",
    }

    account = Account(config)
    assert account.get_name() == "Blah"


def test_can_get_balance():
    config = {
        "type": "Roth",
        "balance": 4000,
    }

    account = Account(config)
    assert account.get_balance() == 4000


def test_apply_growth():
    config = {
        "type": "Roth",
        "balance": 4000,
        "annual_additions": 2000,
    }

    account = Account(config)
    account.process_growth(6)
    assert account.get_balance() == 4000*1.06 + 2000


def test_different_values():
    config = {
        "name": "John's Roth",
        "type": "Roth",
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
        "type": "Roth",
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
        "type": "Roth",
    }

    account = Account(config)
    assert account.get_owner() == "John"


def test_can_get_type():
    config = {
        "type": "Roth",
    }

    account = Account(config)
    assert account.get_type() == "Roth"


def test_can_pull_funds():
    config = {
        "type": "Roth",
        "balance": 5000,
    }

    account = Account(config)
    account.withdrawl(1000)
    assert account.get_balance() == 4000


def test_balance_does_not_change_when_withrawl_fails():
    config = {
        "type": "Roth",
        "balance": 5000,
    }

    account = Account(config)
    assert account.withdrawl(6000) is False
    assert account.get_balance() == 5000


def test_bob_is_invalid():
    try:
        config = {
            "type": "bob",
        }

        Account(config)
        assert False
    except TypeError:
        assert True


def test_roth_is_valid():
    config = {
        "type": "Roth",
    }

    Account(config)


def test_401K_is_valid():
    config = {
        "type": "401K",
    }

    Account(config)


def test_IRA_is_valid():
    config = {
        "type": "IRA",
    }

    Account(config)


def test_investment_is_valid():
    config = {
        "type": "Investment",
    }

    Account(config)


def test_withdrawl_negative_adds():
    config = {
        "type": "Roth",
        "balance": 5000,
    }

    account = Account(config)
    account.withdrawl(-1000)
    assert account.get_balance() == 6000


def test_withdrawl_rmd_does_not_change_balance_for_Roth():
    config = {
        "type": "Roth",
        "balance": 5000,
        "trail_with_rmd": False
    }

    account = Account(config)
    assert account.withdrawl_rmd(10) == 0
    assert account.get_balance() == 5000


def test_withdrawl_rmd_does_change_balance_for_Roth_when_testing_rmd():
    config = {
        "type": "Roth",
        "balance": 5000,
        "trail_with_rmd": True
    }

    account = Account(config)
    assert account.withdrawl_rmd(10, True) == 500
    assert account.get_balance() == 4500


def test_withdrawl_rmd_does_not_change_balance_for_hsa():
    config = {
        "type": "HSA",
        "balance": 5000,
        "trail_with_rmd": False
    }

    account = Account(config)
    assert account.withdrawl_rmd(10) == 0
    assert account.get_balance() == 5000


def test_is_taxable_roth_false():
    config = {
        "type": "Roth",
        "balance": 5000,
    }

    account = Account(config)
    assert account.is_taxable() is False


def test_is_taxable_IRA_false():
    config = {
        "type": "IRA",
        "balance": 5000,
    }

    account = Account(config)
    assert account.is_taxable() is False


def test_is_taxable_401k_false():
    config = {
        "type": "401K",
        "balance": 5000,
    }

    account = Account(config)
    assert account.is_taxable() is False


def test_is_taxable_investment_true():
    config = {
        "type": "Investment",
        "balance": 5000,
    }

    account = Account(config)
    assert account.is_taxable() is True


def test_is_taxable_hsa_false():
    config = {
        "type": "HSA",
        "balance": 5000,
    }

    account = Account(config)
    assert account.is_taxable() is False
