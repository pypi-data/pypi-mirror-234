import logging
from abc import ABC, abstractmethod
from typing import (  # for type hinting
    Any,
    List,
    Mapping,
    Optional,
    Tuple,
    Union,
)

from pandas import Timestamp  # for type hinting
from pandas import DataFrame

from .._analysis.helpers import include_ethernet_overhead, to_bitrate
from .._report.options import Layer2Speed, layer2_speed_info
from .flow_analyser import FlowAnalyser  # for type hinting
from .framelossanalyser import BaseFrameLossAnalyser
from .latencyanalyser import (
    BaseLatencyCDFFrameLossAnalyser,
    BaseLatencyFrameLossAnalyser,
)
from .plotting import GenericChart

# Type aliases
_FrameCountAnalysers = (BaseFrameLossAnalyser, )
_OverTimeLatencyAnalysers = (BaseLatencyFrameLossAnalyser, )
# NOTE: CDF analyser does not support "over time" results (yet):
_OverTimeSupportedAnalysersList = (
    _FrameCountAnalysers + _OverTimeLatencyAnalysers
)
_SummaryLatencyAnalysers = (
    BaseLatencyFrameLossAnalyser,
    BaseLatencyCDFFrameLossAnalyser,  # only supported for summarizing
)
_SummarySupportedAnalysersList = (
    _FrameCountAnalysers + _SummaryLatencyAnalysers
)
_OverTimeOrSummarySupportedAnalysersList = _SummarySupportedAnalysersList
_SUPPORT_LEVEL = (
    BaseLatencyCDFFrameLossAnalyser,  # Frame count & Latency; summary only
    BaseFrameLossAnalyser,  # Frame count; summary & over time
    BaseLatencyFrameLossAnalyser,  # Frame count & Latency; summary & over time
)
# NOTE: Required Python 3.11 or later:
# SupportedAnalysers = Union[*_OverTimeSupportedAnalysersList]
#: :class:`~.flowanalyser.FlowAnalyser` implementations which are supported in
#: the :class:`AnalyserAggregator`.
PossiblySupportedAnalysers = Union[BaseFrameLossAnalyser,
                                   BaseLatencyFrameLossAnalyser,
                                   BaseLatencyCDFFrameLossAnalyser]
# JsonAnalyserAggregator support all analysers
# (it only supports summary results for now)
_SummarySupportedAnalysers = PossiblySupportedAnalysers
# Recursive content type
# ! FIXME - Causes error while generating Sphinx documentation
#         * exception: maximum recursion depth exceeded
#  Content = Mapping[str, Union['Content', str, int, float, bool]]
RecursiveContent = Any  # Woraround to avoid recursion depth error
Content = Mapping[str, Union[RecursiveContent, str, int, float, bool]]


class AnalyserAggregator(ABC):

    # (minimum) number of analysers required for aggregation
    _ANALYSER_COUNT = 2

    __slots__ = ('_analysers', )

    def __init__(self) -> None:
        # This will store the analysers based on their tags.
        # For each of these tags, we will aggregate the resuls
        self._analysers: Mapping[str, List[PossiblySupportedAnalysers]] = {}

    @abstractmethod
    def supports_analyser(self, analyser: FlowAnalyser) -> bool:
        """Return whether the flow analyser is supported."""
        raise NotImplementedError()

    def order_by_support_level(
        self, analyser_list: List[PossiblySupportedAnalysers]
    ) -> List[PossiblySupportedAnalysers]:
        """Order a list of flow analysers by aggregation support level.

        The flow analysers are ordered by the highest level of support they
        provide for aggregating results. "*Result aggregation support*" covers
        both results over time and summarization.

        :param analyser_list: List of flow analysers to order
        :type analyser_list: List[PossiblySupportedAnalysers]
        :return: List of ordered flow analysers
        :rtype: List[PossiblySupportedAnalysers]
        """
        supported_analyser_list = (
            analyser for analyser in analyser_list
            if self.supports_analyser(analyser)
        )

        def support_level(analyser: PossiblySupportedAnalysers) -> int:
            for level, analyser_type in enumerate(_SUPPORT_LEVEL):
                if isinstance(analyser, analyser_type):
                    return level + 1
            return 0

        sorted_analyser_list = sorted(
            supported_analyser_list, key=support_level, reverse=True
        )
        return sorted_analyser_list

    def add_analyser(self, analyser: PossiblySupportedAnalysers) -> None:
        for tag in analyser.tags:
            logging.info(
                '%s: Adding analyser %s to tag %s',
                type(self).__name__, analyser, tag
            )
            if tag in self._analysers:
                self._analysers[tag].append(analyser)
            else:
                self._analysers[tag] = [analyser]

    def can_render(self) -> bool:
        # Check if we have something to render
        return any(
            (
                len(analysers) >= self._ANALYSER_COUNT
                for analysers in self._analysers.values()
            )
        )

    @staticmethod
    def _parse_key(key: str) -> str:
        if key.endswith('analyser'):
            key = key.rpartition('_')[0]
        return key


class HtmlAnalyserAggregator(AnalyserAggregator):

    def supports_analyser(self, analyser: FlowAnalyser) -> bool:
        """Return whether the flow analyser is supported."""
        return isinstance(analyser, _OverTimeOrSummarySupportedAnalysersList)

    def render(self, layer2_speed: Layer2Speed) -> str:
        # Render our aggregate result
        result = '<h3>Aggregated results</h3>\n'\
            f'<pre>\n{layer2_speed_info(layer2_speed)}\n</pre>\n'
        result_charts = ''
        logging.debug('I should render something')

        df_summary = DataFrame(
            columns=[
                'TX frames',
                'RX frames',
                'Frame loss (%)',
                'TX Bytes',
                'RX Bytes',
                'Byte loss (%)',
                'Duration',
                'Average throughput [kbps]',
                'Status',
            ]
        )

        for key, analysers in self._analysers.items():
            if len(analysers) < self._ANALYSER_COUNT:
                continue

            logging.debug('I can aggregate on %s', key)
            title = AnalyserAggregator._parse_key(key)
            title = title.replace('_', ' ').upper()
            logging.info('Title: %s', title)

            # Summary results

            (
                test_passed,
                total_rx_packets,
                total_tx_packets,
                total_rx_bytes,
                total_tx_bytes,
                total_rx_vlan_bytes,
                total_tx_vlan_bytes,
                _timestamp_tx_first,
                _timestamp_tx_last,
                timestamp_rx_first,
                timestamp_rx_last,
                latency_results,
            ) = _summarize_analysers(analysers, layer2_speed)

            total_packets_loss = total_tx_packets - total_rx_packets
            if total_tx_packets:
                total_packets_relative_loss = (
                    100 * total_packets_loss / total_tx_packets
                )
                total_packets_relative_loss_str = (
                    f'{total_packets_relative_loss:.2f}%'
                )
            else:
                total_packets_relative_loss_str = 'n/a'
            total_tx_bytes_without_vlan = total_tx_bytes - total_tx_vlan_bytes
            total_rx_bytes_without_vlan = total_rx_bytes - total_rx_vlan_bytes
            total_bytes_loss_without_vlan = (
                total_tx_bytes_without_vlan - total_rx_bytes_without_vlan
            )
            if total_tx_bytes:
                total_bytes_relative_loss = (
                    100 * total_bytes_loss_without_vlan /
                    total_tx_bytes_without_vlan
                )
                total_bytes_relative_loss_str = (
                    f'{total_bytes_relative_loss:.2f}%'
                )
            else:
                total_bytes_relative_loss_str = 'n/a'
            if timestamp_rx_last is None or timestamp_rx_first is None:
                duration = 0
            else:
                duration = timestamp_rx_last - timestamp_rx_first
            if duration:
                avg_rx_throughput = (
                    total_rx_bytes / duration.total_seconds() * 8 / 1024
                )
                avg_rx_throughput_str = f'{avg_rx_throughput:.2f}'
            else:
                avg_rx_throughput_str = 'n/a'

            if total_tx_vlan_bytes:
                df_summary.rename(
                    columns={
                        'TX Bytes': 'TX Bytes (+VLAN)',
                    }, inplace=True
                )
                total_tx_bytes_str = (
                    f'{total_tx_bytes_without_vlan} (+{total_tx_vlan_bytes})'
                )
            else:
                total_tx_bytes_str = f'{total_tx_bytes}'
            if total_rx_vlan_bytes:
                df_summary.rename(
                    columns={
                        'RX Bytes': 'RX Bytes (+VLAN)',
                    }, inplace=True
                )
                total_rx_bytes_str = (
                    f'{total_rx_bytes_without_vlan} (+{total_rx_vlan_bytes})'
                )
            else:
                total_rx_bytes_str = f'{total_rx_bytes}'

            df_summary.loc[title] = (
                total_tx_packets,
                total_rx_packets,
                f'{total_packets_loss} ({total_packets_relative_loss_str})',
                total_tx_bytes_str,
                total_rx_bytes_str,
                f'{total_bytes_loss_without_vlan}'
                f' ({total_bytes_relative_loss_str})',
                duration,
                avg_rx_throughput_str,
                'PASSED' if test_passed else 'FAILED',
            )

            # TODO - Add latency summary results

            # Over-time results

            if _analyser_frame_count_over_time(analysers[0]):
                df_tx = analysers[0].df_tx_bytes[['Bytes interval']]
                df_rx = analysers[0].df_rx_bytes[['Bytes interval']]
            else:
                df_tx = DataFrame(columns=['Bytes interval'])
                df_rx = DataFrame(columns=['Bytes interval'])

            for analyser in analysers[1:]:
                if not _analyser_frame_count_over_time(analyser):
                    continue

                logging.debug('Adding extra elements to sum')
                if analyser._layer2_speed != layer2_speed:
                    logging.warning(
                        'Layer2 speed reporting option mismatch'
                        ' between analyser and aggregator.'
                        ' You will see unexpected results!'
                    )
                df_tx = df_tx.add(
                    analyser.df_tx_bytes[['Bytes interval']], fill_value=0
                )
                df_rx = df_rx.add(
                    analyser.df_rx_bytes[['Bytes interval']], fill_value=0
                )

            if df_tx.empty and df_rx.empty:
                continue

            chart = GenericChart(
                'Aggregate Throughput',
                x_axis_options={"type": "datetime"},
                chart_options={"zoomType": "x"}
            )
            if not df_tx.empty:
                df_tx_bits = to_bitrate((df_tx, 'Bytes interval'))
                chart.add_series(
                    list(df_tx_bits.itertuples(index=True)),
                    'line',
                    'TX',
                    'Dataspeed',
                    'bits/s',
                )
            if not df_rx.empty:
                df_rx_bits = to_bitrate((df_rx, 'Bytes interval'))
                chart.add_series(
                    list(df_rx_bits.itertuples(index=True)),
                    'line',
                    'RX',
                    'Dataspeed',
                    'bits/s',
                )

            result_charts += f'<h4>{title}</h4>'
            chart_container_id = title.replace(' ', '_').lower()
            result_charts += chart.plot(
                f'analyser_aggregator_container_{chart_container_id}'
            )

        # Compose the aggregated results:
        result += df_summary.to_html()
        result += result_charts

        return result


class JsonAnalyserAggregator(AnalyserAggregator):

    def supports_analyser(self, analyser: FlowAnalyser) -> bool:
        """Return whether the flow analyser is supported."""
        return isinstance(analyser, _SummarySupportedAnalysersList)

    # Also "aggregate" for a single Analyser (DUT)
    _ANALYSER_COUNT = 1

    def summarize(self) -> Content:
        """Summarize our aggregate result.

        :raises RuntimeError: When we have aggregated result name clashes.
        :return: Dictionary with summary result.
        :rtype: Content
        """
        summary: Content = {}
        logging.debug('I should summarize something')

        for key, analysers in self._analysers.items():
            if len(analysers) < self._ANALYSER_COUNT:
                continue

            logging.debug('I can aggregate on %s', key)
            summary_key = AnalyserAggregator._parse_key(key)
            # Convert to 'camelCase', from dash- and/or space-separated string:
            summary_key = _to_camel_case(summary_key)
            logging.info('Summary key: %r', summary_key)
            if summary_key in summary:
                logging.warning(
                    'Overwriting summary results in %r by %r', summary_key, key
                )
                raise RuntimeError(
                    'Overwriting summary results'
                    f' for {summary_key!r} analysers'
                )

            (
                test_passed,
                total_rx_packets,
                total_tx_packets,
                total_rx_bytes,
                total_tx_bytes,
                _total_rx_vlan_bytes,
                _total_tx_vlan_bytes,
                timestamp_tx_first,
                timestamp_tx_last,
                timestamp_rx_first,
                timestamp_rx_last,
                latency_results,
            ) = _summarize_analysers(analysers, None)

            # TODO: How to put VLAN bytes info in JSON?

            test_summary = {
                'status': {
                    'passed': test_passed,
                },
                'sent': {
                    'firstPacketTime': timestamp_tx_first,
                    'lastPacketTime': timestamp_tx_last,
                    'packets': total_tx_packets,
                    'bytes': total_tx_bytes,
                },
                'received': {
                    'firstPacketTime': timestamp_rx_first,
                    'lastPacketTime': timestamp_rx_last,
                    'packets': total_rx_packets,
                    'bytes': total_rx_bytes,
                },
            }

            if latency_results:
                (
                    final_min_latency,
                    final_max_latency,
                    final_avg_latency,
                    final_avg_jitter,
                ) = latency_results
                test_summary['latency'] = {
                    'minimum': final_min_latency,
                    'maximum': final_max_latency,
                    'average': final_avg_latency,
                    'jitter': final_avg_jitter,
                }

            summary[summary_key] = test_summary

        return summary


def _summarize_analysers(
    analysers: List[PossiblySupportedAnalysers],
    layer2_speed: Optional[Layer2Speed]
) -> Tuple[bool, int, int, int, int, int, int, Optional[Timestamp],
           Optional[Timestamp], Optional[Timestamp], Optional[Timestamp],
           Optional[Tuple[Optional[float], Optional[float], Optional[float],
                          Optional[float]]]]:
    """Summarize the results of the analysers.

    :param analysers: List of analysers to summarize.
    :type analysers: List[PossiblySupportedAnalysers]
    :param layer2_speed: Layer 2 speed conversion to make.
       Don't do any conversion if ``None`` is provided.
    :type layer2_speed: Optional[Layer2Speed], optional
    :raises ValueError: When an unsupported Layer2speed is given.
    :return: Summarized values
    :rtype: Tuple[bool, int, int, int, int, int, int, Optional[Timestamp],
       Optional[Timestamp], Optional[Timestamp], Optional[Timestamp],
       Optional[Tuple[Optional[float], Optional[float], Optional[float],
       Optional[float]]]]
    """
    analyser = analysers[0]
    test_passed = analyser.has_passed
    total_rx_packets = analyser.total_rx_packets
    total_tx_packets = analyser.total_tx_packets
    total_rx_bytes = analyser.total_rx_bytes
    total_tx_bytes = analyser.total_tx_bytes
    total_rx_vlan_bytes = analyser.total_rx_vlan_bytes
    total_tx_vlan_bytes = analyser.total_tx_vlan_bytes
    timestamp_tx_first = analyser.timestamp_tx_first
    timestamp_tx_last = analyser.timestamp_tx_last
    timestamp_rx_first = analyser.timestamp_rx_first
    timestamp_rx_last = analyser.timestamp_rx_last
    has_latency = False
    final_min_latency: Optional[float] = None
    final_max_latency: Optional[float] = None
    final_avg_latency: Optional[float] = None
    final_avg_jitter: Optional[float] = None

    if _analyser_has_latency_summary(analyser):
        # Do return the latency-related values whether packets
        # have been received or not:
        # * No latency analysers
        #   => no entries
        # * Latency analysers but no packets received
        #   => entries with `None` value
        has_latency = True
        if total_rx_packets:
            final_min_latency = analyser.final_min_latency
            final_max_latency = analyser.final_max_latency
            final_avg_latency = analyser.final_avg_latency
            final_avg_jitter = analyser.final_avg_jitter
        else:
            logging.warning(
                'Ignoring latency for analyser on flow %r', analyser.flow.name
            )

    for analyser in analysers[1:]:
        logging.debug('Adding extra counters to sum')
        if test_passed is None:
            test_passed = analyser.has_passed
        elif analyser.has_passed is not None:
            test_passed = test_passed and analyser.has_passed
        rx_packets = analyser.total_rx_packets
        tx_packets = analyser.total_tx_packets
        rx_bytes = analyser.total_rx_bytes
        tx_bytes = analyser.total_tx_bytes
        rx_vlan_bytes = analyser.total_rx_vlan_bytes
        tx_vlan_bytes = analyser.total_tx_vlan_bytes
        ts_tx_first = analyser.timestamp_tx_first
        ts_tx_last = analyser.timestamp_tx_last
        ts_rx_first = analyser.timestamp_rx_first
        ts_rx_last = analyser.timestamp_rx_last

        if _analyser_has_latency_summary(analyser):
            # Do return the latency-related values whether packets
            # have been received or not:
            # * No latency analysers
            #   => no entries
            # * Latency analysers but no packets received
            #   => entries with `None` value
            has_latency = True
            if rx_packets:
                logging.debug('Adding extra latency to sum')
                min_latency = analyser.final_min_latency
                max_latency = analyser.final_max_latency
                avg_latency = analyser.final_avg_latency
                avg_jitter = analyser.final_avg_jitter
                # Check if packets (with valid latency) received
                # by previous analysers (value not ``None``):
                if (final_min_latency is None
                        or min_latency < final_min_latency):
                    final_min_latency = min_latency
                # Check if packets (with valid latency) received
                # by previous analysers (value not ``None``):
                if (final_max_latency is None
                        or max_latency > final_max_latency):
                    final_max_latency = max_latency
                # Update weighted average latency and jitter:
                if final_avg_latency is None:
                    # No packets (with valid latency) received
                    # by previous analysers
                    final_avg_latency = avg_latency
                else:
                    final_avg_latency = (
                        (
                            final_avg_latency * total_rx_packets +
                            avg_latency * rx_packets
                        ) / (total_rx_packets + rx_packets)
                    )
                if final_avg_jitter is None:
                    # No packets (with valid latency) received
                    # by previous analysers
                    final_avg_jitter = avg_jitter
                else:
                    final_avg_jitter = (
                        (
                            final_avg_jitter * total_rx_packets +
                            avg_jitter * rx_packets
                        ) / (total_rx_packets + rx_packets)
                    )
            else:
                logging.warning(
                    'Ignoring latency for analyser on flow %r',
                    analyser.flow.name
                )

        total_rx_packets += rx_packets
        total_tx_packets += tx_packets
        total_rx_bytes += rx_bytes
        total_tx_bytes += tx_bytes
        total_rx_vlan_bytes += rx_vlan_bytes
        total_tx_vlan_bytes += tx_vlan_bytes
        if timestamp_tx_first is None or (ts_tx_first is not None and
                                          timestamp_tx_first < ts_tx_first):
            timestamp_tx_first = ts_tx_first
        if timestamp_tx_last is None or (ts_tx_last is not None
                                         and ts_tx_last > timestamp_tx_last):
            timestamp_tx_last = ts_tx_last
        if timestamp_rx_first is None or (ts_rx_first is not None and
                                          timestamp_rx_first < ts_rx_first):
            timestamp_rx_first = ts_rx_first
        if timestamp_rx_last is None or (ts_rx_last is not None
                                         and ts_rx_last > timestamp_rx_last):
            timestamp_rx_last = ts_rx_last

    total_tx_bytes = include_ethernet_overhead(
        layer2_speed, total_tx_bytes, total_tx_packets
    )
    total_rx_bytes = include_ethernet_overhead(
        layer2_speed, total_rx_bytes, total_rx_packets
    )

    if has_latency:
        # Do return the latency-related values whether packets
        # have been received or not:
        # * No latency analysers
        #   => no entries
        # * Latency analysers but no packets received
        #   => entries with `None` value
        latency_results = (
            final_min_latency,
            final_max_latency,
            final_avg_latency,
            final_avg_jitter,
        )
    else:
        latency_results = None

    return (
        test_passed,
        total_rx_packets,
        total_tx_packets,
        total_rx_bytes,
        total_tx_bytes,
        total_rx_vlan_bytes,
        total_tx_vlan_bytes,
        timestamp_tx_first,
        timestamp_tx_last,
        timestamp_rx_first,
        timestamp_rx_last,
        latency_results,
    )


def _analyser_frame_count_over_time(
    analyser: _SummarySupportedAnalysers
) -> bool:
    return isinstance(analyser, _OverTimeSupportedAnalysersList)


def _analyser_has_latency_summary(
    analyser: _SummarySupportedAnalysers
) -> bool:
    return isinstance(analyser, _SummaryLatencyAnalysers)


def _to_camel_case(key: str) -> str:
    """Convert to ``camelCase``, from dash- and/or space-separated string.

    :param key: Key to convert
    :type key: str
    :return: Key in camelCase format.
    :rtype: str
    """
    keys = key.split(' ')
    keys = [k.split('_') for k in keys]
    keys = [k.title() for kk in keys for k in kk]
    keys[0] = keys[0].lower()
    return ''.join(keys)
