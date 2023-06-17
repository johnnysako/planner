from src.rmd import Rmd


def test_can_initialize_rmd():
    config = [{
        "rate": 5,
        "age": 5
    }]
    rmd = Rmd(config)
    assert rmd.getRate(5) == 5


def test_can_initialize_with_different_config():
    config = [{
        "rate": 4,
        "age": 4
    }]
    rmd = Rmd(config)
    assert rmd.getRate(4) == 4


def test_gets_rate_for_age():
    config = [{
        "rate": 5,
        "age": 4
    }]
    rmd = Rmd(config)
    assert rmd.getRate(4) == 5


def test_works_with_an_array():
    config = [
        {"rate": 5,
         "age": 4},
        {"rate": 7,
         "age": 6}
    ]
    rmd = Rmd(config)
    assert rmd.getRate(4) == 5
    assert rmd.getRate(6) == 7