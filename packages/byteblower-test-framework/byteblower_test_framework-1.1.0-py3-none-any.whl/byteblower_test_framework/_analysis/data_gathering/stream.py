"""Data gathering for a ByteBlower Stream."""
import logging
from typing import TYPE_CHECKING  # for type hinting

from byteblowerll.byteblower import (  # for type hinting
    StreamResultData,
    StreamResultHistory,
    StreamRuntimeStatus,
    TransmitErrorSource,
    TransmitErrorStatus,
)
from pandas import Timestamp  # for type hinting
from pandas import to_datetime

from ..._traffic.frame import VLAN_HEADER_LENGTH
from ..._traffic.stream import StreamErrorSource, StreamErrorStatus
from ..storage.frame_count import FrameCountData
from ..storage.stream import StreamStatusData
from .data_gatherer import DataGatherer

if TYPE_CHECKING:
    # NOTE: Import does not work at runtime: cyclic import dependencies
    # See also: https://mypy.readthedocs.io/en/stable/runtime_troubles.html#import-cycles, pylint: disable=line-too-long
    from ..._traffic.frameblastingflow import \
        FrameBlastingFlow  # for type hinting


class StreamDataGatherer(DataGatherer):
    """Base class for Stream Data gatherer."""


class StreamFrameCountDataGatherer(StreamDataGatherer):
    """Data gatherer for ByteBlower Stream."""

    __slots__ = (
        '_stream_status_data',
        '_frame_count_data',
        '_flow',
        '_tx_vlan_header_size',
        '_tx_result',
    )

    def __init__(
        self, stream_status_data: StreamStatusData,
        frame_count_data: FrameCountData, flow: 'FrameBlastingFlow'
    ) -> None:
        super().__init__()
        self._stream_status_data = stream_status_data
        self._frame_count_data = frame_count_data
        self._flow = flow
        self._tx_vlan_header_size: int = 0
        self._tx_result: StreamResultHistory = \
            self._flow._stream.ResultHistoryGet()

    def prepare(self) -> None:
        self._flow._stream.ResultClear()
        # NOTE: We calculate the VLAN header sizes at start of the Flow,
        #       since this is the point where the filter was created.
        # TODO: For TX, it should actually be done when creating the Frame
        #       * objects (setting frame content) at ByteBlower API/Server.
        source_vlan_config = list(self._flow.source.vlan_config)
        self._tx_vlan_header_size = len(
            source_vlan_config
        ) * VLAN_HEADER_LENGTH

    def updatestats(self) -> None:
        # Refresh the history
        self._tx_result.Refresh()

        # Add all the history snapshots
        self._persist_history_snapshots()

        # Clear the history
        self._tx_result.Clear()

    def summarize(self) -> None:
        # Refresh the history
        self._tx_result.Refresh()

        # Add remaining history snapshots
        self._persist_history_snapshots()

        cumulative_snapshot: StreamResultData = (
            self._tx_result.CumulativeLatestGet()
        )
        total_tx_packets = cumulative_snapshot.PacketCountGet()
        if total_tx_packets:
            ts_tx_first_ns = cumulative_snapshot.TimestampFirstGet()
            ts_tx_last_ns = cumulative_snapshot.TimestampLastGet()
        else:
            ts_tx_first_ns = None
            ts_tx_last_ns = None
        self._frame_count_data._total_bytes = (
            cumulative_snapshot.ByteCountGet()
        )
        self._frame_count_data._total_vlan_bytes = (
            total_tx_packets * self._tx_vlan_header_size
        )
        self._frame_count_data._total_packets = total_tx_packets
        self._frame_count_data._timestamp_first = to_datetime(
            ts_tx_first_ns, unit='ns', utc=True
        )
        self._frame_count_data._timestamp_last = to_datetime(
            ts_tx_last_ns, unit='ns', utc=True
        )

        timestamp_ns: int = cumulative_snapshot.TimestampGet()
        interval_snapshot: StreamResultData = (
            self._tx_result.IntervalGetByTime(timestamp_ns)
        )
        timestamp = to_datetime(timestamp_ns, unit='ns', utc=True)
        self._process_snapshot(
            timestamp,
            cumulative_snapshot,
            interval_snapshot,
        )

        # Store the final stream status
        tx_status: StreamRuntimeStatus = self._flow._stream.StatusGet()
        tx_error_status: TransmitErrorStatus = tx_status.ErrorStatusGet()
        self._stream_status_data._error_status = StreamErrorStatus(
            tx_error_status
        )
        tx_error_source: TransmitErrorSource = tx_status.ErrorSourceGet()
        self._stream_status_data._error_source = StreamErrorSource(
            tx_error_source
        )

    def release(self) -> None:
        super().release()
        # NOTE: `_tx_result` will be released with the release of the Stream.
        del self._tx_result

    def _persist_history_snapshots(self) -> None:
        """Add all the history interval results."""
        cumulative_snapshot: StreamResultData = None  # for type hinting
        for cumulative_snapshot in self._tx_result.CumulativeGet()[:-1]:
            try:
                ts_ns: int = cumulative_snapshot.TimestampGet()
                interval_snapshot: StreamResultData = (
                    self._tx_result.IntervalGetByTime(ts_ns)
                )
                timestamp = to_datetime(ts_ns, unit='ns', utc=True)
                self._frame_count_data.over_time.loc[timestamp] = [
                    cumulative_snapshot.IntervalDurationGet(),
                    cumulative_snapshot.PacketCountGet(),
                    cumulative_snapshot.ByteCountGet(),
                    interval_snapshot.IntervalDurationGet(),
                    interval_snapshot.PacketCountGet(),
                    interval_snapshot.ByteCountGet(),
                ]
                self._process_snapshot(
                    timestamp,
                    cumulative_snapshot,
                    interval_snapshot,
                )
            except Exception:
                logging.warning(
                    "Something went wrong during processing of TX stats.",
                    exc_info=True
                )

    def _process_snapshot(
        self, timestamp: Timestamp, cumulative_snapshot: StreamResultData,
        interval_snapshot: StreamResultData
    ) -> None:
        """Perform additional processing of the history snapshots.

        Hook function which can be overridden by child classes.
        Called when updating stats for the given timestamp.

        :param timestamp: Timestamp of the snapshot
        :type timestamp: Timestamp
        :param cumulative_snapshot: Snapshot of the cumulative results
        :type cumulative_snapshot: StreamResultData
        :param interval_snapshot: Snapshot of the interval results
        :type interval_snapshot: StreamResultData
        """
