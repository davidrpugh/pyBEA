"""
Tests for pybea.py module.

@author : David R. Pugh
@date : 2014-09-22

"""
import nose
import pandas as pd

from .. import pybea


def test_get_data_set_list():
    """Testing function for grabbing list of available data sets."""
    df = pybea.get_data_set_list()
    nose.tools.assert_is_instance(df, pd.DataFrame)
    nose.tools.assert_equals(df.shape, (4, 2))


def test_get_parameter_list():
    """Testing function for grabbing list of parameters for a data set."""
    df = pybea.get_parameter_list(DataSetName='FixedAssets')
    nose.tools.assert_is_instance(df, pd.DataFrame)
    nose.tools.assert_equals(df.shape, (2, 6))


def test_get_parameter_values():
    """Testing function for grabbing list of values for a parameter."""
    df = pybea.get_parameter_values(DataSetName='RegionalData',
                                    ParameterName='Year')
    nose.tools.assert_is_instance(df, pd.DataFrame)
    nose.tools.assert_equals(df.shape, (85, 2))


def test_get_data_set():
    """Testinf function for grabbing data."""
    df = pybea.get_data(DataSetName='RegionalData',
                        KeyCode='POP_MI',
                        GeoFips='MSA',
                        Year=['2000', '2005', '2010'])
    nose.tools.assert_is_instance(df, pd.DataFrame)
    nose.tools.assert_equals(df.shape, (1146, 8))

    with nose.tools.assert_raises(ValueError):
        pybea.get_data(DataSetName='InvalidDataSetName')
