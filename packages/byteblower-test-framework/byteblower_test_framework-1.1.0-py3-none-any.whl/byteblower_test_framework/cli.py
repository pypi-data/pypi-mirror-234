"""Command-line interface.

.. versionadded:: 1.1.0
"""
import logging

from byteblower_test_framework.logging import configure_logging

from ._cli._arguments import parse_arguments
from ._cli._config_file import load_config_file
from ._cli._definitions import LOGGING_PREFIX
from ._cli._with_json_configfile import run

# Export user interfaces of this traffic test module
# * to run it as main application
# * to run it integrated in the user's script
__all__ = (
    'main',
    'cli',
    run.__name__,
)


def cli() -> None:
    """Run the main application.

    Parses command-line arguments, loads the configuration file
    and runs the actual use case.

    .. versionadded:: 1.1.0
    """
    logging.info("Initializing ByteBlower traffic Test")

    # Load test configuration
    config_file_name, report_path, report_prefix = parse_arguments()
    logging.info(
        '%sLoading configuration file %s', LOGGING_PREFIX, config_file_name
    )
    test_config = load_config_file(config_file_name)
    run(test_config, report_path=report_path, report_prefix=report_prefix)


def main() -> None:
    """Configure logging and start the main application.

    .. versionadded:: 1.1.0
    """
    # 1. Configure logging
    main_log_level = logging.INFO
    logging.basicConfig(level=main_log_level)

    logging.info("Initializing logging for ByteBlower Test Framework")

    framework_level = logging.INFO
    for framework_module in ('byteblower_test_framework', ):
        framework_logger = logging.getLogger(framework_module)
        framework_logger.setLevel(framework_level)

    # Everything under ._cli module is our "main application",
    # so use the main application log level here
    for main_module in ('byteblower_test_framework._cli',
                        'byteblower_test_framework.cli'):
        framework_logger = logging.getLogger(main_module)
        framework_logger.setLevel(main_log_level)

    configure_logging()

    # 2. Run the use case
    cli()


if __name__ == '__main__':
    main()
