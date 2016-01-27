"""
Functions for fetching data from the Bureau of Economic Analysis (BEA) data api.

@author : David R. Pugh
@date : 2016-01-27

"""
import numpy as np
import pandas as pd

from . import api


def get_data_set_list(UserID, ResultFormat='JSON'):
    """
    Retrieve list of currently available data sets.

    Parameters
    ----------
    UserID: str
            A valid UserID necessary for accessing the BEA data API.
    ResultFormat : str (default='JSON')
        The API returns data in one of two formats: JSON or XML. The
        ResultFormat parameter can be included on any request to specify the
        format of the results.

    Returns
    -------
    data_set_list : Pandas.DataFrame
        A Pandas DataFrame containing the DatasetName and DatasetDescription
        attributes for all available data sets.

    """
    tmp_request = api.DataSetListRequest(UserID=UserID, ResultFormat=ResultFormat)
    data_set_list = pd.DataFrame(tmp_request.data_set, dtype=np.int64)
    return data_set_list


def get_parameter_list(UserID, DataSetName, ResultFormat='JSON'):
    """
    Retrieve list of required and optional parameters for a given data set.

    Parameters
    ----------
    UserID: str
            A valid UserID necessary for accessing the BEA data API.
    DataSetName : str
        A valid name of an available BEA data set. The get_data_set_list
        function returns a complete listing of available data sets and the
        associated DataSetName attributes.
    ResultFormat : str (default='JSON')
        The API returns data in one of two formats: JSON or XML. The
        ResultFormat parameter can be included on any request to specify the
        format of the results.

    Returns
    -------
    parameter_list : Pandas.DataFrame
        A Pandas DataFrame containing the metadata associated with the
        parameters of the requested data set.

    Notes
    -----
    The function returns the following metadata for each required and optional
    parameter in the specified data set.

    - ParameterName: the name of the parameter as used in a data request
    - ParameterDataType: String or Integer
    - ParameterDescription: a description of the parameter
    - ParameterIsRequired: 0 if the parameter can be omitted from a request, 1
    if required.
    - ParameterDefaultValue: the default value used for the request if the
    parameter is not supplied
    - MultipleAcceptedFlag: 0 if the parameter may only have a single value, 1
    if multiple values are permitted. Note that multiple values for a parameter
    are submitted as a comma-separated string.
    - AllValue: the special value for a parameter that means all valid values
    are used without supplying them individually.

    """
    tmp_request = api.ParameterListRequest(UserID=UserID,
                                           DataSetName=DataSetName,
                                           ResultFormat=ResultFormat)
    parameter_list = pd.DataFrame(tmp_request.parameter_list, dtype=np.int64)
    return parameter_list


def get_parameter_values(UserID, DataSetName, ParameterName, ResultFormat='JSON'):
    """
    Retrieve list of valid parameter values for a given data set.

    Parameters
    ----------
    UserID: str
            A valid UserID necessary for accessing the BEA data API.
    DataSetName : str
        A valid name of an available BEA data set. Note that the
        get_data_set_list function returns a complete listing of available data
        sets and their associated DataSetName attributes.
    ParameterName : str
        A valid parameter name for a given data set. Note that the
        get_parameter_list function returns a complete listing of valid
        parameters names for a given data set.
    ResultFormat : str (default='JSON')
        The API returns data in one of two formats: JSON or XML. The
        ResultFormat parameter can be included on any request to specify the
        format of the results.

    Returns
    -------
    param_values : Pandas.DataFrame
        A Pandas DataFrame containing the list of valid parameter values for
        the given data set.

    """
    tmp_request = api.ParameterValuesRequest(UserID=UserID,
                                             DataSetName=DataSetName,
                                             ParameterName=ParameterName,
                                             ResultFormat=ResultFormat)
    param_values = pd.DataFrame(tmp_request.parameter_values, dtype=np.int64)
    return param_values


def get_data(UserID, DataSetName, ResultFormat='JSON', **params):
    r"""
    Retrieve data from the Bureau of Economic Analysis (BEA) data api.

    Parameters
    ----------
    UserID: str
            A valid UserID necessary for accessing the BEA data API.
    DataSetName : str
        A valid name of an available BEA data set. The get_data_set_list
        function returns a complete listing of available data sets and the
        associated DataSetName attributes.
    ResultFormat : str (default='JSON')
        The API returns data in one of two formats: JSON or XML. The
        ResultFormat parameter can be included on any request to specify the
        format of the results.
    params : dict
        Dictionary of optional parameters. The list of valid optional
        parameters is data set specific. See the notes section below for more
        information.

    Returns
    -------
    data : Pandas.DataFrame
        A Pandas DataFrame containing the requested data.

    Notes
    -----
    As noted above the additional required and optional parameters that can be
    passed as parameters is data set specific.

    The following parameters may be passed with DataSetName='RegionalData':

    KeyCodes : list(str), required
        List of valid KeyCode parameters indicating the variables of interest.
    GeoFips : str or list(str), optional (default='STATE')
        List of valid FIPS codes for the geographical locations of interest.
        State, county, and metropolitan statistical area FIPS codes can be
        obtained from the `Census Bureau`_. A comprehensive list of MSAs
        and their component counties is available on the `BEA website`_.
    Year : str or list(str), optional (default='ALL')
        A string representation of the year for which data is being
        requested. Multiple years are requested by passing them as a list
        as follows: `Year=['2000', '2005' , '2010']`. Note that Year will
        default to all available years if the parameter is not specified.

    For additional information see the BEA data API `user guide`_.

    .. _`Census Bureau`: http://www.census.gov/geo/www/ansi/ansi.html
    .. _`BEA website`: http://www.bea.gov/regional/docs/msalist.cfm
    .. _`user guide`: http://www.bea.gov/api/_pdf/bea_web_service_api_user_guide.pdf

    """
    if DataSetName == 'RegionalData':
        data = _get_RegionalData(UserID=UserID, ResultFormat=ResultFormat,
                                 **params)
    elif DataSetName == 'NIPA':
        data = _get_NIPA(UserID=UserID, ResultFormat=ResultFormat,
                         **params)
    elif DataSetName == 'NIUnderlyingDetail':
        data = _get_NIUnderlyingDetail(UserID=UserID, ResultFormat=ResultFormat,
                                       **params)
    elif DataSetName == 'FixedAssets':
        data = _get_FixedAssets(UserID=UserID, ResultFormat=ResultFormat,
                                **params)
    else:
        raise ValueError("Invalid DataSetName requested.")

    return data


def _get_RegionalData(UserID, ResultFormat, KeyCodes, **params):
    """Combines data on multiple KeyCodes into a single Pandas DataFrame."""
    dfs = []
    for KeyCode in KeyCodes:
        tmp_request = api.RegionalDataRequest(UserID=UserID,
                                              Method='GetData',
                                              ResultFormat=ResultFormat,
                                              KeyCode=KeyCode,
                                              **params)
        tmp_df = pd.DataFrame(tmp_request.data, dtype=np.int64)
        dfs.append(tmp_df)

    combined_df = pd.concat(dfs)

    return combined_df


def _get_NIPA(UserID, ResultFormat, **params):
    raise NotImplementedError


def _get_NIUnderlyingDetail(UserID, ResultFormat, **params):
    raise NotImplementedError


def _get_FixedAssets(UserID, ResultFormat, **params):
    raise NotImplementedError
