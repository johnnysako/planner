import pandas as pd
from src.sort import sort_failed, sort_data


def create_test_data():
    # Create some test data frames
    data1 = pd.DataFrame({
        'Year': [2020, 2021, 2022, 2023],
        'Sum of Accounts': [100, 50, 0, 0]
    })

    data2 = pd.DataFrame({
        'Year': [2020, 2021, 2022, 2023],
        'Sum of Accounts': [200, 150, 100, 50]
    })

    data3 = pd.DataFrame({
        'Year': [2020, 2021, 2022, 2023],
        'Sum of Accounts': [300, 200, 100, 0]
    })

    return [data1, data2, data3]


def test_sort_failed():
    failed_plans = create_test_data()

    failed_plans = [plan for plan in failed_plans if plan.iloc[-1]
                    ['Sum of Accounts'] == 0]

    sorted_failed = sort_failed(failed_plans)

    assert sorted_failed[0].iloc[0]['Sum of Accounts'] == 300
    assert sorted_failed[1].iloc[0]['Sum of Accounts'] == 100


def test_sort_data():
    data_for_analysis = create_test_data()

    sorted_data, failed_plans = sort_data(data_for_analysis)

    assert sorted_data[0].iloc[0]['Sum of Accounts'] == 200

    assert failed_plans[0].iloc[0]['Sum of Accounts'] == 300
    assert failed_plans[1].iloc[0]['Sum of Accounts'] == 100

    assert sorted_data[-2].iloc[0]['Sum of Accounts'] == 300
    assert sorted_data[-1].iloc[0]['Sum of Accounts'] == 100
