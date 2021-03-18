import pybea
import pprint
import pandas as pd

UserID = '1985ECDD-2CF4-4239-8A48-4C1C2FFA9A95'


def update_all_nipa():
    pass


def update_nipa(*args):
    for table_name in args:
        print(table_name)
        try:
            temp = pybea.get_data(UserID, 'NIPA', TableName=table_name, Frequency='A,Q,M', Year='2015')
            temp.to_csv('{0}'.format(table_name))
        except KeyError:
            pass
    return


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
    # update_nipa('T80106', 'T10112')

    # So for each Table, we want to have what?
    # Options: User passes list of tables (by TableName) that they want to update to a function.
    # The function then updates each of those tables.
    pass

if __name__ == '__main__':
    main()