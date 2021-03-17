import pybea
import pprint

UserID = '1985ECDD-2CF4-4239-8A48-4C1C2FFA9A95'



""" Testing the pyBEA API """

def main():
    dataset_list = pybea.get_data_set_list(UserID)
    print(dataset_list, '\n')
    # print(pybea.get_parameter_list(UserID, 'NIPA'))
    # print(pybea.get_parameter_values(UserID, 'NIPA', ParameterName='TableID', ResultFormat='JSON'))
    # # See the documentation (https://apps.bea.gov/api/_pdf/bea_web_service_api_user_guide.pdf)
    # # to see required params for each dataset.
    NIPA_example = pybea.get_data(UserID, 'NIPA', 'JSON', TableName='T10105', Frequency='Q', Year='2017,2018,2019,2020')
    NIPA_example.to_csv('NIPA_T10105.csv')
    print('This is NIPA example: \n', NIPA_example)

    print(pybea.get_parameter_list(UserID, 'GDPbyIndustry'))
    pybea.get_parameter_values(UserID, 'GDPbyIndustry', 'TableID')
    pybea.get_data(UserID=UserID, DataSetName='GDPbyIndustry', TableID='ALL', Frequency='A', Year='2016', Industry='ALL')

    # This works now after changing the dictionary key from 'IndustryDescription to IndustrYDescription'
    # There is a typo in the header that comes back from the BEA API call
    print('Get parameter list: \n', pybea.get_parameter_list(UserID, 'GDPbyIndustry'))
    print('Get param values: ', pybea.get_parameter_values(UserID, 'GDPbyIndustry', 'TableID'))
    print('Get data: \n', pybea.get_data(UserID, 'GDPbyIndustry', TableID=15, Frequency='A', Year=2015, Industry='ALL'))
    print(pybea.get_data(UserID, 'GDPbyIndustry', TableID=15, Frequency='A', Year=2015, Industry='ALL'))


    print(pybea.get_parameter_list(UserID, 'FixedAssets'))
    print('asdfasd', pybea.get_parameter_values(UserID, 'FixedAssets', 'TableName'))
    print(pybea.get_data(UserID, 'FixedAssets', TableName='FAAt101', Year='ALL'))



    print('Get param list: ', pybea.get_parameter_list(UserID, 'ITA'))
    print('Get param values: ', pybea.get_parameter_values(UserID, 'ITA', 'Indicator'))
    print('This is ITA: ',  pybea.get_data(UserID=UserID, DataSetName='ITA', Year='ALL', Indicator='BalCapAcct'))




if __name__ == '__main__':
    main()


