import pytest
UserID = 'AEC7FDB2-4F22-4296-982D-7CA35C0341BA'


def test_bea_link():
    import sys
    import os

    pybea_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pybea'))
    sys.path.append(pybea_path)

    import pybea

    df = pybea.get_data_set_list(UserID=UserID)

    assert 'DatasetName' in df


def test_get_data_set_list():
    import sys
    import os
    pybea_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pybea'))
    sys.path.append(pybea_path)
    import pybea
    df = pybea.get_data_set_list(UserID)

    assert 'DatasetDescription' in df


def test_get_parameter_list():
    import sys
    import os
    pybea_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pybea'))
    sys.path.append(pybea_path)
    import pybea
    df = pybea.get_parameter_list(UserID, 'FixedAssets')

    assert 'ParameterName' in df

def test_get_data():
    import sys
    import os
    pybea_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pybea'))
    sys.path.append(pybea_path)
    import pybea
    df = pybea.get_data(UserID, DataSetName='FixedAssets', TableName='FAAt101', Year='ALL')

    assert 'TableName' in df


def test_get_parameter_values():
    import sys
    import os
    pybea_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pybea'))
    sys.path.append(pybea_path)
    import pybea
    df = pybea.get_parameter_values(UserID, 'ITA', 'Indicator')

    assert 'Key' in df


