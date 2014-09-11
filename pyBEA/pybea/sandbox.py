"""
TODO:

1. Create functions out of the subclasses of the Request object.

"""
from api import Request


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
    tmp_request = Request(UserID=UserID,
                          Method='GetData',
                          DataSetName=DataSetName,
                          ParameterName=DataSetName,
                          ResultFormat=ResultFormat,
                          **params)

    return tmp_request.response.content
