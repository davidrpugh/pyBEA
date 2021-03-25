import pybea
import pprint
import pandas as pd
import sys
import time
import pickle

# UserID = '1985ECDD-2CF4-4239-8A48-4C1C2FFA9A95'
UserID = 'AEC7FDB2-4F22-4296-982D-7CA35C0341BA'


def update_all_fa_tag():
    failed_dict = {}
    mb_remaining = 100
    requests_remaining = 100

    fa_table_ids = pybea.get_parameter_values(UserID, 'FixedAssets', ParameterName='TableName', ResultFormat='JSON')
    tablenames = fa_table_ids['TableName'].values

    table_name_col = []
    series_code_col = []
    period_col = []
    data_val_col = []
    line_description_col = []

    for x in tablenames:
        print(x)
        temp = pybea.get_data(UserID, 'FixedAssets', TableName=x, Year='ALL')
        # Compute how many megabytes each request is
        print('This request was ', sys.getsizeof(temp) / 1000000, 'megabytes')
        size = sys.getsizeof(temp) / 1000000
        mb_remaining -= size
        requests_remaining -= 1

        table_name = temp['TableName']
        series_code = temp['SeriesCode']
        period = temp['TimePeriod']
        data_val = temp['DataValue']
        line_description = temp['LineDescription']

        table_name_col.extend(table_name)
        series_code_col.extend(series_code)
        period_col.extend(period)
        data_val_col.extend(data_val)
        line_description_col.extend(line_description)

        time.sleep(1)
        if mb_remaining < 5:
            time.sleep(55)
            mb_remaining = 100
            requests_remaining = 100
        if requests_remaining < 2:
            time.sleep(45)
            mb_remaining = 100
            requests_remaining = 100
        if pybea.JSON_ERROR:
            failed_dict[x] = pybea.JSON_ERROR
            print('FAILED FAILED FAILED')
            time.sleep(1)

    aggregate_fa = pd.DataFrame()
    aggregate_fa['TableName'] = table_name_col
    aggregate_fa['LineDescription'] = line_description_col
    aggregate_fa['SeriesCode'] = series_code_col
    aggregate_fa['TimePeriod'] = period_col
    aggregate_fa['DataValue'] = data_val_col

    aggregate_fa.to_csv('../FA_ALL/aggregate_fa.csv', index=False)

    return failed_dict

def update_all_fa():
    """
    Updates all FixedAssets data (in FA_DATA directory) for year 2000 (default, can be changed below)

    Parameters
    ----------
    Returns: dictionary of failed tables
    -------

    """
    failed_dict = {}
    mb_remaining = 100
    requests_remaining = 100

    fa_table_ids = pybea.get_parameter_values(UserID, 'FixedAssets', ParameterName='TableName', ResultFormat='JSON')
    tablenames = fa_table_ids['TableName'].values

    for x in tablenames:
        print(x)
        temp = pybea.get_data(UserID, 'FixedAssets', TableName=x, Frequency='A', Year=2000)
        # Compute how many megabytes each request is
        print('This request was ', sys.getsizeof(temp) / 1000000, 'megabytes')
        size = sys.getsizeof(temp) / 1000000
        mb_remaining -= size
        requests_remaining -= 1
        print('You have ', mb_remaining, 'more megabytes before throttling and ', requests_remaining,
              'request/s remaining before throttling.')
        temp.to_csv('../FA_DATA/{0}.csv'.format(x))
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


def update_fa(tablenames, frequency, year):
    """
    Updates FixedAsset data (in FA_DATA directory) based on specified list and params

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
        temp = pybea.get_data(UserID, 'FixedAssets', TableName=x, Frequency=frequency, Year=year)
        # Compute how many megabytes each request is
        print('This request was ', sys.getsizeof(temp) / 1000000, 'megabytes')
        size = sys.getsizeof(temp) / 1000000
        mb_remaining -= size
        requests_remaining -= 1
        print('You have ', mb_remaining, 'more megabytes before throttling and ', requests_remaining,
              'request/s remaining before throttling.')
        temp.to_csv('../FA_DATA/{0}.csv'.format(x))
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
    # print(pybea.get_data_set_list(UserID))
    # print(pybea.get_parameter_list(UserID, 'FixedAssets'))
    # fa_params = pybea.get_parameter_list(UserID, 'FixedAssets')

    # fa_table_names = pybea.get_parameter_values(UserID, 'FixedAssets', ParameterName='TableName', ResultFormat='JSON')
    # tablenames = fa_table_names['TableName'].values
    # print(tablenames)

    # nipa_table_ids = pybea.get_parameter_values(UserID, 'FixedAssets', ParameterName='TableID', ResultFormat='JSON')
    # fixed_assets = update_fa(tablenames, 'A', 2010)
    # print(fixed_assets)

    failed = update_all_fa_tag()
    print(failed)


if __name__ == '__main__':
    main()