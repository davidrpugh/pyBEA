"""
Functions for fetching data from the Bureau of Economic Analysis (BEA) data api.
"""
import numpy as np
import pandas as pd
import sys
import os

PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pybea')
sys.path.append(PATH)
import api

global JSON_ERROR
JSON_ERROR = ''


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

    return tmp_request.data_set_list


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
    return tmp_request.parameter_list


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
    # return tmp_request.parameter_values
    temp = tmp_request._json_content
    temp = temp['BEAAPI']['Results']['ParamValue']
    df = pd.DataFrame(temp)
    return df


def get_parameter_values_filtered(UserID, DataSetName, ParameterName,
                                  ResultFormat='JSON', **kwargs):
    """
    Retrieves a list of the valid values for a particular parameter based on
    other provided parameters .

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
    kwargs : dict
        Additional, optional, keyword arguments.

    Returns
    -------
    param_values : Pandas.DataFrame
        A Pandas DataFrame containing the list of valid parameter values for
        the given data set.

    """
    tmp_request = api.ParameterValuesRequest(UserID=UserID,
                                             DataSetName=DataSetName,
                                             ParameterName=ParameterName,
                                             ResultFormat=ResultFormat,
                                             **kwargs)
    param_values = pd.DataFrame(tmp_request.parameter_values, dtype=np.int64)
    return param_values


def get_data(UserID, DataSetName, ResultFormat='JSON', **params):
    """
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

    For additional information see the BEA data API `user guide`_.

    .. _`user guide`: https://www.bea.gov/API/bea_web_service_api_user_guide.htm

    """
    valid_dataset_names = ['NIPA', 'NIUnderlyingDetail', 'FixedAssets', 'MNE',
                           'GDPbyIndustry', 'ITA', 'IIP',
                           'Regional', 'InputOutput',
                           'UnderlyingGDPbyIndustry', 'IntlServTrade']

    df = get_parameter_list(UserID, DataSetName)
    dtypes = {}
    for i in df.index:
        dtypes[df.loc[i]['ParameterName']] = df.loc[i]['ParameterDataType']

    if DataSetName in valid_dataset_names:
        # Format request for Data
        tmp_request = api.DataRequest(UserID, DataSetName, ResultFormat, **params)

        # This is the API call
        json_content = tmp_request._json_content

        data = {}
        # This modifies the json response based on the various ways the return data is structured.
        global JSON_ERROR
        JSON_ERROR = ''

        try:
            data = json_content['BEAAPI']['Results']['Data']
        except (TypeError, KeyError):
            if DataSetName == 'IIP':
                try:
                    data = json_content['BEAAPI']['Data']
                except (KeyError, TypeError):
                    pass
            else:
                try:
                    data = json_content['BEAAPI']['Results']
                    data = data[0]['Data']
                except (KeyError, TypeError):
                    pass
        try:
            JSON_ERROR = json_content['BEAAPI']['Error']['ErrorDetail']['Description']
        except:
            pass

        df = pd.DataFrame(data)
        return df

    else:
        raise ValueError("Invalid DataSetName requested.")

    return df



