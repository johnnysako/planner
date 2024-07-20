import numpy as np


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
