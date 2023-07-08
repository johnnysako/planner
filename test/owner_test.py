from src.owner import Owner


def test_can_initialize_owner():
    config = {
        "name": "Bubbles"
    }

    owner = Owner(config)
    assert owner.get_name() == "Bubbles"


def test_can_get_age():
    config = {
        "birth_year": 1977
    }

    owner = Owner(config)
    assert owner.get_age(2023) == 46


def test_can_get_retirement_age():
    config = {
        "retirement_age": 72
    }

    owner = Owner(config)
    assert owner.get_retirement_age() == 72


def test_can_get_social_security_benefit():
    config = {
        "social_security": 1234
    }

    owner = Owner(config)
    assert owner.get_social_security() == 1234


def test_can_get_different_social_security_benefit():
    config = {
        "social_security": 5678
    }

    owner = Owner(config)
    assert owner.get_social_security() == 5678


def test_should_trial_social_security():
    config = {
        "trial_social_security": True
    }

    owner = Owner(config)
    assert owner.trial_social_security() == True

    config_other = {
        "trial_social_security": False
    }

    other_owner = Owner(config_other)
    assert other_owner.trial_social_security() == False

def test_get_income():
    config = {
        "birth_year": 1977,
        "income": 56789,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }

    owner = Owner(config)
    assert owner.get_income(True, 2010) == 56789
    assert owner.get_income(True, 2042) == 0    
    assert owner.get_income(True, 2046) == 0    
    assert owner.get_income(True, 2047) == 5678

def test_get_income_no_social_security():
    config = {
        "birth_year": 1977,
        "income": 56789,
        "retirement_age": 65,
        "social_security": 5678,
        "start_social_security": 70
    }

    owner = Owner(config)
    assert owner.get_income(False, 2010) == 56789
    assert owner.get_income(False, 2042) == 0    
    assert owner.get_income(False, 2046) == 0    
    assert owner.get_income(False, 2047) == 0