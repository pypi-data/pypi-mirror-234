"""Config file handling."""
from ._definitions import TestConfig  # for type hinting

# Support both simplejson as builtin json module
try:
    import simplejson as json
except ImportError:
    import json

__all__ = ('load_config_file', )


def load_config_file(config_file_name: str) -> TestConfig:
    """Load and parse the test configuration file.

    We currently only support JSON format.

    :param config_file_name: Configuration file name
    :type config_file_name: str
    :return: Dict of configuration items.
    :rtype: TestConfig
    """
    with open(config_file_name, 'r', encoding='utf-8') as config_file:
        test_config = json.load(config_file)
    return test_config
