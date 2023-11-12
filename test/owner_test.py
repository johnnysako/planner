from src.owner import Owner


def test_can_initialize_owner():
    config = {
        "Name": "Bubbles"
    }

    owner = Owner(config)
    assert owner.get_name() == "Bubbles"


def test_can_get_age():
    config = {
        "Year of Birth": 1977
    }

    owner = Owner(config)
    assert owner.get_age(2023) == 46


def test_can_get_retirement_age():
    config = {
        "Retirement Age": 72
    }

    owner = Owner(config)
    assert owner.get_retirement_age() == 72


def test_can_get_social_security_benefit():
    config = {
        "Social Security": 1234
    }

    owner = Owner(config)
    assert owner.get_social_security() == 1234


def test_can_get_different_social_security_benefit():
    config = {
        "Social Security": 5678
    }

    owner = Owner(config)
    assert owner.get_social_security() == 5678


def test_get_income():
    config = {
        "Year of Birth": 1977,
        "Pre-retirement Take Home Pay": 56789,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
    }

    owner = Owner(config)
    assert owner.get_income(True, 2010) == 56789
    assert owner.get_income(True, 2042) == 56789
    assert owner.get_income(True, 2043) == 0
    assert owner.get_income(True, 2046) == 0
    assert owner.get_income(True, 2047) == 5678


def test_get_income_no_social_security():
    config = {
        "Year of Birth": 1977,
        "Pre-retirement Take Home Pay": 56789,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
    }

    owner = Owner(config)
    assert owner.get_income(False, 2010) == 56789
    assert owner.get_income(False, 2043) == 0
    assert owner.get_income(False, 2046) == 0
    assert owner.get_income(False, 2047) == 0


def test_get_life():
    config = {
        "Life Expectancy": 110
    }

    owner = Owner(config)
    assert owner.get_life() == 110


def test_get_different_life():
    config = {
        "Life Expectancy": 115
    }

    owner = Owner(config)
    assert owner.get_life() == 115


def test_is_retired():
    config = {
        "Year of Birth": 1950,
        "Pre-retirement Take Home Pay": 56789,
        "Retirement Age": 65,
        "Social Security": 5678,
        "Age Starts Social Security": 70
    }

    owner = Owner(config)

    assert owner.is_retired(2015) is False
    assert owner.is_retired(2016) is True


def test_get_years_to_live():
    config = {
        "Year of Birth": 1950,
        "Life Expectancy": 115,
        "Pre-retirement Take Home Pay": 56789,
    }

    owner = Owner(config)

    assert owner.years_to_live(2023) == 43
