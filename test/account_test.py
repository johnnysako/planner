from src.account import Account


def test_can_initialize_Account():
    config = {
        "Name": "Blah",
        "Type": "Roth",
    }

    account = Account(config)
    assert account.get_name() == "Blah"


def test_can_get_balance():
    config = {
        "Type": "Roth",
        "Balance": 4000,
    }

    account = Account(config)
    assert account.get_balance() == 4000


def test_apply_growth():
    config = {
        "Type": "Roth",
        "Balance": 4000,
        "Annual Additions": 2000,
    }

    account = Account(config)
    account.process_growth(2023, {"s": 6, "b": 5})
    assert account.get_balance() == 4000*1.06 + 2000


def test_different_values():
    config = {
        "Name": "John's Roth",
        "Type": "Roth",
        "Balance": 5000,
        "Annual Additions": 3000,
    }

    account = Account(config)
    assert account.get_name() == "John's Roth"
    account.process_growth(2020, {"s": 7, "b": 6})
    assert account.get_balance() == 5000*1.07 + 3000


def test_can_only_increase_by_interest():
    config = {
        "Name": "John's Roth",
        "Type": "Roth",
        "Balance": 5000,
        "Annual Additions": 3000,
    }

    account = Account(config)
    assert account.get_name() == "John's Roth"
    account.process_growth(2023, {"s": 7, "b": 6}, True)
    assert account.get_balance() == 5000*1.07


def test_can_get_owner():
    config = {
        "Owner Name": "John",
        "Type": "Roth",
    }

    account = Account(config)
    assert account.get_owner() == "John"


def test_can_get_type():
    config = {
        "Type": "Roth",
    }

    account = Account(config)
    assert account.get_type() == "Roth"


def test_can_pull_funds():
    config = {
        "Type": "Roth",
        "Balance": 5000,
    }

    account = Account(config)
    account.withdraw(1000)
    assert account.get_balance() == 4000


def test_balance_does_not_change_when_withdrawal_fails():
    config = {
        "Type": "Roth",
        "Balance": 5000,
    }

    account = Account(config)
    assert account.withdraw(6000) is False
    assert account.get_balance() == 5000


def test_bob_is_invalid():
    try:
        config = {
            "Type": "bob",
        }

        Account(config)
        assert False
    except TypeError:
        assert True


def test_roth_is_valid():
    config = {
        "Type": "Roth",
    }

    Account(config)


def test_401K_is_valid():
    config = {
        "Type": "401K",
    }

    Account(config)


def test_IRA_is_valid():
    config = {
        "Type": "IRA",
    }

    Account(config)


def test_investment_is_valid():
    config = {
        "Type": "Investment",
    }

    Account(config)


def test_withdrawal_negative_adds():
    config = {
        "Type": "Roth",
        "Balance": 5000,
    }

    account = Account(config)
    account.withdraw(-1000)
    assert account.get_balance() == 6000


def test_withdrawal_rmd_does_not_change_balance_for_Roth():
    config = {
        "Type": "Roth",
        "Balance": 5000,
        "Test as Tax Deferred": False
    }

    account = Account(config)
    assert account.withdraw_rmd(10) == 0
    assert account.get_balance() == 5000


def test_withdrawal_rmd_does_change_balance_for_Roth_when_testing_rmd():
    config = {
        "Type": "Roth",
        "Balance": 5000,
        "Test as Tax Deferred": True
    }

    account = Account(config)
    assert account.withdraw_rmd(10, True) == 500
    assert account.get_balance() == 4500


def test_withdrawal_rmd_does_not_change_balance_for_hsa():
    config = {
        "Type": "HSA",
        "Balance": 5000,
        "Test as Tax Deferred": False
    }

    account = Account(config)
    assert account.withdraw_rmd(10) == 0
    assert account.get_balance() == 5000


def test_is_taxable_roth_false():
    config = {
        "Type": "Roth",
        "Balance": 5000,
    }

    account = Account(config)
    assert account.is_taxable() is False


def test_is_taxable_IRA_false():
    config = {
        "Type": "IRA",
        "Balance": 5000,
    }

    account = Account(config)
    assert account.is_taxable() is False


def test_is_taxable_401k_false():
    config = {
        "Type": "401K",
        "Balance": 5000,
    }

    account = Account(config)
    assert account.is_taxable() is False


def test_is_taxable_investment_true():
    config = {
        "Type": "Investment",
        "Balance": 5000,
    }

    account = Account(config)
    assert account.is_taxable() is True


def test_is_taxable_hsa_false():
    config = {
        "Type": "HSA",
        "Balance": 5000,
    }

    account = Account(config)
    assert account.is_taxable() is False


def test_can_include_allocation():
    config = {
        "Type": "HSA",
        "Balance": 5000,
        "allocation": [{"year": 2000, "stocks": 50, "bonds": 50}]
    }

    account = Account(config)
    assert account.get_allocation(2000, "stocks") == 50
    assert account.get_allocation(2000, "bonds") == 50


def test_allocation_must_total_100():
    try:
        config = {
            "Type": "HSA",
            "Balance": 5000,
            "allocation": [{"year": 2000, "stocks": 45, "bonds": 50}]
        }

        Account(config)
        assert False
    except TypeError:
        assert True


def test_apply_growth_with_allocation():
    config = {
        "Type": "Roth",
        "Balance": 4000,
        "Annual Additions": 2000,
        "allocation": [{"year": 2023, "stocks": 40, "bonds": 60}]
        }

    account = Account(config)
    account.process_growth(2023, {"s": 6, "b": 5})
    assert account.get_balance() == 4000*.4*1.06 + 4000*.6*1.05 + 2000


def test_uses_stock_only_allocation_before_first_year():
    config = {
        "Type": "Roth",
        "Balance": 4000,
        "Annual Additions": 2000,
        "allocation": [{"year": 2023, "stocks": 70, "bonds": 30},
                       {"year": 2043, "stocks": 30, "bonds": 70}]
        }

    account = Account(config)
    account.process_growth(2001, {"s": 6, "b": 5})
    assert account.get_balance() == 4000*1.06 + 2000


def test_uses_allocation_between_years_from_earlier_year():
    config = {
        "Type": "Roth",
        "Balance": 4000,
        "Annual Additions": 2000,
        "allocation": [{"year": 2023, "stocks": 70, "bonds": 30},
                       {"year": 2043, "stocks": 30, "bonds": 70}]
        }

    account = Account(config)
    account.process_growth(2024, {"s": 6, "b": 5})
    assert account.get_balance() == 4000*.7*1.06 + 4000*.3*1.05 + 2000


def test_is_tax_deferred():
    config_401K = {
        "Type": "401K",
        "Balance": 5000,
    }
    config_IRA = {
        "Type": "IRA",
        "Balance": 5000,
    }

    account_401k = Account(config_401K)
    account_ira = Account(config_IRA)

    assert account_401k.is_taxable_deferred() is True
    assert account_ira.is_taxable_deferred() is True


def test_is_tax_free():
    config_hsa = {
        "Type": "HSA",
        "Balance": 5000,
    }
    config_roth = {
        "Type": "HSA",
        "Balance": 5000,
    }

    account_hsa = Account(config_hsa)
    account_roth = Account(config_roth)

    assert account_hsa.is_taxable_free() is True
    assert account_roth.is_taxable_free() is True
