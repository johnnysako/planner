import pytest
import numpy as np
from src.returns import generate_returns


@pytest.fixture
def setup_data():
    data_distribution = np.array([0, 1, 2, 3, 4, 5])
    mean = 2
    std = 1
    years_to_process = 5
    return data_distribution, mean, std, years_to_process


def test_length_of_returns(setup_data):
    data_distribution, mean, std, years_to_process = setup_data
    returns = generate_returns(data_distribution, mean, std, years_to_process)
    assert len(returns) == years_to_process + 1


def test_returns_within_distribution_bounds(setup_data):
    data_distribution, mean, std, years_to_process = setup_data
    returns = generate_returns(data_distribution, mean, std, years_to_process)
    assert np.all(returns >= data_distribution[0])
    assert np.all(returns <= data_distribution[-1])


def test_returns_distribution_zero_length():
    mean = 2
    std = 1
    years_to_process = 5
    with pytest.raises(IndexError):
        generate_returns(np.array([]), mean, std, years_to_process)


def test_non_negative_randoms(setup_data):
    data_distribution, mean, std, years_to_process = setup_data
    randoms = [int(x) for x in np.floor(np.random.default_rng()
                                        .normal(mean, std,
                                                years_to_process + 1))]
    randoms = np.clip(randoms, 0, len(data_distribution) - 1)
    assert np.all(np.array(randoms) >= 0)


def test_randoms_within_bounds(setup_data):
    data_distribution, mean, std, years_to_process = setup_data
    randoms = [int(x) for x in np.floor(np.random.default_rng()
                                        .normal(mean, std,
                                                years_to_process + 1))]
    randoms = np.clip(randoms, 0, len(data_distribution) - 1)
    assert np.all(np.array(randoms) < len(data_distribution))
