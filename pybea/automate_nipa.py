import pybea
import pandas as pd
import sys
import time

# If you get temporarily blocked by the BEA use the other API key.
# UserID = '1985ECDD-2CF4-4239-8A48-4C1C2FFA9A95'
# UserID = 'AEC7FDB2-4F22-4296-982D-7CA35C0341BA'
UserID = '0B4FD943-BC51-49E8-97E1-81C6C85D34F9'


def update_all_nipa_tag(frequency):
    """
    Generates one .csv file (in NIPA_ALL) containing all the NIPA data for a given frequency for all available years.
    The TAG model uses Annual data for the NIPA dataset.
    Parameters
    ----------
    string frequency: 'A', 'Q', 'M'

    Returns --
    -------
    """
    mb_remaining = 100
    requests_remaining = 100
    failures_remaining = 30

    nipa_table_ids = pybea.get_parameter_values(UserID, 'NIPA', ParameterName='TableName', ResultFormat='JSON')
    tablenames = nipa_table_ids['TableName'].values

    series_code_col = []
    period_col = []
    data_val_col = []
    table_name = []

    size = .5
    for x in tablenames:
        print(x)
        try:
            data = pybea.get_data(UserID, 'NIPA', TableName=x, Frequency=frequency, Year='ALL')
            series_code = data['SeriesCode']
            period = data['TimePeriod']
            data_val = data['DataValue']

            series_code_col.extend(series_code)
            period_col.extend(period)
            data_val_col.extend(data_val)

            size = (sys.getsizeof(data) / 1000000)

            table_name.append(x)

        except KeyError:
            # Failures typically mean that the dataset isn't available for the given frequency that was affected.
            print('FAILURE', x)
            failures_remaining -= 1
            if failures_remaining < 3:
                print('Going to sleep for 60 seconds')
                time.sleep(60)
                failures_remaining = 30

        mb_remaining -= size
        requests_remaining -= 1

        if mb_remaining < 5 or requests_remaining < 3:
            time.sleep(60)
            mb_remaining = 100
            requests_remaining = 100

    aggregate_nipa = pd.DataFrame()
    aggregate_nipa['%SeriesCode'] = series_code_col
    aggregate_nipa['Period'] = period_col
    aggregate_nipa['Value'] = data_val_col

    aggregate_nipa.to_csv('../NIPA_ALL/aggregate_nipa_{0}.csv'.format(frequency), index=False)
    aggregate_nipa.to_csv('aggregate_nipa_{0}.csv'.format(frequency), index=False)

    # print('These are the tables that returned valid results: ', table_name)


def update_all_nipa():
    """
    Updates all NIPA data (in NIPA_DATA directory) for year 2000 (default, can be changed below)

    Parameters: None
    ----------
    Returns: dictionary of failed tables
    -------

    """
    failed_dict = {}
    mb_remaining = 100
    requests_remaining = 100

    nipa_table_ids = pybea.get_parameter_values(UserID, 'NIPA', ParameterName='TableName', ResultFormat='JSON')
    tablenames = nipa_table_ids['TableName'].values

    for x in tablenames:
        print(x)
        temp = pybea.get_data(UserID, 'NIPA', TableName=x, Frequency='A', Year='2000')
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
    # Updated update function
    update_all_nipa_tag('A')


if __name__ == '__main__':
    main()
