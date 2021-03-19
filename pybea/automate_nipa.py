import pybea
import pandas as pd
import sys
import time
import pickle

# If you get temporarily blocked by the BEA (you probably will if you run these scripts), use the other API key.
UserID = '1985ECDD-2CF4-4239-8A48-4C1C2FFA9A95'
# UserID = 'AEC7FDB2-4F22-4296-982D-7CA35C0341BA'


# Failures: T20200A

def update_all_nipa():
    pass


def update_nipa(tablenames):
    """
    Takes list of tablenames, outputs .csv with their values in NIPA_DATA directory

    """
    failed_list = []
    mb_remaining = 100
    requests_remaining = 100
    for x in tablenames:
        print(x)
        try:
            temp = pybea.get_data(UserID, 'NIPA', TableName=x, Frequency='A,Q,M', Year='2015')
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
        except KeyError:
            failed_list.append(x)
            print('Failure')
            time.sleep(.75)
    return failed_list


def main():
    print(pybea.get_data_set_list(UserID))
    nipa_params = pybea.get_parameter_list(UserID, 'NIPA')
    nipa_table_names = pybea.get_parameter_values(UserID, 'NIPA', ParameterName='TableName', ResultFormat='JSON')
    nipa_table_ids = pybea.get_parameter_values(UserID, 'NIPA', ParameterName='TableID', ResultFormat='JSON')

    print(nipa_params)
    # TableNames and TableIDs appear to be the same
    print('These are the TableNames for NIPA: \n', nipa_table_names)
    print('These are the TableIDs for NIPA: \n', nipa_table_ids)

    df = pd.DataFrame(nipa_table_ids)
    tablenames = df['TableName'].values
    print(tablenames)
    # print(type(tablenames))

    # for x in tablenames:
    #     print(x)

    """
    Problem; not all tables accept the same parameters, some break if given different Frequencies, Years, etc.
    """
    # failed_list = update_nipa(tablenames)
    # update_nipa(['T11100'])

    pickle_test = ['asd', 'sdfs', 'gdf']

    # with open('failure.pkl', 'wb') as f:
    #     pickle.dump(failed_list, f)

    with open('failure.pkl', 'rb') as f:
        failed_list = pickle.load(f)
        print((failed_list))
        print(len(failed_list))

    # Options:
    # (1) User passes list of tables (by TableID) that they want to update to a function.
    # The function then updates each of those tables.

    # (2) User updates all NIPA tables.
    pass

if __name__ == '__main__':
    main()