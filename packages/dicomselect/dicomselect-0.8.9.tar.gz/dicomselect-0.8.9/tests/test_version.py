from dicomselect import version as module_version
from setup import version as setup_version


def test_version():
    assert setup_version == module_version
    