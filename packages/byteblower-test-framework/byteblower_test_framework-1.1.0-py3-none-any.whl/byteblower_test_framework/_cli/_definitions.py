"""Shared type definitions and constants."""
from typing import Any, Dict  # for type hinting

# Type aliases
TestConfig = Dict[str, Any]

#: Default path to store the reports to:
#: ``None`` (== current directory)
DEFAULT_REPORT_PATH = None
#: Default prefix for the ByteBlower report file names.
DEFAULT_REPORT_PREFIX = 'byteblower'

DEFAULT_ENABLE_HTML = True
DEFAULT_ENABLE_JSON = True
DEFAULT_ENABLE_JUNIT_XML = True

LOGGING_PREFIX = 'Test Case: '
