def sort_failed(failed_plans):
    return sorted(failed_plans,
                  key=lambda x:
                  x['Year'].where(x['Sum of Accounts'] == 0).min(),
                  reverse=True)


def sort_data(data_for_analysis):
    failed_plans = []
    remove_index = -1

    sorted_data = sorted(data_for_analysis,
                         key=lambda x: x.iloc[-1]['Sum of Accounts'],
                         reverse=True)

    for i, data in enumerate(sorted_data):
        if data.iloc[-1]['Sum of Accounts'] == 0:
            failed_plans.append(data)
            if remove_index == -1:
                remove_index = i

    del sorted_data[remove_index:]
    failed_plans = sort_failed(failed_plans)

    for data in failed_plans:
        sorted_data.append(data)

    return sorted_data, failed_plans
