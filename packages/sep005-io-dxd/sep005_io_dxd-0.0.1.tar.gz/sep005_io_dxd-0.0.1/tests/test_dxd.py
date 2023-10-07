import os

import pytest
from sdypy_sep005.sep005 import assert_sep005

from sep005_io_dxd import read_dxd

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, 'static')
GOOD_FILES = os.listdir(os.path.join(static_dir, 'good'))


@pytest.mark.parametrize("filename", GOOD_FILES)
def test_compliance_sep005(filename):
    """
    Test the compliance with the SEP005 guidelines
    """
    file_path = os.path.join(static_dir, 'good', filename)
    signals = read_dxd(file_path)  # should already not crash here

    assert len(signals) != 0  # Not an empty response
    assert_sep005(signals)


def test_acc_001():
    """
    Test the correct import of a single file with acceleration data


    :return:
    """
    test_file_name = r"test_acc_001.dxd"
    file_path = os.path.join(static_dir, 'good', test_file_name)

    signals = read_dxd(file_path)

    assert len(signals) == 3
    assert all(['ACC' in s['name'] for s in signals])
    assert all([s['unit_str'] == 'g' for s in signals])
    assert all([len(s['data']) == 600*100 for s in signals])
