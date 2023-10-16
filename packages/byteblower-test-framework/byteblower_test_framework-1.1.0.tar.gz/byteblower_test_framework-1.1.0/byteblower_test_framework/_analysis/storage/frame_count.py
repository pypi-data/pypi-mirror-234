"""Data stores for input from ByteBlower Triggers (frame blasting use case)."""
from typing import Optional  # for type hinting

from pandas import Timestamp  # for type hinting
from pandas import DataFrame

from .data_store import DataStore


class FrameCountData(DataStore):
    """Storage for total and over time counts of transferred frames."""

    __slots__ = (
        '_over_time',
        '_total_bytes',
        '_total_vlan_bytes',
        '_total_packets',
        '_timestamp_first',
        '_timestamp_last',
    )

    def __init__(self) -> None:
        self._over_time = DataFrame(
            columns=[
                "Duration total",
                "Packets total",
                "Bytes total",
                "Duration interval",
                "Packets interval",
                "Bytes interval",
            ]
        )
        self._total_bytes: Optional[int] = None
        self._total_vlan_bytes: Optional[int] = None
        self._total_packets: Optional[int] = None
        self._timestamp_first: Optional[Timestamp] = None
        self._timestamp_last: Optional[Timestamp] = None

    @property
    def over_time(self) -> DataFrame:
        """
        Return ``DataFrame`` with transferred data over time results.

        Includes:

        * Total duration since first packet transferred
        * Cumulative number of packets transferred
        * Cumulative number of bytes transferred
        * Duration per interval
        * Number of packets transferred per interval
        * Number of bytes transferred per interval
        """
        return self._over_time

    @property
    def total_bytes(self) -> int:
        """Return total number of transferred bytes."""
        return self._total_bytes

    @property
    def total_vlan_bytes(self) -> int:
        """Return total number of bytes transferred in Layer2.5 VLAN header."""
        return self._total_vlan_bytes

    @property
    def total_packets(self) -> int:
        """Return total transferred number of packets."""
        return self._total_packets

    @property
    def timestamp_first(self) -> Optional[Timestamp]:
        """Return the timestamp of the first transferred packet."""
        return self._timestamp_first

    @property
    def timestamp_last(self) -> Optional[Timestamp]:
        """Return the timestamp of the last transferred packet."""
        return self._timestamp_last
