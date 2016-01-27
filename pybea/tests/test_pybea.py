"""
Tests for pybea.py module.

@author : David R. Pugh
@date : 2016-01-27

"""
import nose
import pandas as pd

from .. import pybea


USER_ID = '98A0A0A7-21DF-4B75-96DE-1410D47AB280'


def test_get_data_set_list():
    """Testing function for grabbing list of available data sets."""
    df = pybea.get_data_set_list(UserID=USER_ID)
    nose.tools.assert_is_instance(df, pd.DataFrame)
    nose.tools.assert_equals(df.shape, (12, 2))


def test_get_parameter_list():
    """Testing function for grabbing list of parameters for a data set."""
    df = pybea.get_parameter_list(UserID=USER_ID, DataSetName='FixedAssets')
    nose.tools.assert_is_instance(df, pd.DataFrame)
    nose.tools.assert_equals(df.shape, (2, 7))


def test_get_parameter_values():
    """Testing function for grabbing list of values for a parameter."""
    df = pybea.get_parameter_values(UserID=USER_ID,
                                    DataSetName='RegionalData',
                                    ParameterName='Year')
    nose.tools.assert_is_instance(df, pd.DataFrame)
    nose.tools.assert_equals(df.shape, (117, 2))


def test_get_data_set():
    """Testinf function for grabbing data."""
    df = pybea.get_data(UserID=USER_ID,
                        DataSetName='RegionalData',
                        KeyCodes=['POP_MI'],
                        GeoFips='MSA',
                        Year=['2000', '2005', '2010'])
    nose.tools.assert_is_instance(df, pd.DataFrame)
    nose.tools.assert_equals(df.shape, (1146, 8))

    with nose.tools.assert_raises(ValueError):
        pybea.get_data(UserID=USER_ID, DataSetName='InvalidDataSetName')
