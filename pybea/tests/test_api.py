"""
Tests for api.py module.

@author : David R. Pugh
@date : 2014-09-22

"""
import nose
import unittest

from .. import api


USER_ID = '98A0A0A7-21DF-4B75-96DE-1410D47AB280'


class TestRequest(unittest.TestCase):
    """Testing suite for the base Request class."""

    user_id = '98A0A0A7-21DF-4B75-96DE-1410D47AB280'

    def test__delitem__(self):
        """Testing override of __delitem__."""
        valid_request = api.RegionalDataRequest(UserID=USER_ID,
                                                KeyCode='POP_CI',
                                                Year=['1995'],
                                                GeoFips='MSA',
                                                ResultFormat='JSON')
        nose.tools.assert_true(valid_request.response.ok)

        # confirm that dictionary has been updated
        del valid_request['GeoFips']
        nose.tools.assert_false('GeoFips' in valid_request)

        # confirm that cache has been cleared
        nose.tools.assert_equals(valid_request._response, None)

    def test__init__(self):
        """Testing initiation of a Request."""
        valid_request = api.Request(UserID=USER_ID,
                                    Method='GetDataSetList',
                                    ResultFormat='JSON')
        nose.tools.assert_true(valid_request.response.ok)

    def test__setitem__(self):
        """Testing override of __setitem__."""
        valid_request = api.RegionalDataRequest(UserID=USER_ID,
                                                KeyCode='POP_CI',
                                                Year=['2009'],
                                                GeoFips='STATE',
                                                ResultFormat='JSON')
        nose.tools.assert_true(valid_request.response.ok)

        # confirm that dictionary has been updated
        valid_request['GeoFips'] = 'MSA'
        nose.tools.assert_true('GeoFips' in valid_request)

        # confirm that cache has been cleared
        nose.tools.assert_equals(valid_request._response, None)

    def test_request_attribute(self):
        """Testing the return type of the request attribute."""
        valid_request = api.RegionalDataRequest(UserID=USER_ID,
                                                KeyCode='GDP_MP',
                                                Year=['1990'],
                                                GeoFips='MSA',
                                                ResultFormat='JSON')
        nose.tools.assert_true(valid_request.response.ok)

        # check return type
        nose.tools.assert_is_instance(valid_request.request, dict)

        # XML not yet implemented
        with nose.tools.assert_raises(NotImplementedError):
            valid_request['ResultFormat'] = 'XML'
            valid_request.request

    def test_results_attribute(self):
        """Testing the return type of the results attribute."""
        valid_request = api.RegionalDataRequest(UserID=USER_ID,
                                                KeyCode='GDP_MP',
                                                Year=['1990'],
                                                GeoFips='MSA',
                                                ResultFormat='JSON')
        nose.tools.assert_true(valid_request.response.ok)

        # check return type
        nose.tools.assert_is_instance(valid_request.results, dict)

        # XML not yet implemented
        with nose.tools.assert_raises(NotImplementedError):
            valid_request['ResultFormat'] = 'XML'
            valid_request.results

    def test_validate_result_format(self):
        """Testing validation of ResultFormat keyword arg."""
        # ResultFormat must be a string
        with nose.tools.assert_raises(AttributeError):
            api.Request(UserID=USER_ID, Method='GetDataSetList', ResultFormat=3)

        # Result format must be valid
        with nose.tools.assert_raises(AttributeError):
            api.Request(UserID=USER_ID, Method='GetData', ResultFormat='InvalidFormat')

    def test_validate_method(self):
        """Testing validation of Method keyword arg."""
        # ResultFormat must be a string
        with nose.tools.assert_raises(AttributeError):
            api.Request(UserID=USER_ID, Method=0, ResultFormat='JSON')

        # Method must be valid
        with nose.tools.assert_raises(AttributeError):
            api.Request(UserID=USER_ID, Method='GetParameters', ResultFormat='InvalidFormat')


class DataSetListRequest(unittest.TestCase):
    """Testing suite for the DataTestListRequest."""

    def test_initiate_data_set_list_request(self):
        """Testing initiation of a DataSetListRequest."""
        valid_request = api.DataSetListRequest(UserID=USER_ID, ResultFormat='JSON')
        nose.tools.assert_true(valid_request.response.ok)

    def test_data_set_attribute(self):
        """Testing the return type of the data_set attribute."""
        valid_request = api.DataSetListRequest(UserID=USER_ID, ResultFormat='JSON')
        nose.tools.assert_true(valid_request.response.ok)

        # check return type
        nose.tools.assert_is_instance(valid_request.data_set, list)

        # XML not yet implemented
        with nose.tools.assert_raises(NotImplementedError):
            valid_request['ResultFormat'] = 'XML'
            valid_request.data_set


class ParameterListRequest(unittest.TestCase):
    """Testing suite for the ParameterListRequest."""

    def test_initiate_parameter_list_request(self):
        """Testing initiation of a ParameterListRequest."""
        valid_request = api.ParameterListRequest(UserID=USER_ID,
                                                 DataSetName='NIPA',
                                                 ResultFormat='JSON')
        nose.tools.assert_true(valid_request.response.ok)

    def test_parameter_list_attribute(self):
        """Testing the return type of the parameter list attribute."""
        valid_request = api.ParameterListRequest(UserID=USER_ID,
                                                 DataSetName='NIPA',
                                                 ResultFormat='JSON')
        nose.tools.assert_true(valid_request.response.ok)

        # check return type
        nose.tools.assert_is_instance(valid_request.parameter_list, list)

        # XML not yet implemented
        with nose.tools.assert_raises(NotImplementedError):
            valid_request['ResultFormat'] = 'XML'
            valid_request.parameter_list


class ParameterValuesRequest(unittest.TestCase):
    """Testing suite for the ParameterValuesRequest."""

    def test_initiate_parameter_list_request(self):
        """Testing initiation of a ParameterValuesRequest."""
        valid_request = api.ParameterValuesRequest(UserID=USER_ID,
                                                   DataSetName='NIPA',
                                                   ParameterName='TableID',
                                                   ResultFormat='JSON')
        nose.tools.assert_true(valid_request.response.ok)

    def test_parameter_list_attribute(self):
        """Testing the return type of the parameter list attribute."""
        valid_request = api.ParameterValuesRequest(UserID=USER_ID,
                                                   DataSetName='NIPA',
                                                   ParameterName='TableID',
                                                   ResultFormat='JSON')
        nose.tools.assert_true(valid_request.response.ok)

        # check return type
        nose.tools.assert_is_instance(valid_request.parameter_values, list)

        # XML not yet implemented
        with nose.tools.assert_raises(NotImplementedError):
            valid_request['ResultFormat'] = 'XML'
            valid_request.parameter_values


class DataRequest(unittest.TestCase):
    """Testing suite for the DataRequest."""

    def test_data_attribute(self):
        """Testing the return type of the data attribute."""
        valid_request = api.DataRequest(UserID=USER_ID,
                                        DataSetName='RegionalData',
                                        KeyCode='POP_MI',
                                        Year=['1990'],
                                        GeoFips='MSA',
                                        ResultFormat='JSON')
        nose.tools.assert_true(valid_request.response.ok)

        # check return type
        nose.tools.assert_is_instance(valid_request.data, list)

        # XML not yet implemented
        with nose.tools.assert_raises(NotImplementedError):
            valid_request['ResultFormat'] = 'XML'
            valid_request.data

    def test_dimensions_attribute(self):
        """Testing the return type of the dimensions attribute."""
        valid_request = api.DataRequest(UserID=USER_ID,
                                        DataSetName='RegionalData',
                                        KeyCode='POP_MI',
                                        Year=['1990'],
                                        GeoFips='MSA',
                                        ResultFormat='JSON')
        nose.tools.assert_true(valid_request.response.ok)

        # check return type
        nose.tools.assert_is_instance(valid_request.dimensions, list)

        # XML not yet implemented
        with nose.tools.assert_raises(NotImplementedError):
            valid_request['ResultFormat'] = 'XML'
            valid_request.dimensions

    def test_notes_attribute(self):
        """Testing the return type of the dimensions attribute."""
        valid_request = api.DataRequest(UserID=USER_ID,
                                        DataSetName='RegionalData',
                                        KeyCode='DIR_SI',
                                        Year=['1985'],
                                        GeoFips='STATE',
                                        ResultFormat='JSON')
        nose.tools.assert_true(valid_request.response.ok)

        # check return type
        nose.tools.assert_is_instance(valid_request.notes, list)

        # XML not yet implemented
        with nose.tools.assert_raises(NotImplementedError):
            valid_request['ResultFormat'] = 'XML'
            valid_request.notes


class NIPARequest(unittest.TestCase):
    """Testing suite for the NIPARequest class."""

    def test_initiate_nipa_request(self):
        """Testing initiation of a NIPARequest."""
        valid_request = api.NIPARequest(UserID=USER_ID,
                                        TableID='25',
                                        Frequency='Q',
                                        Year=['2000', '2005'],
                                        ResultFormat='JSON')
        nose.tools.assert_true(valid_request.response.ok)


class NIUnderlyingDetailRequest(unittest.TestCase):
    """Testing suite for the NIUnderlyingDetailRequest class."""

    def test_initiate_ni_underlying_detail_request(self):
        """Testing initiation of a NIUnderlyingDetailRequest."""
        valid_request = api.NIUnderlyingDetailRequest(UserID=USER_ID,
                                                      TableID='25',
                                                      Frequency='Q',
                                                      Year=['2000', '2005'],
                                                      ResultFormat='JSON')
        nose.tools.assert_true(valid_request.response.ok)


class FixedAssetsRequest(unittest.TestCase):
    """Testing suite for the FixedAssetsRequest class."""

    def test_initiate_fixed_assets_request(self):
        """Testing initiation of a FixedAssetsRequest."""
        valid_request = api.FixedAssetsRequest(UserID=USER_ID,
                                               TableID='23',
                                               Year=['2000', '2010'],
                                               ResultFormat='JSON')
        nose.tools.assert_true(valid_request.response.ok)
