"""Data storage for Stream status information."""
from typing import TYPE_CHECKING  # for type hinting
from typing import Optional  # for type hinting

from ..._traffic.stream import (  # for type hinting
    StreamErrorSource,
    StreamErrorStatus,
)
from .data_store import DataStore

if TYPE_CHECKING:
    # NOTE: Used in documentation only
    from byteblowerll.byteblower import Stream

__all__ = ('StreamStatusData', )


class StreamStatusData(DataStore):
    """Status data from a :class:`Stream`."""

    __slots__ = (
        '_error_status',
        '_error_source',
    )

    def __init__(self) -> None:
        """Create stream status data container."""
        super().__init__()
        self._error_status: Optional[StreamErrorStatus] = None
        self._error_source: Optional[StreamErrorSource] = None

    @property
    def error_status(self) -> Optional[StreamErrorStatus]:
        """Return the transmit error status of a stream.

        :return: Transmit error status of the stream.
        :rtype: Optional[StreamErrorStatus]
        """
        return self._error_status

    @property
    def error_source(self) -> Optional[StreamErrorSource]:
        """Return the source of transmit errors on a stream.

        :return: Transmit error source.
        :rtype: Optional[StreamErrorSource]
        """
        return self._error_source
