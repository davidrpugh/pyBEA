"""
@author : David R. Pugh
@date : 2016-01-27


TODO
-----
1. Use ElementTree to implement XML parsing of BEA data.
2. Lots of documentation needs to be written! Mostly this can be copied
verbatim from the BEA user guide.

"""
import json

import requests


class Request(dict):
    """Base class for a Request."""

    _response = None

    base_url = 'http://www.bea.gov/api/data'

    valid_formats = ['JSON', 'XML']

    valid_methods = ['GetDataSetList',
                     'GetParameterList',
                     'GetParameterValues',
                     'GetParameterValuesFiltered',
                     'GetData',
                     ]

    def __init__(self, UserID, Method, ResultFormat='JSON', **params):
        # validate required keyword args
        valid_user_id = self._validate_user_id(UserID)
        valid_method = self._validate_method(Method)
        valid_format = self._validate_result_format(ResultFormat)

        required_params = {'UserID': valid_user_id,
                           'Method': valid_method,
                           'ResultFormat': valid_format}
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
        return self.response.json()

    def _load_xml_content(self):
        raise NotImplementedError

    def _validate_method(self, method):
        """Validate the Method keyword argument."""
        if not isinstance(method, str):
            mesg = "Method keyword argument must be a string, not a {}."
            raise AttributeError(mesg.format(method.__class__))
        elif method not in self.valid_methods:
            mesg = "Method keyword argument must be one of {}"
            raise AttributeError(mesg.format(str(self.valid_methods)))
        else:
            return method

    def _validate_result_format(self, fmt):
        """Validate the ResultFormat keyword argument."""
        if not isinstance(fmt, str):
            mesg = "ResultFormat keyword argument must be a string, not a {}."
            raise AttributeError(mesg.format(fmt.__class__))
        elif fmt not in self.valid_formats:
            mesg = "ResultFormat keyword argument must be one of {}"
            raise AttributeError(mesg.format(str(self.valid_formats)))
        else:
            return fmt

    def _validate_user_id(self, user_id):
        """Validate the UserID keyword argument."""
        if not isinstance(user_id, str):
            mesg = "UserID keyword argument must be a string, not a {}."
            raise AttributeError(mesg.format(user_id.__class__))
        else:
            return user_id


class DataSetListRequest(Request):

    def __init__(self, UserID, ResultFormat='JSON'):
        """
        Create an instance of the DataSetListRequest class.

        Parameters
        ----------
        UserID: str
            A valid UserID necessary for accessing the BEA data API.
        ResultFormat : str (default='JSON')
            The API returns data in one of two formats: JSON or XML. The
            ResultFormat parameter can be included on any request to specify
            the format of the results. The valid values for ResultFormat are
            `JSON' and 'XML'.

        """
        required_params = {'UserID': UserID,
                           'Method': 'GetDataSetList',
                           'ResultFormat': ResultFormat}
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

    def __init__(self, UserID, DataSetName, ResultFormat='JSON'):
        """
        Create an instance of the ParameterListRequest class.

        Parameters
        ----------
        UserID: str
            A valid UserID necessary for accessing the BEA data API.
        DataSetName : str
            A valid name of an available BEA data set.
        ResultFormat : str (default='JSON')
            The API returns data in one of two formats: JSON or XML. The
            ResultFormat parameter can be included on any request to specify
            the format of the results. The valid values for ResultFormat are
            'JSON' and 'XML'.

        """
        required_params = {'UserID': UserID,
                           'Method': 'GetParameterList',
                           'DataSetName': DataSetName,
                           'ResultFormat': ResultFormat}
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

    def __init__(self, UserID, DataSetName, ParameterName, ResultFormat='JSON'):
        """
        Create an instance of the ParameterValuesRequest class.

        Parameters
        ----------
        UserID: str
            A valid UserID necessary for accessing the BEA data API.
        DataSetName : str
            A valid name of an available BEA data set.
        ParameterName : str
            A valid parameter name for a given data set. Note that the
            get_parameter_list function returns a complete listing of valid
            parameters names for a given data set.
        ResultFormat : str (default='JSON')
            The API returns data in one of two formats: JSON or XML. The
            ResultFormat parameter can be included on any request to specify
            the format of the results. The valid values for ResultFormat are
            'JSON' and 'XML'.

        """
        required_params = {'UserID': UserID,
                           'Method': 'GetParameterValues',
                           'DataSetName': DataSetName,
                           'ParameterName': ParameterName,
                           'ResultFormat': ResultFormat}
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


class ParameterValuesFilteredRequest(ParameterValuesRequest):

    def __init__(self, UserID, DataSetName, ParameterName, ResultFormat='JSON', **kwargs):
        """
        Create an instance of the ParameterValuesRequest class.

        Parameters
        ----------
        UserID: str
            A valid UserID necessary for accessing the BEA data API.
        DataSetName : str
            A valid name of an available BEA data set.
        ParameterName : str
            A valid parameter name for a given data set. Note that the
            get_parameter_list function returns a complete listing of valid
            parameters names for a given data set.
        ResultFormat : str (default='JSON')
            The API returns data in one of two formats: JSON or XML. The
            ResultFormat parameter can be included on any request to specify
            the format of the results. The valid values for ResultFormat are
            'JSON' and 'XML'.
        kwargs : dict
            Additional, optional, keyword arguments.

        """
        required_params = {'UserID': UserID,
                           'Method': 'GetParameterValuesFiltered',
                           'DataSetName': DataSetName,
                           'ParameterName': ParameterName,
                           'ResultFormat': ResultFormat}
        super(ParameterValuesRequestFiltered, self).__init__(**required_params)


class DataRequest(Request):
    """Base class for a DataRequest."""

    def __init__(self, UserID, DataSetName, ResultFormat='JSON', **params):
        """
        Create an instance of the DataRequest class.

        Parameters
        ----------
        UserID: str
            A valid UserID necessary for accessing the BEA data API.
        DataSetName : str
            A valid name of an available BEA data set.
        ResultFormat : str (default='JSON')
            The API returns data in one of two formats: JSON or XML. The
            ResultFormat parameter can be included on any request to specify
            the format of the results. The valid values for ResultFormat are
            `JSON' and 'XML'.

        """
        required_params = {'UserID': UserID,
                           'Method': 'GetData',
                           'DataSetName': DataSetName,
                           'ResultFormat': ResultFormat}
        required_params.update(params)

        super(DataRequest, self).__init__(**required_params)

    @property
    def _json_data(self):
        return self.results['Data']

    @property
    def _json_dimensions(self):
        return self.results['Dimensions']

    @property
    def _json_notes(self):
        return self.results['Notes']

    @property
    def _xml_data(self):
        raise NotImplementedError

    @property
    def _xml_dimensions(self):
        raise NotImplementedError

    @property
    def _xml_notes(self):
        raise NotImplementedError

    @property
    def data(self):
        if self['ResultFormat'] == 'JSON':
            tmp_data = self._json_data
        else:
            tmp_data = self._xml_data
        return tmp_data

    @property
    def dimensions(self):
        if self['ResultFormat'] == 'JSON':
            tmp_dimensions = self._json_dimensions
        else:
            tmp_dimensions = self._xml_dimensions
        return tmp_dimensions

    @property
    def notes(self):
        if self['ResultFormat'] == 'JSON':
            tmp_notes = self._json_notes
        else:
            tmp_notes = self._xml_notes
        return tmp_notes


class RegionalProductRequest(DataRequest):

    def __init__(self, UserID, Component, IndustryId, GeoFips, ResultFormat='JSON', **params):
        r"""
        Create an instance of the RegionalProductRequest class.

        Parameters
        ----------
        UserID: str
            A valid UserID necessary for accessing the BEA data API.
        Component : str
            Component name.
        IndustryId: int
            Industry code of the Component.
        GeoFips : str or list(str)
            Comma-delimited list of state or MSA codes. Other values are 'STATE'
            for all states, and 'MSA' for all Metropolitan Statistical Areas.
        ResultFormat : str (default='JSON')
            The API returns data in one of two formats: JSON or XML. The
            ResultFormat parameter can be included on any request to specify
            the format of the results. The valid values for ResultFormat are
            'JSON' and 'XML'.
        params : dict
            Dictionary of optional parameters.

        Notes
        -----
        The optional parameters for RegionalIncomeRequest are:

        Year : str or list(str) (default='ALL')
            A string representation of the year for which data is being
            requested. Multiple years are requested by specifying them as a
            list: `Year=['2000', '2005' , '2010']`. Note that Year will default
            to all available years, 'ALL', if the parameter is not specified.
            Additional options are `LAST5` and `LAST10`.

        """
        required_params = {'UserID': UserID,
                           'Method': 'GetData',
                           'DataSetName': 'RegionalProduct',
                           'Component': Component,
                           'IndustryId': IndustryId,
                           'GeoFips': GeoFips,
                           'ResultFormat': ResultFormat}
        required_params.update(params)
        super(RegionalProductRequest, self).__init__(**required_params)


class RegionalIncomeRequest(DataRequest):

    def __init__(self, UserID, TableName, LineCode, GeoFips, ResultFormat='JSON', **params):
        r"""
        Create an instance of the RegionalIncomeRequest class.

        Parameters
        ----------
        UserID: str
            A valid UserID necessary for accessing the BEA data API.
        TableName : str
            Published table name.
        LineCode : int
            Line code in table.
        GeoFips : str or list(str)
            Comma-delimited list of 5-character geographic codes; 'COUNTY' for
            all counties, 'STATE' for all states, 'MSA' for all Metropolitan
            Statistical Areas, 'MIC' for all Micropolitan Areas, 'PORT' for all
            state metropolitan/nonmetropolitan portions, 'DIV' for all
            Metropolitan Divisions, 'CSA' for all Combined Statistical Areas,
            state post office abbreviation for all counties in one state
            (e.g. 'NY').
        ResultFormat : str (default='JSON')
            The API returns data in one of two formats: JSON or XML. The
            ResultFormat parameter can be included on any request to specify
            the format of the results. The valid values for ResultFormat are
            'JSON' and 'XML'.
        params : dict
            Dictionary of optional parameters.

        Notes
        -----
        The optional parameters for RegionalIncomeRequest are:

        Year : str or list(str) (default='LAST5')
            A string representation of the year for which data is being
            requested. Multiple years are requested by specifying them as a
            list: `Year=['2000', '2005' , '2010']`. Note that Year will default
            to last five available years, 'LAST5', if the parameter is not
            specified. Additional options are `LAST10` and `ALL`.

        """
        required_params = {'UserID': UserID,
                           'Method': 'GetData',
                           'DataSetName': 'RegionalIncome',
                           'TableName': TableName,
                           'LineCode': LineCode,
                           'GeoFips': GeoFips,
                           'ResultFormat': ResultFormat}
        required_params.update(params)
        super(RegionalIncomeRequest, self).__init__(**required_params)


class NIPARequest(DataRequest):

    def __init__(self, UserID, TableID, Frequency, Year="X", ResultFormat='JSON', **params):
        """
        Create an instance of the NIPARequest class.

        Parameters
        ----------
        UserID: str
            A valid UserID necessary for accessing the BEA data API.
        TableID : str
            The TableID parameter is an integer that refers to a specific NIPA
            table. Note that the list of valid TableIDs may change depending on
            the monthly news release cycles.
        Frequency : str or list(str)
            The Frequency parameter is a string that refers to the time series
            for the requested NIPA table. Multiple frequencies are requested by
            specifying them as a list: `Frequency=['A', 'Q' , 'M']`. When data
            is requested for frequencies that don't exist for a particular NIPA
            table, only data that exists is returned.
        Year : str or list(str) (default='X' for all available years)
            A string representation of the year for which data is being
            requested. Multiple years are requested by specifying them as a
            list: `Year=['2000', '2005' , '2010']`. Note that Year will default
            to all available years if the parameter is not specified.
        ResultFormat : str (default='JSON')
            The API returns data in one of two formats: JSON or XML. The
            ResultFormat parameter can be included on any request to specify
            the format of the results. The valid values for ResultFormat are
            'JSON' and 'XML'.
        params : dict
            Dictionary of optional parameters. Note that the list of valid
            optional parameters is data set specific.

        Notes
        -----
        The optional parameters for NIPADataRequest are:

        ShowMillions : str
            The ShowMillions parameter is a string indicating whether the data
            for the requested NIPA table should be returned in million-dollar
            units. Million-dollar estimate data doesn't exist for all tables,
            and data is returned in million-dollar units only if available.
            When million-dollar data doesn't exist for a table, data is
            returned as if million-dollar data was not requested.

        """
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

    def __init__(self, UserID, TableID, Frequency, Year, ResultFormat='JSON'):
        """
        Create an instance of the NIUnderlyingDetailRequest class.

        Parameters
        ----------
        UserID: str
            A valid UserID necessary for accessing the BEA data API.
        TableID : str
            The TableID parameter is an integer that refers to a specific NIPA
            table.
        Frequency : str or list(str)
            The Frequency parameter is a string that refers to the time series
            for the requested NIPA table. Multiple frequencies are requested by
            specifying them as a list: `Frequency=['A', 'Q' , 'M']`. When data
            is requested for frequencies that don't exist for a particular NIPA
            table, only data that exists is returned.
        Year : str or list(str) (default='ALL')
            A string representation of the year for which data is being
            requested. Multiple years are requested by specifying them as a
            list: `Year=['2000', '2005' , '2010']`. Note that Year will default
            to all available years if the parameter is not specified.
        ResultFormat : str (default='JSON')
            The API returns data in one of two formats: JSON or XML. The
            ResultFormat parameter can be included on any request to specify
            the format of the results. The valid values for ResultFormat are
            'JSON' and 'XML'.

        """
        required_params = {'UserID': UserID,
                           'Method': 'GetData',
                           'DataSetName': 'NIUnderlyingDetail',
                           'TableID': TableID,
                           'Frequency': Frequency,
                           'Year': Year,
                           'ResultFormat': ResultFormat}
        super(NIUnderlyingDetailRequest, self).__init__(**required_params)


class FixedAssetsRequest(DataRequest):

    def __init__(self, UserID, TableID, Year, ResultFormat='JSON'):
        """
        Create an instance of the FixedAssetsRequest class.

        Parameters
        ----------
        UserID: str
            A valid UserID necessary for accessing the BEA data API.
        TableID : str
            The TableID parameter is an integer that refers to a specific
            FixedAssets table.
        Year : str or list(str) (default='ALL')
            A string representation of the year for which data is being
            requested. Multiple years are requested by specifying them as a
            list: `Year=['2000', '2005' , '2010']`. Note that Year will default
            to all available years if the parameter is not specified.
        ResultFormat : str (default='JSON')
            The API returns data in one of two formats: JSON or XML. The
            ResultFormat parameter can be included on any request to specify
            the format of the results. The valid values for ResultFormat are
            'JSON' and 'XML'.

        """
        required_params = {'UserID': UserID,
                           'Method': 'GetData',
                           'DataSetName': 'FixedAssets',
                           'TableID': TableID,
                           'Year': Year,
                           'ResultFormat': ResultFormat}
        super(FixedAssetsRequest, self).__init__(**required_params)
