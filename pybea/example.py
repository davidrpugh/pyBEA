import pybea

UserID = '1985ECDD-2CF4-4239-8A48-4C1C2FFA9A95'


def main():
    dataset_list = pybea.get_data_set_list(UserID)
    print(dataset_list, '\n')
    print(pybea.get_parameter_list(UserID, 'NIPA'))

    # See the documentation (https://apps.bea.gov/api/_pdf/bea_web_service_api_user_guide.pdf)
    # to see required params for each dataset.
    NIPA_example = pybea.get_data(UserID, 'NIPA', 'JSON', TableName='T10105', Frequency='Q', Year='2017,2018,2019,2020')
    NIPA_example.to_csv('NIPA_T10105.csv')

    pybea.get_parameter_list(UserID, 'GDPbyIndustry').to_csv('gdp_by_industry.csv')
    # print(pybea.get_parameter_values(UserID, 'GDPbyIndustry', 'TableName'))


if __name__ == '__main__':
    main()
