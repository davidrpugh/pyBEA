import pybea
import pprint

UserID = '1985ECDD-2CF4-4239-8A48-4C1C2FFA9A95'



""" Testing the pyBEA API """

def main():
    dataset_list = pybea.get_data_set_list(UserID)
    print(dataset_list, '\n')
    print(pybea.get_parameter_list(UserID, 'NIPA'))
    print(pybea.get_parameter_values(UserID, 'NIPA', ParameterName='TableID', ResultFormat='JSON'))
    # See the documentation (https://apps.bea.gov/api/_pdf/bea_web_service_api_user_guide.pdf)
    # to see required params for each dataset.

    # NIPA Okay
    NIPA_example = pybea.get_data(UserID, 'NIPA', 'JSON', TableName='T10105', Frequency='Q', Year='2017,2018,2019,2020')
    # NIPA_example.to_csv('NIPA_T10105.csv')
    print('This is NIPA example: \n', NIPA_example)

    # NIUnderlyingDetail Okay
    # print('Get param list: ', pybea.get_parameter_list(UserID, 'NIUnderlyingDetail'))
    # print('Get param values: ', pybea.get_parameter_values(UserID, 'NIUnderlyingDetail', 'TableName'))
    print('This is NIUnderlyingDetail: ',  pybea.get_data(UserID=UserID, DataSetName='NIUnderlyingDetail',
                                                          TableName='U001BC', Frequency='A', Year='ALL'))

    # MNE Okay
    # print('Get param list: ', pybea.get_parameter_list(UserID, 'MNE'))
    # print('Get param values: ', pybea.get_parameter_values(UserID, 'MNE', 'OwnershipLevel'))
    print('This is MNE: ',  pybea.get_data(UserID=UserID, DataSetName='MNE',DirectionOfInvestment='Outward',
                                           Classification='COUNTRY', Year='ALL'))

    # FixedAssets Okay
    # print(pybea.get_parameter_list(UserID, 'FixedAssets'))
    # print('asdfasd', pybea.get_parameter_values(UserID, 'FixedAssets', 'TableName'))
    print(pybea.get_data(UserID, 'FixedAssets', TableName='FAAt101', Year='ALL'))

    # ITA Okay
    # print('Get param list: ', pybea.get_parameter_list(UserID, 'ITA'))
    # print('Get param values: ', pybea.get_parameter_values(UserID, 'ITA', 'Indicator'))
    print('This is ITA: ',  pybea.get_data(UserID=UserID, DataSetName='ITA', Year='ALL', Indicator='BalCapAcct'))


    # IIP Okay
    # print('Get param list: ', pybea.get_parameter_list(UserID, 'IIP'))
    # print('Get param values: ', pybea.get_parameter_values(UserID, 'IIP', 'TypeOfInvestment'))
    print('This is IIP: ',  pybea.get_data(UserID=UserID, DataSetName='IIP', TypeOfInvestment='ALL', Year=2015))

    # InputOutput Okay
    # print('Get param list: ', pybea.get_parameter_list(UserID, 'InputOutput'))
    # print('Get param values: ', pybea.get_parameter_values(UserID, 'InputOutput', 'TableID'))
    print('This is IIP: ',  pybea.get_data(UserID=UserID, DataSetName='InputOutput', TableID='56', Year=2015))

    # IntlServTrade
    # print('Get param list: ', pybea.get_parameter_list(UserID, 'IntlServTrade'))
    # print('Get param values: ', pybea.get_parameter_values(UserID, 'IntlServTrade', 'AreaOrCountry'))
    print('This is IntlServTrade: ',  pybea.get_data(UserID=UserID, DataSetName='IntlServTrade', TradeDirection='All',
                                           AreaOrCountry='UnitedKingdom', TypeOfService='WasteTreatAndDePol', Year=2018))

    # GDPbyIndustry Okay
    # print(pybea.get_parameter_list(UserID, 'GDPbyIndustry'))
    # pybea.get_parameter_values(UserID, 'GDPbyIndustry', 'TableID')
    print(pybea.get_data(UserID=UserID, DataSetName='GDPbyIndustry', TableID='ALL', Frequency='A', Year='2016',
                   Industry='ALL'))
    # print('Get parameter list: \n', pybea.get_parameter_list(UserID, 'GDPbyIndustry'))
    # print('Get param values: ', pybea.get_parameter_values(UserID, 'GDPbyIndustry', 'TableID'))
    # print('Get data: \n', pybea.get_data(UserID, 'GDPbyIndustry', TableID=15, Frequency='A', Year=2015, Industry='ALL'))
    # print(pybea.get_data(UserID, 'GDPbyIndustry', TableID=15, Frequency='A', Year=2015, Industry='ALL'))

    # Regional Okay
    # print('Get param list: ', pybea.get_parameter_list(UserID, 'Regional'))
    # print('Get param values: ', pybea.get_parameter_values(UserID, 'Regional', 'LineCode'))
    print('This is Regional: ',  pybea.get_data(UserID=UserID, DataSetName='Regional', TableName='SQINC7H',
                                                GeoFIPS='00000', LineCode=100))
    # UnderlyingGDPbyIndustry Okay
    # print('Get param list: ', pybea.get_parameter_list(UserID, 'UnderlyingGDPbyIndustry'))
    # print('Get param values: ', pybea.get_parameter_values(UserID, 'UnderlyingGDPbyIndustry', 'Industry'))
    print('This is UnderlyingGDPbyIndustry: ',  pybea.get_data(UserID=UserID, DataSetName='UnderlyingGDPbyIndustry',
                                                               TableID='213', Frequency='A', Industry='113FF', Year='ALL'))


if __name__ == '__main__':
    main()


