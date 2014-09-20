"""
Tests for apy.py module.

@author : David R. Pugh
@date : 2014-09-19

"""
import nose

from .. import api

valid_formats = ['JSON', 'XML']
valid_methods = ['GetDataSetList', 'GetParameterList', 'GetParameterValues',
                 'GetData']


# testing functions
def test_validate_result_format():
    """Testing validation of ResultFormat keyword arg."""
    # ResultFormat must be a string
    with nose.tools.assert_raises(AttributeError):
        api.Request(Method=valid_methods[0], ResultFormat=3)

    # Result format must be valid
    with nose.tools.assert_raises(AttributeError):
        api.Request(Method=valid_methods[-1], ResultFormat='InvalidFormat')


def test_validate_method():
    """Testing validation of Method keyword arg."""
    # ResultFormat must be a string
    with nose.tools.assert_raises(AttributeError):
        api.Request(Method=0, ResultFormat=valid_formats[0])

    # Method must be valid
    with nose.tools.assert_raises(AttributeError):
        api.Request(Method='GetParameters', ResultFormat=valid_formats[1])
