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
        return super(Request, self).__setitem__(self, item, value)

    def __delitem__(self, item):
        self._response = None
        return super(Request, self).__delitem__(self, item)

    @property
    def response(self):
        if self._response is None:
            self._response = requests.get(url=self.base_url, params=self)
        return self._response


class DataSetListRequest(Request):

    def __init__(self, UserID, ResultFormat='JSON', **params):
        required_params = {'UserID': UserID,
                           'Method': 'GetDataSetList',
                           'ResultFormat': ResultFormat}
        required_params.update(params)
        super(DataSetListRequest, self).__init__(**required_params)


class ParameterListRequest(Request):

    def __init__(self, UserID, DataSetName, ResultFormat='JSON', **params):
        required_params = {'UserID': UserID,
                           'Method': 'GetParameterList',
                           'DataSetName': DataSetName,
                           'ResultFormat': ResultFormat}
        required_params.update(params)
        super(ParameterListRequest, self).__init__(**required_params)


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


class RegionalDataRequest(Request):

    def __init__(self, UserID, KeyCode, ResultFormat='JSON', **params):
        required_params = {'UserID': UserID,
                           'Method': 'GetData',
                           'DataSetName': 'RegionalData',
                           'KeyCode': KeyCode,
                           'ResultFormat': ResultFormat}
        required_params.update(params)
        super(RegionalDataRequest, self).__init__(**required_params)


class NIPARequest(Request):

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


class NIUnderlyingDetailRequest(Request):

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


class FixedAssetsRequest(Request):

    def __init__(self, UserID, TableID, Year, ResultFormat='JSON', **params):
        required_params = {'UserID': UserID,
                           'Method': 'GetData',
                           'DataSetName': 'FixedAssets',
                           'TableID': TableID,
                           'Year': Year,
                           'ResultFormat': ResultFormat}
        required_params.update(params)
        super(FixedAssetsRequest, self).__init__(**required_params)
