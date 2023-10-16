import logging
from typing import Optional  # for type hinting

from ..data_analysis.frameblasting import (
    FrameCountAnalyser,
    LatencyAnalyser,
    LatencyCDFAnalyser,
    MosAnalyser,
)
from ..helpers import to_bitrate
from ..plotting import GenericChart
from .renderer import AnalysisDetails  # for type hinting
from .renderer import Renderer


class FrameCountRenderer(Renderer):

    __slots__ = ('_data_analyser', )

    def __init__(self, data_analyser: FrameCountAnalyser) -> None:
        super().__init__()
        self._data_analyser = data_analyser

    def render(self) -> str:
        analysis_log = self._data_analyser.log

        # Get the data
        df_tx = self._data_analyser.df_tx_bytes
        df_rx = self._data_analyser.df_rx_bytes

        df_tx_bits = to_bitrate((df_tx, 'Bytes interval'))
        df_rx_bits = to_bitrate((df_rx, 'Bytes interval'))

        # Set the summary
        result = self._verbatim(analysis_log)

        # Build the graph
        chart = GenericChart(
            "Throughput",
            x_axis_options={"type": "datetime"},
            chart_options={"zoomType": "x"}
        )
        chart.add_series(
            list(df_tx_bits.itertuples(index=True)),
            "line",
            "TX",
            "Dataspeed",
            "bits/s",
        )
        chart.add_series(
            list(df_rx_bits.itertuples(index=True)),
            "line",
            "RX",
            "Dataspeed",
            "bits/s",
        )
        result += chart.plot(
            f'frame_count_container{FrameCountRenderer.container_id}'
        )
        FrameCountRenderer.container_id += 1

        return result

    def details(self) -> Optional[AnalysisDetails]:
        # Get the data
        timestamp_tx_first = self._data_analyser.timestamp_tx_first
        timestamp_tx_last = self._data_analyser.timestamp_tx_last
        timestamp_rx_first = self._data_analyser.timestamp_rx_first
        timestamp_rx_last = self._data_analyser.timestamp_rx_last
        total_tx_packets = self._data_analyser.total_tx_packets
        total_rx_packets = self._data_analyser.total_rx_packets
        total_tx_bytes = self._data_analyser.total_tx_bytes
        total_rx_bytes = self._data_analyser.total_rx_bytes
        df_tx = self._data_analyser.df_tx[[
            'Duration interval',
            'Packets interval',
            'Bytes interval',
        ]]
        df_rx = self._data_analyser.df_rx[[
            'Duration interval',
            'Packets interval',
            'Bytes interval',
        ]]

        # Update naming
        df_rx = df_rx.rename(
            columns={
                'Duration interval': 'duration',
                'Bytes interval': 'bytes',
                'Packets interval': 'packets',
            }
        )
        df_tx = df_tx.rename(
            columns={
                'Duration interval': 'duration',
                'Bytes interval': 'bytes',
                'Packets interval': 'packets',
            }
        )

        # Set the details
        # TODO: How to put VLAN bytes info in JSON?
        details: AnalysisDetails = {
            'source': {
                'sent': {
                    'firstPacketTime': timestamp_tx_first,
                    'lastPacketTime': timestamp_tx_last,
                    'packets': total_tx_packets,
                    'bytes': total_tx_bytes,
                    'overTimeResults': df_tx,
                },
            },
            'destination': {
                'received': {
                    'firstPacketTime': timestamp_rx_first,
                    'lastPacketTime': timestamp_rx_last,
                    'packets': total_rx_packets,
                    'bytes': total_rx_bytes,
                    'overTimeResults': df_rx,
                },
            },
        }

        return details


class LatencyFrameCountRenderer(Renderer):

    __slots__ = (
        '_framecount_analyser',
        '_latency_analyser',
    )

    def __init__(
        self, framecount_analyser: FrameCountAnalyser,
        latency_analyser: LatencyAnalyser
    ) -> None:
        super().__init__()
        self._framecount_analyser = framecount_analyser
        self._latency_analyser = latency_analyser

    def render(self) -> str:
        analysis_log = '\n'.join(
            (self._framecount_analyser.log, self._latency_analyser.log)
        )

        # Get the data
        df_tx = self._framecount_analyser.df_tx_bytes
        df_rx = self._framecount_analyser.df_rx_bytes
        df_latency_min = self._latency_analyser.df_latency_min
        df_latency_max = self._latency_analyser.df_latency_max
        df_latency_avg = self._latency_analyser.df_latency_avg
        df_latency_jitter = self._latency_analyser.df_latency_jitter

        df_tx_bits = to_bitrate((df_tx, 'Bytes interval'))
        df_rx_bits = to_bitrate((df_rx, 'Bytes interval'))

        # Set the summary
        result = self._verbatim(analysis_log)

        # Build the graph
        chart = GenericChart(
            "Flow results",
            x_axis_options={"type": "datetime"},
            chart_options={"zoomType": "x"}
        )
        chart.add_series(
            list(df_tx_bits.itertuples(index=True)),
            "line",
            "TX",
            "Dataspeed",
            "bits/s",
        )
        chart.add_series(
            list(df_rx_bits.itertuples(index=True)),
            "line",
            "RX",
            "Dataspeed",
            "bits/s",
        )
        chart.add_series(
            list(df_latency_min.itertuples(index=True)), "line", "Minimum",
            "Latency", "Milliseconds"
        )
        chart.add_series(
            list(df_latency_max.itertuples(index=True)), "line", "Maximum",
            "Latency", "Milliseconds"
        )
        chart.add_series(
            list(df_latency_avg.itertuples(index=True)), "line", "Average",
            "Latency", "Milliseconds"
        )
        chart.add_series(
            list(df_latency_jitter.itertuples(index=True)), "line", "Jitter",
            "Latency", "Milliseconds"
        )
        result += chart.plot(
            'latency_frame_count_container'
            f'{LatencyFrameCountRenderer.container_id}'
        )
        LatencyFrameCountRenderer.container_id += 1

        return result

    def details(self) -> Optional[AnalysisDetails]:
        # Get the data
        # Frame count data
        timestamp_tx_first = self._framecount_analyser.timestamp_tx_first
        timestamp_tx_last = self._framecount_analyser.timestamp_tx_last
        timestamp_rx_first = self._framecount_analyser.timestamp_rx_first
        timestamp_rx_last = self._framecount_analyser.timestamp_rx_last
        total_tx_packets = self._framecount_analyser.total_tx_packets
        total_rx_packets = self._framecount_analyser.total_rx_packets
        total_tx_bytes = self._framecount_analyser.total_tx_bytes
        total_rx_bytes = self._framecount_analyser.total_rx_bytes
        df_tx = self._framecount_analyser.df_tx[[
            'Duration interval',
            'Packets interval',
            'Bytes interval',
        ]]
        df_rx = self._framecount_analyser.df_rx[[
            'Duration interval',
            'Packets interval',
            'Bytes interval',
        ]]
        # Latency data
        final_packet_count_valid = \
            self._latency_analyser.final_packet_count_valid
        final_packet_count_invalid = \
            self._latency_analyser.final_packet_count_invalid
        final_min_latency = self._latency_analyser.final_min_latency
        final_max_latency = self._latency_analyser.final_max_latency
        final_avg_latency = self._latency_analyser.final_avg_latency
        final_avg_jitter = self._latency_analyser.final_avg_jitter
        df_latency = self._latency_analyser.df_latency

        # Update naming
        df_rx = df_rx.rename(
            columns={
                'Duration interval': 'duration',
                'Bytes interval': 'bytes',
                'Packets interval': 'packets',
            }
        )
        df_tx = df_tx.rename(
            columns={
                'Duration interval': 'duration',
                'Bytes interval': 'bytes',
                'Packets interval': 'packets',
            }
        )
        df_latency = df_latency.rename(
            columns={
                'Minimum': 'minimum',
                'Maximum': 'maximum',
                'Average': 'average',
                'Jitter': 'jitter',
            }
        )

        # Set the details
        # TODO: How to put VLAN bytes info in JSON?
        details: AnalysisDetails = {
            'source': {
                'sent': {
                    'firstPacketTime': timestamp_tx_first,
                    'lastPacketTime': timestamp_tx_last,
                    'packets': total_tx_packets,
                    'bytes': total_tx_bytes,
                    'overTimeResults': df_tx,
                },
            },
            'destination': {
                'received': {
                    'firstPacketTime': timestamp_rx_first,
                    'lastPacketTime': timestamp_rx_last,
                    'packets': total_rx_packets,
                    'bytes': total_rx_bytes,
                    'overTimeResults': df_rx,
                },
                'latency': {
                    'packetsValid': final_packet_count_valid,
                    'packetsInvalid': final_packet_count_invalid,
                    'minimum': final_min_latency,
                    'maximum': final_max_latency,
                    'average': final_avg_latency,
                    'jitter': final_avg_jitter,
                    'overTimeResults': df_latency,
                },
            },
        }

        return details


class LatencyCDFRenderer(Renderer):

    __slots__ = (
        '_framecount_analyser',
        '_latency_cdf_analyser',
    )

    def __init__(
        self, framecount_analyser: FrameCountAnalyser,
        latency_cdf_analyser: LatencyCDFAnalyser
    ) -> None:
        super().__init__()
        self._framecount_analyser = framecount_analyser
        self._latency_cdf_analyser = latency_cdf_analyser

    def render(self) -> str:
        analysis_log = '\n'.join(
            (self._framecount_analyser.log, self._latency_cdf_analyser.log)
        )

        # Get the data
        rxpacketstotal = self._latency_cdf_analyser.final_packet_count_valid
        # NOTE: Copy to avoid altering the original values
        #     ! That would fail other parts using the latency CDF results
        latency_cdf = self._latency_cdf_analyser.df_latency.copy()

        # Set the summary
        result = self._verbatim(analysis_log)

        if not rxpacketstotal:
            return result

        # Build the graphs
        # [ns] -> [ms]
        latency_cdf["latency"] /= 1000 * 1000.0
        # Set the latency column as index
        latency_cdf = latency_cdf.set_index("latency")

        # CDF
        logging.debug('Latency CDF: %s', latency_cdf)

        chart = GenericChart(
            "Latency CDF",
            x_axis_title="Latency [ms]",
            chart_options={"zoomType": "x"},
            x_axis_options={"labels": {
                "format": "{value} ms"
            }},
        )

        chart.add_series(
            list(latency_cdf.itertuples(index=True)),
            "line",
            "latency CDF",
            "",
            "",
            y_axis_options={
                # "reversed": "true",
                "title": "percentile",
                "labels": {
                    "formatter":
                    "function() {"
                    " let str = this.value;"
                    " str += '%';"
                    " return str }"
                },
                # "type": "logarithmic",
                "tickInterval": 1,
                "minorTickInterval": 0.1,
                "endOnTick": "true",
                "gridLineWidth": 1,
                "min": 0.0,
                "max": 100.0,
            },
        )
        result += chart.plot(
            f'latency_cdf_container{LatencyCDFRenderer.container_id}'
        )
        LatencyCDFRenderer.container_id += 1

        # CCDF

        # Complement of the percentile
        latency_cdf["percentile"] = 100.0 - latency_cdf["percentile"]

        chart = GenericChart(
            "Latency CCDF",
            x_axis_title="Latency [ms]",
            chart_options={"zoomType": "x"},
            x_axis_options={"labels": {
                "format": "{value} ms"
            }},
        )

        chart.add_series(
            list(latency_cdf.itertuples(index=True)),
            "line",
            "latency CCDF",
            "",
            "",
            y_axis_options={
                # "reversed": "true",
                "title": "percentile",
                "labels": {
                    "formatter":
                    "function() {"
                    " let str = 'P';"
                    " str += (100.0 - this.value);"
                    " return str }"
                },
                "type": "logarithmic",
                "tickInterval": 1,
                "minorTickInterval": 0.1,
                "endOnTick": "true",
                "gridLineWidth": 1,
                "max": 100.0,
                "min": 0.1,
            },
        )
        result += chart.plot(
            f'latency_ccdf_container{LatencyCDFRenderer.container_id}'
        )
        LatencyCDFRenderer.container_id += 1

        return result

    def details(self) -> Optional[AnalysisDetails]:
        # Get the data
        # Frame count data
        timestamp_tx_first = self._framecount_analyser.timestamp_tx_first
        timestamp_tx_last = self._framecount_analyser.timestamp_tx_last
        timestamp_rx_first = self._framecount_analyser.timestamp_rx_first
        timestamp_rx_last = self._framecount_analyser.timestamp_rx_last
        total_tx_packets = self._framecount_analyser.total_tx_packets
        total_rx_packets = self._framecount_analyser.total_rx_packets
        total_tx_bytes = self._framecount_analyser.total_tx_bytes
        total_rx_bytes = self._framecount_analyser.total_rx_bytes
        df_tx = self._framecount_analyser.df_tx[[
            'Duration interval',
            'Packets interval',
            'Bytes interval',
        ]]
        df_rx = self._framecount_analyser.df_rx[[
            'Duration interval',
            'Packets interval',
            'Bytes interval',
        ]]
        # Latency data
        final_packet_count_valid = \
            self._latency_cdf_analyser.final_packet_count_valid
        final_packet_count_invalid = \
            self._latency_cdf_analyser.final_packet_count_invalid
        final_packet_count_below_min = \
            self._latency_cdf_analyser.final_packet_count_below_min
        final_packet_count_above_max = \
            self._latency_cdf_analyser.final_packet_count_above_max
        final_min_latency = self._latency_cdf_analyser.final_min_latency
        final_max_latency = self._latency_cdf_analyser.final_max_latency
        final_avg_latency = self._latency_cdf_analyser.final_avg_latency
        final_avg_jitter = self._latency_cdf_analyser.final_avg_jitter
        # NOTE: Copy to avoid altering the original values
        #     ! That would fail other parts using latency histogram results
        latency_histogram = self._latency_cdf_analyser.latency_histogram.copy()
        # NOTE: Copy to avoid altering the original values
        #     ! That would fail other parts using latency CDF results
        latency_cdf = self._latency_cdf_analyser.df_latency.copy()

        # Update naming
        df_rx = df_rx.rename(
            columns={
                'Duration interval': 'duration',
                'Bytes interval': 'bytes',
                'Packets interval': 'packets',
            }
        )
        df_tx = df_tx.rename(
            columns={
                'Duration interval': 'duration',
                'Bytes interval': 'bytes',
                'Packets interval': 'packets',
            }
        )

        # [ns] -> [ms]
        latency_cdf["latency"] /= 1e6
        latency_histogram[["start", "end"]] /= 1e6

        # Set the details
        # TODO: How to put VLAN bytes info in JSON?
        distribution_details = latency_histogram.to_dict(orient='records')
        cdf_details = latency_cdf.to_dict(orient='records')
        details: AnalysisDetails = {
            'source': {
                'sent': {
                    'firstPacketTime': timestamp_tx_first,
                    'lastPacketTime': timestamp_tx_last,
                    'packets': total_tx_packets,
                    'bytes': total_tx_bytes,
                    'overTimeResults': df_tx,
                },
            },
            'destination': {
                'received': {
                    'firstPacketTime': timestamp_rx_first,
                    'lastPacketTime': timestamp_rx_last,
                    'packets': total_rx_packets,
                    'bytes': total_rx_bytes,
                    'overTimeResults': df_rx,
                },
                'latency': {
                    'minimum': final_min_latency,
                    'maximum': final_max_latency,
                    'average': final_avg_latency,
                    'jitter': final_avg_jitter,
                    'packetsValid': final_packet_count_valid,
                    'packetsInvalid': final_packet_count_invalid,
                    'packetsBelowMinimum': final_packet_count_below_min,
                    'packetsAboveMaximum': final_packet_count_above_max,
                    'distribution': distribution_details,
                    # NOTE: We don't want the index,
                    # just the latency/percentile records:
                    'cdf': cdf_details,
                },
            },
        }

        return details


class MosRenderer(Renderer):

    __slots__ = ('_analyser', )

    def __init__(self, analyser: MosAnalyser) -> None:
        super().__init__()
        self._analyser = analyser

    def render(self) -> str:
        analysis_log = self._analyser.log

        # Get the data
        df_tx = self._analyser.df_tx_bytes
        df_rx = self._analyser.df_rx_bytes
        has_rx = self._analyser.has_rx
        df_latency_min = self._analyser.df_latency_min
        df_latency_max = self._analyser.df_latency_max
        df_latency_avg = self._analyser.df_latency_avg
        df_latency_jitter = self._analyser.df_latency_jitter

        df_tx_bits = to_bitrate((df_tx, 'Bytes interval'))
        df_rx_bits = to_bitrate((df_rx, 'Bytes interval'))

        # Set the summary
        result = self._verbatim(analysis_log)

        if not has_rx:
            return result

        # Build the graph
        chart = GenericChart(
            "Flow results",
            x_axis_options={"type": "datetime"},
            chart_options={"zoomType": "x"}
        )
        chart.add_series(
            list(df_tx_bits.itertuples(index=True)),
            "line",
            "TX",
            "Dataspeed",
            "bits/s",
        )
        chart.add_series(
            list(df_rx_bits.itertuples(index=True)),
            "line",
            "RX",
            "Dataspeed",
            "bits/s",
        )
        chart.add_series(
            list(df_latency_min.itertuples(index=True)), "line", "Minimum",
            "Latency", "Milliseconds"
        )
        chart.add_series(
            list(df_latency_max.itertuples(index=True)), "line", "Maximum",
            "Latency", "Milliseconds"
        )
        chart.add_series(
            list(df_latency_avg.itertuples(index=True)), "line", "Average",
            "Latency", "Milliseconds"
        )
        chart.add_series(
            list(df_latency_jitter.itertuples(index=True)), "line", "Jitter",
            "Latency", "Milliseconds"
        )
        result += chart.plot(f'mos_container{MosRenderer.container_id}')
        MosRenderer.container_id += 1

        return result
