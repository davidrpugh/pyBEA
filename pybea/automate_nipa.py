import pybea
import pandas as pd
import numpy as np
import sys
import time
import pickle

# If you get temporarily blocked by the BEA use the other API key.
# UserID = '1985ECDD-2CF4-4239-8A48-4C1C2FFA9A95'
UserID = 'AEC7FDB2-4F22-4296-982D-7CA35C0341BA'


def update_all_nipa_tag(frequency):
    mb_remaining = 100
    requests_remaining = 100
    failures_remaining = 30

    nipa_table_ids = pybea.get_parameter_values(UserID, 'NIPA', ParameterName='TableID', ResultFormat='JSON')
    tablenames = nipa_table_ids['TableName'].values

    series_code_col = []
    period_col = []
    data_val_col = []

    size = .5
    for x in tablenames:
        print(x)
        try:
            data = pybea.get_data(UserID, 'NIPA', TableName=x, ParameterName='TableID', Frequency=frequency, Year='ALL')
            series_code = data['SeriesCode']
            period = data['TimePeriod']
            data_val = data['DataValue']

            series_code_col.extend(series_code)
            period_col.extend(period)
            data_val_col.extend(data_val)

            size = (sys.getsizeof(data) / 1000000)

        except KeyError:
            print('FAILURE', x)
            failures_remaining -= 1
            if failures_remaining == 1:
                time.sleep(55)
            pass

        mb_remaining -= size
        requests_remaining -= 1

        if mb_remaining < 5 or requests_remaining < 2:
            time.sleep(40)
            mb_remaining = 100
            requests_remaining = 100

    aggregate_nipa = pd.DataFrame()
    aggregate_nipa['%SeriesCode'] = series_code_col
    aggregate_nipa['Period'] = period_col
    aggregate_nipa['Value'] = data_val_col

    aggregate_nipa.to_csv('../NIPA_ALL/aggregate_nipa_{0}.csv'.format(frequency))

    print(tablenames)


def update_all_nipa():
    """
    Updates all NIPA data (in NIPA_DATA directory) for year 2000 (default, can be changed below)

    Parameters
    ----------
    Returns: dictionary of failed tables
    -------

    """
    failed_dict = {}
    mb_remaining = 100
    requests_remaining = 100

    nipa_table_ids = pybea.get_parameter_values(UserID, 'NIPA', ParameterName='TableID', ResultFormat='JSON')
    tablenames = nipa_table_ids['TableName'].values

    for x in tablenames:
        print(x)
        temp = pybea.get_data(UserID, 'NIPA', TableName=x, Frequency='A', Year='ALL')
        # Compute how many megabytes each request is
        print('This request was ', sys.getsizeof(temp) / 1000000, 'megabytes')
        size = sys.getsizeof(temp) / 1000000
        mb_remaining -= size
        requests_remaining -= 1
        print('You have ', mb_remaining, 'more megabytes before throttling and ', requests_remaining,
              'request/s remaining before throttling.')
        temp.to_csv('../NIPA_DATA/{0}.csv'.format(x))
        time.sleep(1)
        if mb_remaining < 5:
            time.sleep(30)
            mb_remaining = 100
        if requests_remaining < 2:
            time.sleep(45)
            requests_remaining = 100
        if pybea.JSON_ERROR:
            failed_dict[x] = pybea.JSON_ERROR
            time.sleep(.75)
    return failed_dict


def update_nipa(tablenames, frequency, year):
    """
    Updates NIPA data (in NIPA_DATA directory) based on specified list and params

    Parameters
    ----------
    tablenames: list of tables to be updated
    frequency: Annual, Quarterly, or Monthly ('A', 'Q', 'M')
    year: year

    Returns: dictionary of failed tables
    -------

    """
    failed_dict = {}
    mb_remaining = 100
    requests_remaining = 100
    for x in tablenames:
        print(x)
        temp = pybea.get_data(UserID, 'NIPA', TableName=x, Frequency=frequency, Year=year)
        # Compute how many megabytes each request is
        print('This request was ', sys.getsizeof(temp)/1000000, 'megabytes')
        size = sys.getsizeof(temp) / 1000000
        mb_remaining -= size
        requests_remaining -= 1
        print('You have ', mb_remaining, 'more megabytes before throttling and ', requests_remaining,
              'request/s remaining before throttling.')
        temp.to_csv('../NIPA_DATA/{0}.csv'.format(x))
        time.sleep(1)
        if mb_remaining < 5:
            time.sleep(30)
            mb_remaining = 100
        if requests_remaining < 2:
            time.sleep(45)
            requests_remaining = 100
        if pybea.JSON_ERROR:
            failed_dict[x] = pybea.JSON_ERROR
            time.sleep(.75)

    return failed_dict


def main():
    # Options:
    # (1) User passes list of tables (by TableID) that they want to update to a function.
    # The function then updates each of those tables.

    # (2) User updates all NIPA tables.
    # print(pybea.get_data_set_list(UserID))
    # nipa_params = pybea.get_parameter_list(UserID, 'NIPA')
    # nipa_table_names = pybea.get_parameter_values(UserID, 'NIPA', ParameterName='TableName', ResultFormat='JSON')
    # nipa_table_ids = pybea.get_parameter_values(UserID, 'NIPA', ParameterName='TableID', ResultFormat='JSON')

    # print(nipa_params)
    # TableNames and TableIDs appear to be the same
    # print('These are the TableNames for NIPA: \n', nipa_table_names)
    # print('These are the TableIDs for NIPA: \n', nipa_table_ids)

    # df = pd.DataFrame(nipa_table_ids)
    # tablenames = df['TableName'].values
    # print(tablenames)

    # Updated update function
    # update_all_nipa_tag('Y')
    update_all_nipa_tag('Q')
    # update_all_nipa_tag('M')

    # Save a list of all the tables that failed get_data calls.
    # failed_dict = update_all_nipa()
    # failed_dict = update_nipa(tablenames, 'A', 2015)
    # print(failed_dict)

    # with open('failure.pkl', 'wb') as f:
    #     pickle.dump(failed_list, f)

    # with open('failure.pkl', 'rb') as f:
    #     failed_list = pickle.load(f)
    #     print((failed_list))
    #     print(len(failed_list))


if __name__ == '__main__':
    main()
