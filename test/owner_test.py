from src.owner import Owner


def test_can_initialize_owner():
    config = {
        "name": "Bubbles"
    }

    owner = Owner(config)
    assert owner.get_name() == "Bubbles"


def test_can_get_age():
    config = {
        "age": 42
    }

    owner = Owner(config)
    assert owner.get_age() == 42


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
