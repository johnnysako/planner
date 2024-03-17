from src.tax import Tax
import pytest


@pytest.fixture
def tax_instance():
    config = {
        "married joint": [
            {"max_tax_previous": 0, "rate": 10, "cutoff": 23200},
            {"max_tax_previous": 2320, "rate": 12, "cutoff": 94300}
        ],
        "single": [
            {"max_tax_previous": 0, "rate": 10, "cutoff": 11600},
            {"max_tax_previous": 1160, "rate": 12, "cutoff": 45200}
        ],
        "married separate": [
            {"max_tax_previous": 0, "rate": 10, "cutoff": 11600},
            {"max_tax_previous": 1160, "rate": 12, "cutoff": 47150},
            {"max_tax_previous": 5376, "rate": 22, "cutoff": 95250},
            {"max_tax_previous": 19571, "rate": 24, "cutoff": None}
        ]
    }
    return Tax(config)


def test_single_filing_status(tax_instance):
    income = 30000
    expected_tax = 12/100 * (income - 11600) + 1160
    assert tax_instance.calculate(income, "single") == expected_tax


def test_married_joint_filing_status(tax_instance):
    income = 80000
    expected_tax = 12/100 * (income - 23200) + 2320
    assert tax_instance.calculate(income, "married joint") == expected_tax


def test_married_separate_filing_status(tax_instance):
    income = 100000
    expected_tax = 24/100 * (income - 95250) + 19571
    assert tax_instance.calculate(income, "married separate") == expected_tax


def test_invalid_filing_status(tax_instance):
    income = 50000
    with pytest.raises(ValueError):
        tax_instance.calculate(income, "invalid")
