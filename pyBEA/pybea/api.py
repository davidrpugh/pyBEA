"""
TODO
-----
1. Use ElementTree to implement XML parsing of BEA data.
2. Lots of documentation needs to be written! Mostly this can be copied
verbatim from the BEA user guide.

"""
import json
import requests


class Request(dict):

    _response = None

    base_url = 'http://www.bea.gov/api/data'

    def __init__(self, UserID, Method, ResultFormat='JSON', **params):
        required_params = {'UserID': UserID,
                           'Method': Method,
                           'ResultFormat': ResultFormat}
        required_params.update(params)
        super(Request, self).__init__(**required_params)

    def __setitem__(self, item, value):
        self._response = None
        return super(Request, self).__setitem__(item, value)

    def __delitem__(self, item):
        self._response = None
        return super(Request, self).__delitem__(item)

    @property
    def _json_request(self):
        raw_json = self._load_json_content()
        return raw_json['BEAAPI']['Request']

    @property
    def _json_results(self):
        raw_json = self._load_json_content()
        return raw_json['BEAAPI']['Results']

    @property
    def _xml_request(self):
        raise NotImplementedError

    @property
    def _xml_results(self):
        raise NotImplementedError

    @property
    def request(self):
        if self['ResultFormat'] == 'JSON':
            tmp_request = self._json_request
        else:
            tmp_request = self._xml_request
        return tmp_request

    @property
    def response(self):
        if self._response is None:
            self._response = requests.get(url=self.base_url, params=self)
        return self._response

    @property
    def results(self):
        if self['ResultFormat'] == 'JSON':
            tmp_results = self._json_results
        else:
            tmp_results = self._xml_results
        return tmp_results

    def _load_json_content(self):
        return json.loads(self.response.content)

    def _load_xml_content(self):
        raise NotImplementedError


class DataSetListRequest(Request):

    def __init__(self, UserID, ResultFormat='JSON', **params):
        required_params = {'UserID': UserID,
                           'Method': 'GetDataSetList',
                           'ResultFormat': ResultFormat}
        required_params.update(params)
        super(DataSetListRequest, self).__init__(**required_params)

    @property
    def _json_data_set(self):
        return self.results['Dataset']

    @property
    def _xml_data_set(self):
        raise NotImplementedError

    @property
    def data_set(self):
        if self['ResultFormat'] == 'JSON':
            tmp_data_set = self._json_data_set
        else:
            tmp_data_set = self._xml_data_set
        return tmp_data_set


class ParameterListRequest(Request):

    def __init__(self, UserID, DataSetName, ResultFormat='JSON', **params):
        required_params = {'UserID': UserID,
                           'Method': 'GetParameterList',
                           'DataSetName': DataSetName,
                           'ResultFormat': ResultFormat}
        required_params.update(params)
        super(ParameterListRequest, self).__init__(**required_params)

    @property
    def _json_parameter_list(self):
        return self.results['Parameter']

    @property
    def _xml_parameter_list(self):
        raise NotImplementedError

    @property
    def parameter_list(self):
        if self['ResultFormat'] == 'JSON':
            tmp_parameter_list = self._json_parameter_list
        else:
            tmp_parameter_list = self._xml_parameter_list
        return tmp_parameter_list


class ParameterValuesRequest(Request):

    def __init__(self, UserID, DataSetName, ParameterName, ResultFormat='JSON',
                 **params):
        required_params = {'UserID': UserID,
                           'Method': 'GetParameterValues',
                           'DataSetName': DataSetName,
                           'ParameterName': ParameterName,
                           'ResultFormat': ResultFormat}
        required_params.update(params)
        super(ParameterValuesRequest, self).__init__(**required_params)

    @property
    def _json_parameter_values(self):
        return self.results['ParamValue']

    @property
    def _xml_parameter_values(self):
        raise NotImplementedError

    @property
    def parameter_values(self):
        if self['ResultFormat'] == 'JSON':
            tmp_parameter_values = self._json_parameter_values
        else:
            tmp_parameter_values = self._xml_parameter_values
        return tmp_parameter_values


class DataRequest(Request):

    @property
    def _json_data(self):
        return self.results['Data']

    @property
    def _xml_data(self):
        raise NotImplementedError

    @property
    def data(self):
        if self['ResultFormat'] == 'JSON':
            tmp_data = self._json_data
        else:
            tmp_data = self._xml_data
        return tmp_data


class RegionalDataRequest(DataRequest):

    def __init__(self, UserID, KeyCode, ResultFormat='JSON', **params):
        required_params = {'UserID': UserID,
                           'Method': 'GetData',
                           'DataSetName': 'RegionalData',
                           'KeyCode': KeyCode,
                           'ResultFormat': ResultFormat}
        required_params.update(params)
        super(RegionalDataRequest, self).__init__(**required_params)


class NIPARequest(DataRequest):

    def __init__(self, UserID, TableID, Frequency, Year, ResultFormat='JSON',
                 **params):
        required_params = {'UserID': UserID,
                           'Method': 'GetData',
                           'DataSetName': 'NIPA',
                           'TableID': TableID,
                           'Frequency': Frequency,
                           'Year': Year,
                           'ResultFormat': ResultFormat}
        required_params.update(params)
        super(NIPARequest, self).__init__(**required_params)


class NIUnderlyingDetailRequest(DataRequest):

    def __init__(self, UserID, TableID, Frequency, Year, ResultFormat='JSON',
                 **params):
        required_params = {'UserID': UserID,
                           'Method': 'GetData',
                           'DataSetName': 'NIUnderlyingDetail',
                           'TableID': TableID,
                           'Frequency': Frequency,
                           'Year': Year,
                           'ResultFormat': ResultFormat}
        required_params.update(params)
        super(NIUnderlyingDetailRequest, self).__init__(**required_params)


class FixedAssetsRequest(DataRequest):

    def __init__(self, UserID, TableID, Year, ResultFormat='JSON', **params):
        required_params = {'UserID': UserID,
                           'Method': 'GetData',
                           'DataSetName': 'FixedAssets',
                           'TableID': TableID,
                           'Year': Year,
                           'ResultFormat': ResultFormat}
        required_params.update(params)
        super(FixedAssetsRequest, self).__init__(**required_params)
