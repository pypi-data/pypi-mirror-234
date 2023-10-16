"""Definitions related to stream status information."""
from enum import Enum
from typing import TYPE_CHECKING  # for type hinting

from byteblowerll.byteblower import TransmitErrorSource, TransmitErrorStatus

if TYPE_CHECKING:
    # NOTE: Used in documentation only
    from byteblowerll.byteblower import Stream

__all__ = (
    'StreamErrorStatus',
    'StreamErrorSource',
)


class StreamErrorStatus(Enum):
    """The error status of a :class:`Stream`."""

    UNKNOWN = TransmitErrorStatus.UNKNOWN

    NONE = TransmitErrorStatus.NONE
    OUT_OF_RESOURCES = TransmitErrorStatus.OUT_OF_RESOURCES

    def to_json(self) -> str:
        """Return the name of the stream error status."""
        return self.name


class StreamErrorSource(Enum):
    """The source of an error of a :class:`Stream`."""

    UNKNOWN = TransmitErrorSource.UNKNOWN

    NONE = TransmitErrorSource.NONE
    INTERFACE_HARDWARE = TransmitErrorSource.INTERFACE_HARDWARE
    SCHEDULING_CONFLICT = TransmitErrorSource.SCHEDULING_CONFLICT
    TXUSER = TransmitErrorSource.TXUSER

    def to_json(self) -> str:
        """Return the name of the stream error source."""
        return self.name
