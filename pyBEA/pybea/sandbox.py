"""
TODO:

1. Create functions out of the subclasses of the Request object.

"""
import numpy as np
import pandas as pd

from api import *


def get_data_set_list(UserID, ResultFormat='JSON', **params):
    tmp_request = Request(UserID=UserID,
                          Method='GetDataSetList',
                          ResultFormat=ResultFormat,
                          **params)

    return tmp_request.response.content


def get_parameter_list(UserID, DataSetName, ResultFormat='JSON', **params):
    tmp_request = Request(UserID=UserID,
                          Method='GetParameterList',
                          DataSetName=DataSetName,
                          ResultFormat=ResultFormat,
                          **params)

    return tmp_request.response.content


def get_parameter_values(self, UserID, DataSetName, ParameterName,
                         ResultFormat='JSON', **params):
    tmp_request = Request(UserID=UserID,
                          Method='GetParameterValues',
                          DataSetName=DataSetName,
                          ParameterName=DataSetName,
                          ResultFormat=ResultFormat,
                          **params)

    return tmp_request.response.content


def get_data(UserID, DataSetName, ResultFormat='JSON', **params):
    """
    Retrieve data from the Bureau of Economic Analysis (BEA) data api.

    Parameters
    ----------
    UserID : str

    DataSetName : str

    ResultFormat : str

    params : dict

    Returns
    -------
    data : Pandas.DataFrame
        A Pandas DataFrame containing the requested data.

    """
    if DataSetName == 'RegionalData':
        tmp_request = RegionalDataRequest(UserID=UserID,
                                          Method='GetData',
                                          ResultFormat=ResultFormat,
                                          **params)
    elif DataSetName == 'NIPA':
        tmp_request = NIPARequest(UserID=UserID,
                                  Method='GetData',
                                  ResultFormat=ResultFormat,
                                  **params)
    elif DataSetName == 'NIUnderlyingDetail':
        tmp_request = NIPARequest(UserID=UserID,
                                  Method='GetData',
                                  ResultFormat=ResultFormat,
                                  **params)
    elif DataSetName == 'FixedAssets':
        tmp_request = NIPARequest(UserID=UserID,
                                  Method='GetData',
                                  ResultFormat=ResultFormat,
                                  **params)
    else:
        raise ValueError("Invalid DataSetName requested.")

    # convert to DataFrame
    tmp_df = pd.DataFrame(tmp_request.data, dtype=np.int64)

    return tmp_df
