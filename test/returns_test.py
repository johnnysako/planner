import pytest
import numpy as np
from src.returns import generate_returns
from src.returns import create_data_table
import os
import json


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


@pytest.fixture
def setup_data_table():
    distribution = np.array([0, 1, 2, 3, 4, 5])
    mean = 2
    std = 1
    years_to_process = 5
    num_simulations = 10
    file_name = 'test_returns.json'
    yield distribution, mean, std, years_to_process, num_simulations, file_name
    if os.path.exists(os.path.join('_internal', file_name)):
        os.remove(os.path.join('_internal', file_name))


def test_create_data_table_file_creation(setup_data_table):
    distribution, mean, std, years_to_process, num_simulations, \
        file_name = setup_data_table
    create_data_table(distribution, mean, std, years_to_process,
                      num_simulations, file_name)
    assert os.path.exists(os.path.join('_internal', file_name))


def test_create_data_table_num_simulations(setup_data_table):
    distribution, mean, std, years_to_process, num_simulations, \
        file_name = setup_data_table
    create_data_table(distribution, mean, std, years_to_process,
                      num_simulations, file_name)
    with open(os.path.join('_internal', file_name), 'r') as f:
        data = json.load(f)
    assert len(data) == num_simulations


def test_create_data_table_num_returns_per_simulation(setup_data_table):
    distribution, mean, std, years_to_process, num_simulations, \
        file_name = setup_data_table
    create_data_table(distribution, mean, std, years_to_process,
                      num_simulations, file_name)
    with open(os.path.join('_internal', file_name), 'r') as f:
        data = json.load(f)
    for returns in data:
        assert len(returns) == years_to_process + 1
