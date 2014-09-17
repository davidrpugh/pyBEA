"""
@author : David R. Pugh
@date : 2014-09-09

"""
import numpy as np
import pandas as pd

import api


def get_data_set_list(UserID, ResultFormat='JSON'):
    """
    Retrieve list of currently available data sets.

    Parameters
    ----------
    UserID : str
        Before using the API, users must obtain a unique 36-character UserID by
        registering at http://www.bea.gov/api/signup/.
    ResultFormat : str (default='JSON')
        The API returns data in one of two formats: JSON or XML. The
        ResultFormat parameter can be included on any request to specify the
        format of the results. If ResultFormat is not supplied on the request,
        or an invalid ResultFormat is specified, the default format returned is
        JSON. The valid values for ResultFormat are 'JSON' and 'XML'.

    Returns
    -------
    data_set_list : Pandas.DataFrame
        A Pandas DataFrame containing the DatasetName and DatasetDescription
        attributes for all available data sets.

    """
    tmp_request = api.DataSetListRequest(UserID=UserID,
                                         ResultFormat=ResultFormat,
                                         )
    data_set_list = pd.DataFrame(tmp_request.data_set, dtype=np.int64)
    return data_set_list


def get_parameter_list(UserID, DataSetName, ResultFormat='JSON'):
    """
    Retrieve list of required and optional parameters for a given data set.

    Parameters
    ----------
    UserID : str
        Before using the API, users must obtain a unique 36-character UserID by
        registering at http://www.bea.gov/api/signup/.
    DataSetName : str
        A valid name of an available BEA data set. The get_data_set_list
        function returns a complete listing of available data sets and the
        associated DataSetName attributes.
    ResultFormat : str (default='JSON')
        The API returns data in one of two formats: JSON or XML. The
        ResultFormat parameter can be included on any request to specify the
        format of the results. If ResultFormat is not supplied on the request,
        or an invalid ResultFormat is specified, the default format returned is
        JSON. The valid values for ResultFormat are 'JSON' and 'XML'.

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
                                           ResultFormat=ResultFormat,
                                           )
    parameter_list = pd.DataFrame(tmp_request.parameter_list, dtype=np.int64)
    return parameter_list


def get_parameter_values(UserID, DataSetName, ParameterName, ResultFormat='JSON'):
    """
    Retrieve list of valid parameter values for a given data set.

    Parameters
    ----------
    UserID : str
        Before using the API, users must obtain a unique 36-character UserID by
        registering at http://www.bea.gov/api/signup/.
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
        format of the results. If ResultFormat is not supplied on the request,
        or an invalid ResultFormat is specified, the default format returned is
        JSON. The valid values for ResultFormat are 'JSON' and 'XML'.

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
                                             )
    param_values = pd.DataFrame(tmp_request.parameter_values, dtype=np.int64)
    return param_values


def get_data(UserID, DataSetName, ResultFormat='JSON', **params):
    r"""
    Retrieve data from the Bureau of Economic Analysis (BEA) data api.

    Parameters
    ----------
    UserID : str
        Before using the API, users must obtain a unique 36-character UserID by
        registering at http://www.bea.gov/api/signup/.
    DataSetName : str
        A valid name of an available BEA data set. The get_data_set_list
        function returns a complete listing of available data sets and the
        associated DataSetName attributes.
    ResultFormat : str (default='JSON')
        The API returns data in one of two formats: JSON or XML. The
        ResultFormat parameter can be included on any request to specify the
        format of the results. If ResultFormat is not supplied on the request,
        or an invalid ResultFormat is specified, the default format returned is
        JSON. The valid values for ResultFormat are 'JSON' and 'XML'.
    params : dict
        Dictionary of optional parameters. Note that the list of valid optional
        parameters is data set specific. The get_parameter_list function will
        return a complete listing of all required and optional parameters for
        a given data set.

    Returns
    -------
    data : Pandas.DataFrame
        A Pandas DataFrame containing the requested data.

    Notes
    -----
    For additional information see the BEA data API `user guide`_.

    .. _`user guide`: http://www.bea.gov/api/_pdf/bea_web_service_api_user_guide.pdf

    """
    if DataSetName == 'RegionalData':
        tmp_request = api.RegionalDataRequest(UserID=UserID,
                                              Method='GetData',
                                              ResultFormat=ResultFormat,
                                              **params)
    elif DataSetName == 'NIPA':
        tmp_request = api.NIPARequest(UserID=UserID,
                                      Method='GetData',
                                      ResultFormat=ResultFormat,
                                      **params)
    elif DataSetName == 'NIUnderlyingDetail':
        tmp_request = api.NIPARequest(UserID=UserID,
                                      Method='GetData',
                                      ResultFormat=ResultFormat,
                                      **params)
    elif DataSetName == 'FixedAssets':
        tmp_request = api.NIPARequest(UserID=UserID,
                                      Method='GetData',
                                      ResultFormat=ResultFormat,
                                      **params)
    else:
        raise ValueError("Invalid DataSetName requested.")

    data = pd.DataFrame(tmp_request.data, dtype=np.int64)
    return data
