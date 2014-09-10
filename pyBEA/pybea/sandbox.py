import requests


class DataSet(object):

    base_url = 'http://www.bea.gov/api/data?'

    def __init__(self, api_key, data_set_name, result_format='json'):
        # data_set_name is read-only
        self._data_set_name = data_set_name

        self.api_key = api_key
        self.result_format = result_format

    @property
    def data_set_list(self):
        tmp_query = {'UserID': self.api_key,
                     'Method': 'GetDataSetList',
                     'ResultFormat': self.result_format}
        tmp_response = requests.get(url=self.base_url, params=tmp_query)
        return tmp_response

    @property
    def data_set_name(self):
        return self._data_set_name

    @property
    def parameter_list(self):
        tmp_query = {'UserID': self.api_key,
                     'Method': 'GetParameterList',
                     'DataSetName': self.data_set_name,
                     'ResultFormat': self.result_format}
        tmp_response = requests.get(url=self.base_url, params=tmp_query)
        return tmp_response

    @property
    def result_format(self):
        return self._result_format

    @result_format.setter
    def result_format(self, value):
        self._result_format = self._validate_result_format(value)

    def _validate_result_format(self, value):
        """Validates the result_format attribute."""
        valid_formats = ['json', 'xml']
        if not isinstance(value, str):
            mesg = "'result_format' must be a {} instance."
            raise AttributeError(mesg.format(str))
        elif value.lower() not in valid_formats:
            mesg = "'result_format' must be either {} or {}."
            raise AttributeError(mesg.format(*valid_formats))
        else:
            return value

    def grab_data(self, **kwargs):
        base_query = {'UserID': self.api_key,
                      'Method': 'GetData',
                      'DataSetName': self.data_set_name,
                      'ResultFormat': self.result_format}
        base_query.update(kwargs)
        tmp_response = requests.get(url=self.base_url, params=base_query)
        return tmp_response

    def grab_parameter_values(self, parameter):
        tmp_query = {'UserID': self.api_key,
                     'Method': 'GetParameterValues',
                     'DataSetName': self.data_set_name,
                     'ParameterName': parameter,
                     'ResultFormat': self.result_format}
        tmp_response = requests.get(url=self.base_url, params=tmp_query)
        return tmp_response


class RegionalData(DataSet):

    def __init__(self, api_key, result_format='json'):
        super(RegionalData, self).__init__(api_key, 'RegionalData', result_format)

    def grab_data(self, key_code, geo_fips='STATE', year='ALL'):
        base_query = {'UserID': self.api_key,
                      'Method': 'GetData',
                      'DataSetName': self.data_set_name,
                      'KeyCode': key_code,
                      'GeoFIPS': geo_fips,
                      'Year': year,
                      'ResultFormat': self.result_format}
        tmp_response = requests.get(url=self.base_url, params=base_query)
        return tmp_response


class NIPA(DataSet):

    def __init__(self, api_key, result_format='json'):
        super(RegionalData, self).__init__(api_key, 'NIPA', result_format)


class NIUnderlyingDetail(DataSet):

    def __init__(self, api_key, result_format='json'):
        super(RegionalData, self).__init__(api_key, 'NIUnderlyingDetail', result_format)


class FixedAssets(DataSet):

    def __init__(self, api_key, result_format='json'):
        super(RegionalData, self).__init__(api_key, 'FixedAssets', result_format)
