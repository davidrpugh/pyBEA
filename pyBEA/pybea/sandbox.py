import requests


class BEA(object):

    base_url = 'http://www.bea.gov/api/data?'

    def __init__(self, api_key, result_format='json'):
        self.api_key = api_key
        self.result_format = result_format

    @property
    def data(self):
        tmp_query = {'UserID': self.api_key,
                     'Method': 'GetData',
                     'DataSetName': self.data_set_name,
                     'ResultFormat': self.result_format}
        tmp_response = requests.get(url=self.base_url, params=tmp_query)
        return tmp_response

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
    def parameter_name(self):
        return self._parameter_name

    @property
    def parameter_values(self):
        tmp_query = {'UserID': self.api_key,
                     'Method': 'GetParameterValues',
                     'DataSetName': self.data_set_name,
                     'ParameterName': self.parameter_name,
                     'ResultFormat': self.result_format}
        tmp_response = requests.get(url=self.base_url, params=tmp_query)
        return tmp_response

    @data_set_name.setter
    def data_set_name(self, value):
        self._data_set_name = value

    @parameter_name.setter
    def parameter_name(self, value):
        self._parameter_name = value
    