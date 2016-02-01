"""
@author : David R. Pugh
@date : 2016-01-31


TODO
-----
1. Use ElementTree to implement XML parsing of BEA data.

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
        return json.loads(self.response.content.decode())

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


class RegionalDataRequest(DataRequest):
    """
    The new datasets RegionalIncome and RegionalProduct have more statistics and industry detail than the RegionalData dataset. See Appendices I and J. Although RegionalData is still valid, we encourage users to switch to the more comprenhensive datasets RegionalIncome and RegionalProduct.

    The RegionalData dataset contains estimates from the Regional Economic Accounts. These include estimates of GDP by state and metropolitan area; estimates of personal income and employment by state, metropolitan area, and county; and regional price parities by state and MSA.

    """

    def __init__(self, UserID, KeyCode, ResultFormat='JSON', **params):
        r"""
        Create an instance of the RegionalDataRequest class.

        Parameters
        ----------
        UserID: str
            A valid UserID necessary for accessing the BEA data API.
        KeyCode : str
            KeyCode specifies a statistic drawn from the regional income and product accounts public tables. Exactly one KeyCode must be provided.
        ResultFormat : str (default='JSON')
            The API returns data in one of two formats: JSON or XML. The
            ResultFormat parameter can be included on any request to specify
            the format of the results. The valid values for ResultFormat are
            'JSON' and 'XML'.
        params : dict
            Dictionary of optional parameters.

        Notes
        -----
        The optional parameters for RegionalDataRequest are:

        GeoFips : str, int or list(int)
            GeoFips specifies geography. It can be all states ("STATE"), all counties ("COUNTY"), or all MSAs ("MSA"). It can also be a list of ANSI state-county codes or metropolitan statistical area codes. For example, the counties in Connecticut:

            .. code-block:: python

                GeoFips=list(09001,09003,09005,09007,09009,09011,09013,09015)

            GeoFips will default to all states, counties, or MSAs, if not specified. State, county, and metropolitan statistical area FIPS codes can be obtained from the `Census`_. A comprehensive list of MSAs and their component counties can be accessed on the `BEA website`_.
        Year : str, int or list(int)
            A string representation of the year for which data is being
            requested. Multiple years are requested by specifying them as a
            list:

            .. code-block:: python
                Year=[2000, 2005, 2010]

            Note that Year will default to all available years if the parameter is not specified.

        .. _`Census`: http://www.census.gov/geo/www/ansi/ansi.html
        .. _`BEA website`: http://www.bea.gov/regional/docs/msalist.cfm

        """
        required_params = {'UserID': UserID,
                           'Method': 'GetData',
                           'DataSetName': 'RegionalData',
                           'KeyCode': KeyCode,
                           'ResultFormat': ResultFormat}
        query_params = required_params.update(params)
        super(RegionalDataRequest, self).__init__(**query_params)


class NIPARequest(DataRequest):
    """
    The NIPA dataset contains data from the standard set of NIPA tables as published in the Survey of Current Business. Availability of updated NIPA data follows the BEA News Release schedule as posted on the BEA web site. The NIPA dataset may be unavailable for a few minutes preceding the monthly GDP release while data is being updated (as it is for all other methods of acquiring newly released data).

    """

    def __init__(self, UserID, TableID, Frequency, Year, ResultFormat='JSON',
                 **params):
        r"""
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
            specifying them as a list:

            .. code-block :: python

                Frequency=['A', 'Q' , 'M']

            When data is requested for frequencies that don't exist for a particular NIPA table, only data that exists is returned.
        Year : str, int or list(int)
            A string representation of the year for which data is being
            requested. Multiple years are requested by specifying them as a
            list:

            .. code-block:: python
                Year=[2000, 2005, 2010]

            Note that Year will default to all available years if the parameter is not specified.
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
        query_params = required_params.update(params)
        super(NIPARequest, self).__init__(**query_params)


class NIUnderlyingDetailRequest(DataRequest):
    """
    The NIUnderlyingDetail dataset contains detailed estimate data from underlying NIPA series that appear in the national income and product account (NIPA) tables as published in the Survey of Current Business.

    """

    def __init__(self, UserID, TableID, Frequency, Year, ResultFormat='JSON'):
        r"""
        Create an instance of the NIUnderlyingDetailRequest class.

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
            specifying them as a list:

            .. code-block :: python

                Frequency=['A', 'Q' , 'M']

            When data is requested for frequencies that don't exist for a particular NIPA table, only data that exists is returned.
        Year : str, int or list(int)
            A string representation of the year for which data is being
            requested. Multiple years are requested by specifying them as a
            list:

            .. code-block:: python
                Year=[2000, 2005, 2010]

            Note that Year will default to all available years if the parameter is not specified.
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
    """
    The FixedAssets dataset contains data from the standard set of Fixed Assets tables as published online.

    """

    def __init__(self, UserID, TableID, Year, ResultFormat='JSON'):
        r"""
        Create an instance of the FixedAssetsRequest class.

        Parameters
        ----------
        UserID: str
            A valid UserID necessary for accessing the BEA data API.
        TableID : str
            The TableID parameter is an integer that refers to a specific
            FixedAssets table.
        Year : str, int or list(int)
            A string representation of the year for which data is being
            requested. Multiple years are requested by specifying them as a
            list:

            .. code-block:: python
                Year=[2000, 2005, 2010]

            Note that Year will default to all available years if the parameter is not specified.
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


class InputOutputRequest(DataRequest):
    """
    The Input-Output Statistics are contained within a dataset called InputOutput. BEA's industry accounts are used extensively by policymakers and businesses to understand industry interactions, productivity trends, and the changing structure of the U.S. economy. The input-output accounts provide a detailed view of the interrelationships between U.S. producers and users. The Input-Output dataset contains Make Tables, Use Tables, and Direct and Total Requirements tables.

    """

    def __init__(self, UserID, TableID, Year='ALL', ResultFormat='JSON'):
        r"""
        Create an instance of the InputOutputRequest class.

        Parameters
        ----------
        UserID: str
            A valid UserID necessary for accessing the BEA data API.
        TableID : str, int or list(int)
            The TableID parameter is an integer that refers to a specific
            InputOutput table. Multiple years are requested by specifying them as a list as follows:

            .. code-block :: python

                TableID=[47, 48, 49]

        Year : str, int or list(int)
            A string representation of the year for which data is being
            requested. Multiple years are requested by specifying them as a
            list:

            .. code-block:: python
                Year=[2000, 2005, 2010]

            Note that Year will default to all available years if the parameter is not specified.
        ResultFormat : str (default='JSON')
            The API returns data in one of two formats: JSON or XML. The
            ResultFormat parameter can be included on any request to specify
            the format of the results. The valid values for ResultFormat are
            'JSON' and 'XML'.

        """
        required_params = {'UserID': UserID,
                           'Method': 'GetData',
                           'DataSetName': 'InputOutput',
                           'TableID': TableID,
                           'Year': Year,
                           'ResultFormat': ResultFormat}
        super(InputOutputRequest, self).__init__(**required_params)


class DirectInvestmentMNEsRequest(DataRequest):
    """
    This data set contains statistics on income and financial transactions in direct investment that underlie the U.S. balance of payments statistics, and direct investment positions that underlie the U.S. international investment positions.

    """

    def __init__(self, UserID, DirectionOfInvestment, Classification,
                 Year='ALL', ResultFormat='JSON', **params):
        r"""
        Create an instance of the DirectInvestmentMNEsRequest class.

        Parameters
        ----------
        UserID : str
            A valid UserID necessary for accessing the BEA data API.
        DirectionOfInvestment : str
            DirectionOfInvestment can take on two values: "Outward" for data on transactions and positions between foreign affiliates and their U.S. parent enterprises; "Inward" for data on transactions and positions between U.S. affiliates and their foreign parent groups.
        Classification : str
            Classification can take on four values: "Country" for a total value by country only; "Industry" for a total value by industry only; "CountryByIndustry" for a country broken out by industry (where available); "IndustryByCountry" for an industry broken out by country (where available);
        Year : str, int or list(int) (default="ALL")
            A string representation of the year for which data is being
            requested. Multiple years are requested by specifying them as a
            list:

            .. code-block:: python
                Year=[2000, 2005, 2010]

            Note that Year will default to all available years if the parameter is not specified.
        ResultFormat : str (default='JSON')
            The API returns data in one of two formats: JSON or XML. The
            ResultFormat parameter can be included on any request to specify
            the format of the results. The valid values for ResultFormat are
            'JSON' and 'XML'.

        Notes
        -----
        The optional parameters for DirectInvestmentMNEsRequest are:

        SeriesID : str, int, or list(int)

        Country : str, int, or list(int)
            Refer to the GetParameterValuesRequest API call above for the list of three-digit country and region identification values. Use ‘000’ for the total of all countries and ‘all’ for all available countries and regions. Separate multiple values with a comma.
        Industry : str, int, or list(int)
            Refer to the GetParameterValuesRequest API call abovefor the list of four-digit industry identification values. These generally follow the North American Industry Classification System (NAICS). Use ‘0000’ for the all- industries total and ‘all’ for all available industries. Separate multiple values with a comma.
        State : str, int, or list(int)
            At the state level data are only available on employment and (for 2007 and earlier years), property, plant, and equipment.

            Refer to the GetParameterValuesRequest API call above for the list of the two-digit Federal Information Processing Standards (FIPS) codes, or the FIPS codes found at this `link`_: . Use ‘70’ for “Other U.S. Areas”, ‘75’ for “Foreign”, ‘00’ for total U.S., and ‘all’ for all states and areas. Separate multiple values with a comma.

        .. _`link`: http://www.epa.gov/envirofw/html/codes/state.html

        """
        required_params = {'UserID': UserID,
                           'DirectionOfInvestment': DirectionOfInvestment,
                           'Classification': Classification,
                           'Method': 'GetData',
                           'DataSetName': 'MNE',
                           'Year': Year,
                           'ResultFormat': ResultFormat}
        query_params = required_params.update(params)
        super(DirectInvestmentMNEsRequest, self).__init__(**query_params)
