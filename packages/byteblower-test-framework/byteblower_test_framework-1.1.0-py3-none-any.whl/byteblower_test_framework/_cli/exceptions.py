"""Command-line interface specific exceptions."""
from ..exceptions import ByteBlowerTestFrameworkException


class UDPMaxExceeded(ByteBlowerTestFrameworkException):
    """Exceeded maximum allowed UDP port number (65535)."""
