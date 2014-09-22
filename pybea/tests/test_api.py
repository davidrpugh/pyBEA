"""
Tests for apy.py module.

@author : David R. Pugh
@date : 2014-09-19

"""
import nose
import unittest

from .. import api

valid_formats = ['JSON', 'XML']
valid_methods = ['GetDataSetList', 'GetParameterList', 'GetParameterValues',
                 'GetData']


class TestRequest(unittest.TestCase):
    """Testing suite for the base Request class."""

    def test__detitem__(self):
        """Testing override of __delitem__."""
        valid_request = api.RegionalDataRequest(KeyCode='POP_CI',
                                                Year=['1995'],
                                                GeoFips='MSA',
                                                ResultFormat=valid_formats[0])
        nose.tools.assert_true(valid_request.response.ok)

        # confirm that dictionary has been updated
        del valid_request['GeoFips']
        nose.tools.assert_false('GeoFips' in valid_request)

        # confirm that cache has been cleared
        nose.tools.assert_equals(valid_request._response, None)

    def test__init__(self):
        """Testing initiation of a Request."""
        valid_request = api.Request(Method=valid_methods[0],
                                    ResultFormat=valid_formats[0])
        nose.tools.assert_true(valid_request.response.ok)

    def test__setitem__(self):
        """Testing override of __setitem__."""
        valid_request = api.RegionalDataRequest(KeyCode='POP_CI',
                                                Year=['2009'],
                                                GeoFips='STATE',
                                                ResultFormat=valid_formats[0])
        nose.tools.assert_true(valid_request.response.ok)

        # confirm that dictionary has been updated
        valid_request['GeoFips'] = 'MSA'
        nose.tools.assert_true('GeoFips' in valid_request)

        # confirm that cache has been cleared
        nose.tools.assert_equals(valid_request._response, None)

    def test_request_attribute(self):
        """Testing the return type of the request attribute."""
        valid_request = api.RegionalDataRequest(KeyCode='GDP_MP',
                                                Year=['1990'],
                                                GeoFips='MSA',
                                                ResultFormat=valid_formats[0])
        nose.tools.assert_true(valid_request.response.ok)

        # check return type
        nose.tools.assert_is_instance(valid_request.request, dict)

        # XML not yet implemented
        with nose.tools.assert_raises(NotImplementedError):
            valid_request['ResultFormat'] = 'XML'
            valid_request.request

    def test_results_attribute(self):
        """Testing the return type of the results attribute."""
        valid_request = api.RegionalDataRequest(KeyCode='GDP_MP',
                                                Year=['1990'],
                                                GeoFips='MSA',
                                                ResultFormat=valid_formats[0])
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
            api.Request(Method=valid_methods[0], ResultFormat=3)

        # Result format must be valid
        with nose.tools.assert_raises(AttributeError):
            api.Request(Method=valid_methods[-1], ResultFormat='InvalidFormat')

    def test_validate_method(self):
        """Testing validation of Method keyword arg."""
        # ResultFormat must be a string
        with nose.tools.assert_raises(AttributeError):
            api.Request(Method=0, ResultFormat=valid_formats[0])

        # Method must be valid
        with nose.tools.assert_raises(AttributeError):
            api.Request(Method='GetParameters', ResultFormat=valid_formats[1])


class DataSetListRequest(unittest.TestCase):
    """Testing suite for the DataTestListRequest."""

    def test_initiate_data_set_list_request(self):
        """Testing initiation of a DataSetListRequest."""
        valid_request = api.DataSetListRequest(ResultFormat=valid_formats[0])
        nose.tools.assert_true(valid_request.response.ok)
