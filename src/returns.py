import numpy as np
import json
import os
import yfinance as yf


def generate_returns(data_distribution, mean, std, years_to_process):
    randoms = [int(x) for x in np.floor(np
                                        .random.default_rng()
                                        .normal(mean,
                                                std,
                                                years_to_process+1))]
    randoms = np.clip(randoms, 0, len(data_distribution)-1)
    returns = []
    for random in randoms:
        if random <= 0:
            returns.append(data_distribution[random])
        else:
            returns.append(np.random
                           .uniform(data_distribution[random-1],
                                    data_distribution[random]))
    return np.array(returns)


def create_data_table(distribution, mean, std,
                      years_to_process, num_simulations, file_name):
    all_returns = []
    for _ in range(num_simulations):
        returns = generate_returns(distribution,
                                   mean, std, years_to_process)
        all_returns.append(returns.tolist())

    with open(os.path.join('_internal',
                           file_name), 'w') as f:
        json.dump(all_returns, f)


def create_stock_returns():
    symbol = "^GSPC"
    start_date = "1950-01-01"
    end_date = "2021-12-31"

    data = yf.download(symbol, start=start_date, end=end_date)

    stock_annual_returns = data['Adj Close'].resample(
        'Y').ffill().pct_change().dropna()
    sorted_stock_annual_returns = sorted(stock_annual_returns)

    create_data_table(sorted_stock_annual_returns, 26, 9, 150, 1000,
                      'stock_returns.json')


def create_bond_returns():
    symbol = "LQD"
    start_date = "2002-07-29"
    end_date = "2021-12-31"

    data = yf.download(symbol, start=start_date, end=end_date)

    bond_annual_returns = data['Adj Close'].resample(
        'Y').ffill().pct_change().dropna()
    sorted_bond_annual_returns = sorted(bond_annual_returns)

    create_data_table(sorted_bond_annual_returns, 6, 2, 150, 1000,
                      'bond_returns.json')


def main():
    create_stock_returns()
    create_bond_returns()


if __name__ == "__main__":
    main()
