"""Host interfaces which serve ByteBlower traffic endpoints."""
from ._host.server import Server

# Export the user interfaces.
#
# Outcomes:
# * Limits import on `from byteblower_test_framework.host import *`
# * Exposes the interfaces in the (Sphinx) documentation
#
__all__ = (
    Server.__name__,  # ByteBlowerServer interface
)
