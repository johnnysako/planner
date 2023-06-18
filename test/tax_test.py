from src.tax import Tax


def test_can_initialize_tax():
    config = [
        {
            "max_tax_previous": 0,
            "rate": 10,
            "cutoff": 10000
        }
    ]

    tax = Tax(config)
    assert tax.calculate(1000) == 100

def test_can_calculate_with_different_rate():
    config = [
        {
            "max_tax_previous": 0,
            "rate": 5,
            "cutoff": 10000
        }
    ]

    tax = Tax(config)
    assert tax.calculate(1000) == 50

def test_no_cutoff():
    config = [
        {
            "max_tax_previous": 0,
            "rate": 12,
            "cutoff": None
        }
    ]

    tax = Tax(config)
    assert tax.calculate(1000) == 120

def test_adds_previous():
    config = [
        {
            "max_tax_previous": 10000,
            "rate": 7,
            "cutoff": None
        }
    ]

    tax = Tax(config)
    assert tax.calculate(100000) == 17000

def test_works_with_two_tiers():
    config = [
        {
            "max_tax_previous": 0,
            "rate": 10,
            "cutoff": 10000
        },
        {
            "max_tax_previous": 1000,
            "rate": 12,
            "cutoff": None
        }
    ]

    tax = Tax(config)
    assert tax.calculate(7000) == 700
    assert tax.calculate(11000) == 1120

def test_works_with_three_tiers():
    config = [
        {
            "max_tax_previous": 0,
            "rate": 10,
            "cutoff": 22000
        },
        {
            "max_tax_previous": 2200,
            "rate": 12,
            "cutoff": 89450
        },
        {
            "max_tax_previous": 10294,
            "rate": 22,
            "cutoff": None
        }
    ]

    tax = Tax(config)
    assert tax.calculate(7000) == 700
    assert tax.calculate(23000) == 2320
    assert tax.calculate(90000) == 10415
