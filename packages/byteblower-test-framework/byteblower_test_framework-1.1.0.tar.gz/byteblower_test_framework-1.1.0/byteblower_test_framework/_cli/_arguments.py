"""Module for generic argument parsing."""
from argparse import ArgumentParser
from os import getcwd
from os.path import exists, join
from typing import Optional, Tuple  # for type hinting

from byteblower_test_framework.exceptions import InvalidInput

from ._definitions import DEFAULT_REPORT_PATH, DEFAULT_REPORT_PREFIX

__all__ = ('parse_arguments', )

# Use the package name as the default config file name (without extension):
_FILE_BASE_NAME = __package__.rsplit('.', maxsplit=2)[-2]
DEFAULT_CONFIG_FILE = _FILE_BASE_NAME + '.json'
DEFAULT_CONFIG_PATH = '.'


def parse_arguments() -> Tuple[str, Optional[str], str]:
    """Parse the command line arguments of a script.

    Parses the generic command-line arguments of a use case script
    for traffic generation.

    :raises InvalidInput: When the config file does not exist
    :raises InvalidInput: When the given report path does not exist
    :return:
       Tuple of:

       1. Config file name. Default: :const:`DEFAULT_CONFIG_FILE`
          (<script_name> + '.json')
       2. (*optional*) report path. Default: None
       3. Prefix for the report file name(s).
          Default: :const:`DEFAULT_REPORT_PREFIX`

    :rtype: Tuple[str, Optional[str], str]
    """
    parser = ArgumentParser(description='ByteBlower tests for UDP/TCP traffic')
    parser.add_argument(
        '--config_file',
        help='Test configuration file to load. If an absolute path is given'
        ', the `<config_path>` won\'t be used.'
        f' Default: {DEFAULT_CONFIG_FILE!r}',
        default=DEFAULT_CONFIG_FILE,
        metavar='<config_file>'
    )
    parser.add_argument(
        '--config_path',
        help='Location of the configuration file(s).'
        f' Default: {DEFAULT_CONFIG_PATH!r} (current directory)',
        default=DEFAULT_CONFIG_PATH,
        metavar='<config_path>'
    )
    parser.add_argument(
        '--report_path',
        help='Output location for the report file(s).'
        f' Default: {DEFAULT_REPORT_PATH!r} (current directory)',
        default=DEFAULT_REPORT_PATH,
        metavar='<report_path>'
    )
    parser.add_argument(
        '--report_prefix',
        help='Prefix for the report file(s).'
        f' Default: {DEFAULT_REPORT_PREFIX!r}',
        default=DEFAULT_REPORT_PREFIX,
        metavar='<report_prefix>'
    )
    args = parser.parse_args()

    # NOTE: No need to check ``isabs(args.config_file)`` ourselves.
    # From ``join`` documentation:
    #     If any component is an absolute path, all
    #     previous path components will be discarded.
    config_file_name = join(args.config_path, args.config_file)

    report_path = args.report_path
    if report_path is not None:
        # NOTE: No need to check ``isabs(args.output_dir)`` ourselves.
        # From ``join`` documentation:
        #     If any component is an absolute path, all
        #     previous path components will be discarded.
        report_path = join(getcwd(), report_path)
    report_prefix = args.report_prefix

    # Sanity checks
    if not exists(config_file_name):
        raise InvalidInput(
            'Test configuration file does not exist.'
            f' Tried {config_file_name!r}'
        )
    if report_path is not None and not exists(report_path):
        raise InvalidInput(
            f'Test report path {report_path!r} does not exist.'
            ' Please create the report output location and try again.'
        )

    return config_file_name, report_path, report_prefix
