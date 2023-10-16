import logging
from typing import Optional  # for type hinting

from pandas import DataFrame, Timestamp, concat  # for type hinting

from ..._report.options import Layer2Speed, layer2_speed_info
from ..helpers import include_ethernet_overhead
from ..storage.frame_count import FrameCountData
from ..storage.trigger import LatencyData, LatencyDistributionData
from .data_analyser import DataAnalyser

__all__ = (
    'FrameCountAnalyser',
    'LatencyAnalyser',
    'LatencyCDFAnalyser',
    'MosAnalyser',
)


class FrameCountAnalyser(DataAnalyser):

    __slots__ = (
        '_tx_data',
        '_rx_data',
        '_df_tx_bytes',
        '_df_rx_bytes',
        '_layer2_speed',
        '_max_loss_percentage',
    )

    def __init__(
        self, tx_data: FrameCountData, rx_data: FrameCountData,
        layer2_speed: Layer2Speed, max_loss_percentage: float
    ) -> None:
        super().__init__()
        self._tx_data = tx_data
        self._rx_data = rx_data
        self._df_tx_bytes: DataFrame = None
        self._df_rx_bytes: DataFrame = None
        self._layer2_speed = layer2_speed
        self._max_loss_percentage = max_loss_percentage

    def analyse(self) -> None:
        """Fail the test if the packet loss > ``max_loss_percentage``."""
        df_tx = self._tx_data.over_time
        df_rx = self._rx_data.over_time

        total_tx_packets = self._tx_data.total_packets
        total_rx_packets = self._rx_data.total_packets
        total_tx_bytes = self._tx_data.total_bytes
        total_rx_bytes = self._rx_data.total_bytes
        total_tx_vlan_bytes = self._tx_data.total_vlan_bytes
        total_rx_vlan_bytes = self._rx_data.total_vlan_bytes

        summary_log = []

        # Layer 2 speed calculation info
        summary_log.append(f"{layer2_speed_info(self._layer2_speed)}")

        self._df_tx_bytes = include_ethernet_overhead(
            self._layer2_speed, (df_tx, 'Bytes interval'),
            (df_tx, 'Packets interval')
        )
        self._df_rx_bytes = include_ethernet_overhead(
            self._layer2_speed, (df_rx, 'Bytes interval'),
            (df_rx, 'Packets interval')
        )
        total_tx_bytes = include_ethernet_overhead(
            self._layer2_speed, total_tx_bytes, total_tx_packets
        )
        total_rx_bytes = include_ethernet_overhead(
            self._layer2_speed, total_rx_bytes, total_rx_packets
        )

        self._set_result(True)

        total_tx_bytes_without_vlan = total_tx_bytes - total_tx_vlan_bytes
        total_rx_bytes_without_vlan = total_rx_bytes - total_rx_vlan_bytes
        byteloss = total_tx_bytes_without_vlan - total_rx_bytes_without_vlan
        relativebyteloss = 100.0
        if total_tx_bytes != 0:
            relativebyteloss *= byteloss / total_tx_bytes_without_vlan

        packetloss = total_tx_packets - total_rx_packets
        relativepacketloss = 100.0
        if total_tx_packets != 0:
            relativepacketloss *= packetloss / total_tx_packets

        # Append count summary info
        summary_log.append("Transmitted:")
        summary_log.append(f"    {total_tx_packets} packets")
        if total_tx_vlan_bytes:
            summary_log.append(
                f"    {total_tx_bytes_without_vlan} bytes"
                f" (+{total_tx_vlan_bytes} VLAN)"
            )
        else:
            summary_log.append(f"    {total_tx_bytes} bytes")
        summary_log.append("Received:")
        summary_log.append(f"    {total_rx_packets} packets")
        if total_rx_vlan_bytes:
            summary_log.append(
                f"    {total_rx_bytes_without_vlan} bytes"
                f" (+{total_rx_vlan_bytes} VLAN)"
            )
        else:
            summary_log.append(f"    {total_rx_bytes} bytes")
        summary_log.append("Loss:")
        summary_log.append(f"    {byteloss} bytes ({relativebyteloss:0.2f}%)")
        summary_log.append(
            f"    {packetloss} packets ({relativepacketloss:0.2f}%)"
        )

        self._set_log('\n'.join(summary_log))
        if relativepacketloss > self._max_loss_percentage:
            self._set_result(False)
            self._add_failure_cause(
                "Packet loss has exceeded the maximum allowed"
                f" loss of {self._max_loss_percentage:0.2f} %"
            )
        elif relativebyteloss > self._max_loss_percentage:
            self._set_result(False)
            self._add_failure_cause(
                "Byte loss has exceeded the maximum allowed loss"
                f" of {self._max_loss_percentage:0.2f} %"
            )

    @property
    def df_tx(self) -> DataFrame:
        """
        Return ``DataFrame`` of transmitter over time results.

        Includes:

        * Total duration since first packet transmitted
        * Cumulative number of packets transmitted
        * Cumulative number of bytes transmitted
        * Duration per interval
        * Number of packets transmitted per interval
        * Number of bytes transmitted per interval
        """
        return self._tx_data.over_time

    @property
    def df_rx(self) -> DataFrame:
        """
        Return ``DataFrame`` of receiver over time results.

        Includes:

        * Total duration since first packet received
        * Cumulative number of packets received
        * Cumulative number of bytes received
        * Duration per interval
        * Number of packets received per interval
        * Number of bytes received per interval
        """
        return self._rx_data.over_time

    @property
    def df_tx_bytes(self) -> DataFrame:
        """Return ``DataFrame`` of transmitted bytes per interval."""
        return self._df_tx_bytes

    @property
    def df_rx_bytes(self) -> DataFrame:
        """Return ``DataFrame`` of received bytes per interval."""
        return self._df_rx_bytes

    @property
    def total_tx_bytes(self) -> int:
        """Return total transmitted number of bytes.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._tx_data.total_bytes

    @property
    def total_rx_bytes(self) -> int:
        """Return total received number of bytes.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._rx_data.total_bytes

    @property
    def total_tx_vlan_bytes(self) -> int:
        """Return total number of bytes transmitted in Layer2.5 VLAN header.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._tx_data.total_vlan_bytes

    @property
    def total_rx_vlan_bytes(self) -> int:
        """Return total number of bytes received in Layer2.5 VLAN header.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._rx_data.total_vlan_bytes

    @property
    def total_tx_packets(self) -> int:
        """Return total transmitted number of packets.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._tx_data.total_packets

    @property
    def total_rx_packets(self) -> int:
        """Return total received number of packets.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._rx_data.total_packets

    @property
    def timestamp_tx_first(self) -> Optional[Timestamp]:
        """Return the timestamp of the first transmitted packet."""
        return self._tx_data.timestamp_first

    @property
    def timestamp_tx_last(self) -> Optional[Timestamp]:
        """Return the timestamp of the last transmitted packet."""
        return self._tx_data.timestamp_last

    @property
    def timestamp_rx_first(self) -> Optional[Timestamp]:
        """Return the timestamp of the first received packet.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._rx_data.timestamp_first

    @property
    def timestamp_rx_last(self) -> Optional[Timestamp]:
        """Return the timestamp of the last received packet.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._rx_data.timestamp_last


class LatencyAnalyser(DataAnalyser):

    __slots__ = (
        '_data',
        '_df_latency_min',
        '_df_latency_max',
        '_df_latency_avg',
        '_df_latency_jitter',
        '_max_threshold_latency',
    )

    def __init__(
        self, data: LatencyData, max_threshold_latency: float
    ) -> None:
        super().__init__()
        self._data = data
        self._df_latency_min: DataFrame = None
        self._df_latency_max: DataFrame = None
        self._df_latency_avg: DataFrame = None
        self._df_latency_jitter: DataFrame = None
        self._max_threshold_latency = max_threshold_latency

    def analyse(self) -> None:
        self._df_latency_min = self._data.df_latency[["Minimum"]]
        self._df_latency_max = self._data.df_latency[["Maximum"]]
        self._df_latency_avg = self._data.df_latency[["Average"]]
        self._df_latency_jitter = self._data.df_latency[["Jitter"]]

        final_min_latency = self._data.final_min_latency
        final_max_latency = self._data.final_max_latency
        final_avg_latency = self._data.final_avg_latency
        final_avg_jitter = self._data.final_avg_jitter
        final_packet_count_valid = self._data.final_packet_count_valid
        final_packet_count_invalid = self._data.final_packet_count_invalid

        summary_log = []

        # Add latency summary information to the log
        summary_log.append(
            f"Minimum latency: {_format_milliseconds(final_min_latency)}"
        )
        summary_log.append(
            f"Maximum latency: {_format_milliseconds(final_max_latency)}"
        )
        summary_log.append(
            f"Average latency: {_format_milliseconds(final_avg_latency)}"
        )
        summary_log.append(
            f"Average latency jitter: {_format_milliseconds(final_avg_jitter)}"
        )
        summary_log.append(
            f"Packets with valid latency tag: {final_packet_count_valid}"
        )
        summary_log.append(
            f"Packets with invalid latency tag: {final_packet_count_invalid}"
        )

        self._set_log('\n'.join(summary_log))

        self._set_result(True)
        if final_max_latency is None:
            # NOTE - If we did not receive any data,
            #        we will not have latency values.
            self._set_result(False)
            self._add_failure_cause("No latency related data received")
        elif final_max_latency > self._max_threshold_latency:
            self._set_result(False)
            self._add_failure_cause(
                "Latency has exceeded the maximum allowed latency"
                f" of {self._max_threshold_latency:0.2f} ms"
            )

    @property
    def df_latency(self) -> DataFrame:
        """Return the latency statistics over time.

        Includes result snapshots with content:

        * Index: "Timestamp": Snapshot timestamp
        * "Minimum": Maximum latency within the duration of this snapshot.
        * "Maximum": Maximum latency within the duration of this snapshot.
        * "Average": Average latency within the duration of this snapshot.
        * "Jitter": Average latency jitter within the duration of this snapshot.

        .. note::
           Used for machine-readable detailed reporting.
        """
        return self._data.df_latency

    @property
    def df_latency_min(self) -> DataFrame:
        """Return the minimum latency over time.

        Includes result snapshots with content:

        * Index: "Timestamp": Snapshot timestamp
        * "Minimum": Maximum latency within the duration of this snapshot.

        .. note::
           Used for human-readable detailed reporting.
        """
        return self._df_latency_min

    @property
    def df_latency_max(self) -> DataFrame:
        """Return the maximum latency over time.

        Includes result snapshots with content:

        * Index: "Timestamp": Snapshot timestamp
        * "Maximum": Maximum latency within the duration of this snapshot.

        .. note::
           Used for human-readable detailed reporting.
        """
        return self._df_latency_max

    @property
    def df_latency_avg(self) -> DataFrame:
        """Return the average latency over time.

        Includes result snapshots with content:

        * Index: "Timestamp": Snapshot timestamp
        * "Average": Average latency within the duration of this snapshot.

        .. note::
           Used for human-readable detailed reporting.
        """
        return self._df_latency_avg

    @property
    def df_latency_jitter(self) -> DataFrame:
        """Return the average latency jitter over time.

        Includes result snapshots with content:

        * Index: "Timestamp": Snapshot timestamp
        * "Jitter": Average latency jitter within the duration of this snapshot.

        .. note::
           Used for human-readable detailed reporting.
        """
        return self._df_latency_jitter

    @property
    def final_min_latency(self) -> Optional[float]:
        """Return the minimum latency in milliseconds.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._data.final_min_latency

    @property
    def final_max_latency(self) -> Optional[float]:
        """Return the maximum latency in milliseconds.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._data.final_max_latency

    @property
    def final_avg_latency(self) -> Optional[float]:
        """Return the average latency in milliseconds.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._data.final_avg_latency

    @property
    def final_avg_jitter(self) -> Optional[float]:
        """Return the average jitter in milliseconds.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._data.final_avg_jitter

    @property
    def final_packet_count_valid(self) -> int:
        """Return the number of packets with valid latency tag.

        .. note::
           Used for machine-readable detailed reporting.
        """
        return self._data.final_packet_count_valid

    @property
    def final_packet_count_invalid(self) -> int:
        """Return the number of packets with invalid latency tag.

        .. note::
           Used for machine-readable detailed reporting.
        """
        return self._data.final_packet_count_invalid


class LatencyCDFAnalyser(DataAnalyser):

    __slots__ = (
        '_data',
        '_df_latency',
        '_max_threshold_latency',
        '_quantile',
    )

    def __init__(
        self, data: LatencyDistributionData, max_threshold_latency: float,
        quantile: float
    ) -> None:
        super().__init__()
        self._data = data
        self._df_latency: DataFrame = None
        self._max_threshold_latency = max_threshold_latency
        self._quantile = quantile

    def analyse(self) -> None:
        bucket_width = self._data.bucket_width
        packet_count_buckets = self._data.packet_count_buckets
        # TODO: Avoid hard-coded value(s).
        #     ! Also update (Base)LatencyCDFFrameCountDataGatherer accordingly
        latency_range_min = 0.0 / 1e6
        latency_range_max = len(packet_count_buckets) * bucket_width / 1e6
        assert (latency_range_max == int(50 * self._max_threshold_latency)), (
            "Invalid latency range. Expected hard-coded maximum value"
            " of 50 * max latency threshold."
        )

        self._df_latency = DataFrame(columns=["latency", "percentile"])

        final_min_latency = self._data.final_min_latency
        final_max_latency = self._data.final_max_latency
        final_avg_latency = self._data.final_avg_latency
        final_avg_jitter = self._data.final_avg_jitter
        final_packet_count_valid = self._data.final_packet_count_valid
        # final_packet_count_invalid = self._data.final_packet_count_invalid
        final_packet_count_below_min = self._data.final_packet_count_below_min
        final_packet_count_above_max = self._data.final_packet_count_above_max

        # Build percentiles
        percentiles = []
        i = 0.00
        incr = 10.0
        while i <= 100.00:
            i += incr
            logging.debug("Adding percentile %s", i)
            percentiles.append(i)
            # I know this seems strange, but comparing floats is very tricky.
            # This doesn't work:
            # if ( 100.0 - i ) < incr
            # See  https://stackoverflow.com/questions/3049101/floating-point-equality-in-python-and-in-general  # noqa: E501
            if (100.0 - i - incr) < (incr / 10):
                incr /= 10
                if incr < 0.01:
                    break

        # Process latency
        self._set_result(True)
        if final_packet_count_valid == 0:
            self._set_log("No packets received. Test has failed.")
            self._set_result(False)
            self._add_failure_cause(
                "Did not receive any packets with valid latency tag."
            )
            return

        total_packet_count_in_buckets = sum(packet_count_buckets)
        if (total_packet_count_in_buckets + final_packet_count_below_min +
                final_packet_count_above_max) != final_packet_count_valid:
            logging.warning(
                'Packet count: %r (total in buckets) + %r (below min) '
                '+ %r (above max) != %r (valid): Latency sampling'
                ' was likely active on the ByteBlower server',
                total_packet_count_in_buckets, final_packet_count_below_min,
                final_packet_count_above_max, final_packet_count_valid
            )

        if total_packet_count_in_buckets == 0:
            summary_log = []
            failure_cause = (
                "Failed to validate results. All packets"
                " received outside latency histogram range"
                f" [{latency_range_min}, {latency_range_max}] ms"
            )

            summary_log.append(failure_cause)
            summary_log.append(
                "Number of packets below minimum latency"
                f": {final_packet_count_below_min}"
            )
            summary_log.append(
                "Number of packets above maximum latency"
                f": {final_packet_count_above_max}"
            )

            self._set_log('\n'.join(summary_log))
            self._set_result(False)
            self._add_failure_cause(failure_cause)
            return

        if final_packet_count_below_min:
            logging.warning(
                'Latency CDF data analysis: Number of packets (%r) with'
                ' latency values below minimum are not taken into'
                ' account for the CDF calculation.',
                final_packet_count_below_min
            )

        if final_packet_count_above_max:
            logging.warning(
                'Latency CDF data analysis: Number of packets (%r) with'
                ' latency values above maximum are not taken into'
                ' account for the CDF calculation.',
                final_packet_count_above_max
            )

        log = [
            f"Latency is below {self._max_threshold_latency} ms"
            " for all percentile values."
        ]
        for percentile in percentiles:
            # Let's calculate the latency
            percentile_factor = percentile / 100.0
            if (final_packet_count_above_max / total_packet_count_in_buckets >
                (1.0 - percentile_factor) and percentile <= self._quantile):
                if self.has_passed:
                    failure_cause = (
                        "Latency is larger"
                        f" than {self._max_threshold_latency} ms"
                        f" for quantile {percentile}"
                    )
                    self._set_result(False)
                    self._add_failure_cause(failure_cause)
                    log = [failure_cause]
            # The user will need to know the latency percentile.
            threshold = percentile_factor * total_packet_count_in_buckets
            cumul = 0
            for bucket_number, packet_count_bucket in enumerate(
                    packet_count_buckets, start=1):
                cumul += packet_count_bucket
                if cumul > threshold:
                    df_latency_update = DataFrame(
                        {
                            'latency': [bucket_number * bucket_width],
                            'percentile': percentile,
                        }
                    )

                    # Avoid FutureWarning:
                    #   The behavior of DataFrame concatenation with empty
                    #   or all-NA entries is deprecated. In a future version,
                    #   this will no longer exclude empty or all-NA columns
                    #   when determining the result dtypes. To retain the
                    #   old behavior, exclude the relevant entries before
                    #   the concat operation.
                    if self._df_latency.empty:
                        self._df_latency = df_latency_update
                    else:
                        self._df_latency = concat(
                            [self._df_latency, df_latency_update],
                            ignore_index=True,
                        )

                    if not self.has_passed:
                        bucket_latency = (
                            bucket_number * bucket_width / 1000000.0
                        )
                        log.append(
                            f"\tLatency for quantile {percentile}"
                            f" is {bucket_latency:0.2f}ms."
                        )
                    break
        if final_max_latency is None:
            # NOTE - If we did not receive any data,
            #        we will not have latency values.
            self._set_result(False)
            self._add_failure_cause("No latency related data received")
        elif final_max_latency > self._max_threshold_latency:
            self._set_result(False)
            self._add_failure_cause(
                "Latency has exceeded the maximum allowed latency"
                f" of {self._max_threshold_latency:0.2f} ms"
            )

        # Add latency summary information to the log
        summary_log = []
        summary_log.append(
            f"Minimum latency: {_format_milliseconds(final_min_latency)}"
        )
        summary_log.append(
            f"Maximum latency: {_format_milliseconds(final_max_latency)}"
        )
        summary_log.append(
            f"Average latency: {_format_milliseconds(final_avg_latency)}"
        )
        summary_log.append(
            f"Average latency jitter: {_format_milliseconds(final_avg_jitter)}"
        )
        summary_log.append(
            "Number of packets below minimum latency"
            f": {final_packet_count_below_min}"
        )
        summary_log.append(
            "Number of packets above maximum latency"
            f": {final_packet_count_above_max}"
        )

        self._set_log('\n'.join((*summary_log, *log)))

    @property
    def df_latency(self) -> DataFrame:
        return self._df_latency

    @property
    def final_min_latency(self) -> Optional[float]:
        """Return the minimum latency in milliseconds.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._data.final_min_latency

    @property
    def final_max_latency(self) -> Optional[float]:
        """Return the maximum latency in milliseconds.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._data.final_max_latency

    @property
    def final_avg_latency(self) -> Optional[float]:
        """Return the average latency in milliseconds.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._data.final_avg_latency

    @property
    def final_avg_jitter(self) -> Optional[float]:
        """Return the average jitter in milliseconds.

        .. note::
           Used by the :class:`~.analysis.AnalyserAggregator`.
        """
        return self._data.final_avg_jitter

    @property
    def final_packet_count_valid(self) -> int:
        """Return the number of packets received with valid latency tag.

        .. note::
           Used for machine-readable detailed reporting.
        """
        return self._data.final_packet_count_valid

    @property
    def final_packet_count_invalid(self) -> int:
        """Return the number of packets received with invalid latency tag.

        .. note::
           Used for machine-readable detailed reporting.
        """
        return self._data.final_packet_count_invalid

    @property
    def final_packet_count_below_min(self) -> int:
        """Return the number of packets received with latency below minimum.

        .. note::
           Used for machine-readable detailed reporting.
        """
        return self._data.final_packet_count_below_min

    @property
    def final_packet_count_above_max(self) -> int:
        """Return the number of packets received with latency above maximum.

        .. note::
           Used for machine-readable detailed reporting.
        """
        return self._data.final_packet_count_above_max

    @property
    def latency_histogram(self) -> DataFrame:
        """Return Latency histogram.

        Each bucket contains:

        * ``start``: Start latency of the bucket, in nanoseconds.
        * ``end``: End latency of the bucket, in nanoseconds.
        * ``packets``: Number of packets that were received
          inside the specified latency range.

        See also `Latency distribution in JSON <https://api.byteblower.com/json/byteblower_json_documentation.html#frameBlastingFlows_items_destinations_items_latency_distribution>`_.

        .. note::
           Used for machine-readable detailed reporting.

        :return: Latency histogram
        :rtype: DataFrame
        """  # pylint: disable=line-too-long
        bucket_width = self._data.bucket_width
        # TODO: Avoid hard-coded value(s).
        #     ! Also update (Base)LatencyCDFFrameCountDataGatherer accordingly
        latency_range_min = 0
        # For column names, see
        # https://api.byteblower.com/json/byteblower_json_documentation.html#frameBlastingFlows_items_destinations_items_latency_distribution
        histogram_data = (
            {
                'start': latency_range_min + bucket_index * bucket_width,
                'end': latency_range_min + (bucket_index + 1) * bucket_width,
                'packets': packet_count,
            } for bucket_index, packet_count in
            enumerate(self._data.packet_count_buckets)
        )
        histogram = DataFrame(data=histogram_data)

        return histogram


class MosAnalyser(DataAnalyser):

    __slots__ = (
        '_data_tx_framecount',
        '_data_rx_framecount',
        '_data_latency',
        '_layer2_speed',
        '_df_tx_bytes',
        '_df_rx_bytes',
        '_df_latency_min',
        '_df_latency_max',
        '_df_latency_avg',
        '_df_latency_jitter',
        '_minimum_mos',
    )

    def __init__(
        self, data_tx_framecount: FrameCountData,
        data_rx_framecount: FrameCountData, data_latency: LatencyData,
        layer2_speed: Layer2Speed, minimum_mos: float
    ) -> None:
        super().__init__()
        self._data_tx_framecount = data_tx_framecount
        self._data_rx_framecount = data_rx_framecount
        self._data_latency = data_latency
        self._df_tx_bytes: DataFrame = None
        self._df_rx_bytes: DataFrame = None
        self._df_latency_min: DataFrame = None
        self._df_latency_max: DataFrame = None
        self._df_latency_avg: DataFrame = None
        self._df_latency_jitter: DataFrame = None
        self._layer2_speed = layer2_speed
        self._minimum_mos = minimum_mos

    def analyse(self) -> None:
        df_tx = self._data_tx_framecount.over_time
        df_rx = self._data_rx_framecount.over_time
        self._df_latency_min = self._data_latency.df_latency[["Minimum"]]
        self._df_latency_max = self._data_latency.df_latency[["Maximum"]]
        self._df_latency_avg = self._data_latency.df_latency[["Average"]]
        self._df_latency_jitter = self._data_latency.df_latency[["Jitter"]]

        total_tx_packets = self._data_tx_framecount.total_packets
        total_rx_packets = self._data_rx_framecount.total_packets
        total_tx_bytes = self._data_tx_framecount.total_bytes
        total_rx_bytes = self._data_rx_framecount.total_bytes
        total_tx_vlan_bytes = self._data_tx_framecount.total_vlan_bytes
        total_rx_vlan_bytes = self._data_rx_framecount.total_vlan_bytes

        final_min_latency = self._data_latency.final_min_latency
        final_max_latency = self._data_latency.final_max_latency
        final_avg_latency = self._data_latency.final_avg_latency
        final_avg_jitter = self._data_latency.final_avg_jitter
        final_packet_count_valid = self._data_latency.final_packet_count_valid
        final_packet_count_invalid = self._data_latency.final_packet_count_invalid

        summary_log = []

        # Layer 2 speed calculation info
        summary_log.append(f"{layer2_speed_info(self._layer2_speed)}")

        self._df_tx_bytes = include_ethernet_overhead(
            self._layer2_speed, (df_tx, 'Bytes interval'),
            (df_tx, 'Packets interval')
        )
        self._df_rx_bytes = include_ethernet_overhead(
            self._layer2_speed, (df_rx, 'Bytes interval'),
            (df_rx, 'Packets interval')
        )
        total_tx_bytes = include_ethernet_overhead(
            self._layer2_speed, total_tx_bytes, total_tx_packets
        )
        total_rx_bytes = include_ethernet_overhead(
            self._layer2_speed, total_rx_bytes, total_rx_packets
        )

        total_tx_bytes_without_vlan = total_tx_bytes - total_tx_vlan_bytes
        total_rx_bytes_without_vlan = total_rx_bytes - total_rx_vlan_bytes
        byteloss = total_tx_bytes_without_vlan - total_rx_bytes_without_vlan
        relativebyteloss = 100.0
        if total_tx_bytes != 0:
            relativebyteloss *= byteloss / total_tx_bytes_without_vlan

        packetloss = total_tx_packets - total_rx_packets
        relativepacketloss = 100.0
        if total_tx_packets != 0:
            relativepacketloss *= packetloss / total_tx_packets

        # Append count summary info
        summary_log.append("Transmitted:")
        summary_log.append(f"    {total_tx_packets} packets")
        if total_tx_vlan_bytes:
            summary_log.append(
                f"    {total_tx_bytes_without_vlan} bytes"
                f" (+{total_tx_vlan_bytes} VLAN)"
            )
        else:
            summary_log.append(f"    {total_tx_bytes} bytes")
        summary_log.append("Received:")
        summary_log.append(f"    {total_rx_packets} packets")
        if total_rx_vlan_bytes:
            summary_log.append(
                f"    {total_rx_bytes_without_vlan} bytes"
                f" (+{total_rx_vlan_bytes} VLAN)"
            )
        else:
            summary_log.append(f"    {total_rx_bytes} bytes")
        summary_log.append("Loss:")
        summary_log.append(f"    {byteloss} bytes ({relativebyteloss:0.2f}%)")
        summary_log.append(
            f"    {packetloss} packets ({relativepacketloss:0.2f}%)"
        )

        if not total_rx_bytes:
            # No packets received, so we can't calculate a MOS value.
            failure_cause = "No packets received. MOS calculation is skipped."
            summary_log.append(f"Test has failed. {failure_cause}")
            self._set_log('\n'.join(summary_log))
            self._set_result(False)
            self._add_failure_cause(failure_cause)
            return

        # Add latency summary information to the log
        summary_log.append(
            f"Minimum latency: {_format_milliseconds(final_min_latency)}"
        )
        summary_log.append(
            f"Maximum latency: {_format_milliseconds(final_max_latency)}"
        )
        summary_log.append(
            f"Average latency: {_format_milliseconds(final_avg_latency)}"
        )
        summary_log.append(
            f"Average latency jitter: {_format_milliseconds(final_avg_jitter)}"
        )
        summary_log.append(
            f"Packets with valid latency tag: {final_packet_count_valid}"
        )
        summary_log.append(
            f"Packets with invalid latency tag: {final_packet_count_invalid}"
        )

        # Calculate MOS
        if final_avg_latency is not None and final_avg_jitter is not None:
            mos_score = calculate_mos(
                relativepacketloss, final_avg_latency, final_avg_jitter
            )
            mos_score_str = f"{mos_score:0.3f}"
        else:
            mos_score = None
            mos_score_str = "n/a"

        # Append VoIP info
        summary_log.append(f"Average MOS: {mos_score_str}")

        self._set_log('\n'.join(summary_log))

        self._set_result(True)
        if mos_score is None:
            self._set_result(False)
            self._add_failure_cause(
                "No packets received with valid latency tag."
                " MOS calculation is skipped."
            )
        elif mos_score < self._minimum_mos:
            self._set_result(False)
            self._add_failure_cause(
                "Audio quality is less then desired"
                " minimum Mean Opinion Score (MOS)"
            )

    @property
    def has_rx(self) -> bool:
        """Return if this analyser received data.

        :return: Whether data was received.
        :rtype: bool
        """
        return self._data_rx_framecount.total_bytes > 0

    @property
    def df_tx_bytes(self) -> DataFrame:
        """Return DataFrame of transmitted bytes per interval."""
        return self._df_tx_bytes

    @property
    def df_rx_bytes(self) -> DataFrame:
        """Return DataFrame of received bytes per interval."""
        return self._df_rx_bytes

    @property
    def df_latency_min(self) -> DataFrame:
        return self._df_latency_min

    @property
    def df_latency_max(self) -> DataFrame:
        return self._df_latency_max

    @property
    def df_latency_avg(self) -> DataFrame:
        return self._df_latency_avg

    @property
    def df_latency_jitter(self) -> DataFrame:
        return self._df_latency_jitter


def calculate_mos(
    relative_loss: float, avg_latency: float, avg_jitter: float
) -> float:
    """Calculate MOS.

    :param relative_loss: Relative packet loss
    :type relative_loss: float
    :param avg_latency: Average latency in milliseconds
    :type avg_latency: float
    :param avg_jitter: Average jitter in milliseconds
    :type avg_jitter: float
    :return: MOS value (1.0 - 5.0)
    :rtype: float
    """
    # G.107, 7.1 Calculation of the transmission rating factor, R
    #   R = Ro - Is - Id - Ie-eff + A
    # where
    #   Ro: basic signal-to-noise ratio, including noise sources
    #       such as circuit noise and room noise.
    #   Is: combination of all impairments which occur more or less
    #       simultaneously with the voice signal.
    #   Id: impairments caused by delay
    #   Ie-eff: Effective equipment impairment factor represents
    #           impairments caused by low bit-rate codecs.
    #           It also includes impairment due to randomly
    #           distributed packet losses.
    #   A: Advantage factor allows for compensation of impairment factors
    #      when the user benefits from other types of access to the user.
    # Where (G.107, 7.7 Default values):
    #   TODO: Where does this 93.2 come from?
    #   Ro - Is = 93.2
    #   Ie = 0
    #   Ppl = 0 [no packet loss]
    #   Bpl = *** [See G.113]
    #   BurstR = 1 [random packet loss, not bursty]
    #   => Ie-eff = 0
    #   A = 0
    # From G.113, Appendix I, Provisional planning values for the
    #      equipment impairment factor, Ie, and packet-loss robustness
    #      factor, Bpl:
    #   Ie = 0 [PCM, G.711, 10ms]
    #   Bpl = 4.3/25.1 [G.711; random packet loss]
    effective_latency = avg_latency + (avg_jitter * 2) + 10
    if effective_latency < 160:
        r_value = 93.2 - (effective_latency / 40)
    else:
        r_value = 93.2 - (effective_latency - 120) / 10
    r_value = r_value - (relative_loss * 2.5)
    r_value = clamp(r_value, 0, 100)
    mos_score = 1 + (0.035 * r_value) + (0.000007 * r_value
                                         ) * (r_value - 60) * (100 - r_value)
    return mos_score


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


def _format_milliseconds(value: Optional[float]) -> str:
    if value is not None:
        return f"{value:0.3f} ms"
    return "n/a"
