"""Aggregation for latency results."""
import logging
from typing import List  # for type hinting

from .._analysis.flow_analyser import FlowAnalyser  # for type hinting
from .latencyanalyser import BaseLatencyCDFFrameLossAnalyser
from .plotting.generic_chart import GenericChart

_LOGGER = logging.getLogger(__name__)


class HtmlLatencyAggregator(object):
    """
    Aggregator for latency-related :class:`FlowAnalyser`.

    The results will be rendering for HTML output.
    """
    __slots__ = ('_analysers', )

    container_id = 0

    def __init__(self) -> None:
        """Create the aggregator for latency-related FlowAnalysers."""
        self._analysers: List[BaseLatencyCDFFrameLossAnalyser] = []

    def add_analyser(self, analyser: FlowAnalyser) -> None:
        """
        Add a FlowAnalyser.

        .. note::
           Only FlowAnalysers supporting latency (*CDF-only for now*)
           will be added.
        """
        if isinstance(analyser, BaseLatencyCDFFrameLossAnalyser):
            self._analysers.append(analyser)

    def can_render(self) -> bool:
        """Return whether there is anything to render."""
        return len(self._analysers) > 0

    def render(self) -> str:
        """Render the aggregated results of the added FlowAnalysers.

        A :class:`FlowAnalyser` can be added using :meth:`add_analyser`

        :return: HTML content with rendered aggregated results.
        :rtype: str
        """
        result = '<h3>Aggregated latency results</h3>\n'

        # CCDF
        chart = GenericChart(
            "Latency CCDF",
            x_axis_title="Latency [ms]",
            chart_options={"zoomType": "x"},
            x_axis_options={"labels": {
                "format": "{value} ms"
            }},
        )

        series_titles = set()
        for analyser in self._analysers:
            series_title = (
                f'{analyser.flow.name}<br/> {analyser.flow.source.name}'
                f' \u2794 {analyser.flow.destination.name}'
            )
            if series_title in series_titles:
                _LOGGER.warning(
                    'Duplicate latency test results: %r \u2794  Skipping!',
                    series_title,
                )
                continue
            series_titles.add(series_title)

            # Get the data
            total_rx_packets = analyser.total_rx_packets

            if not total_rx_packets:
                continue

            df_latency = analyser._latency_cdf_analyser.df_latency.copy()

            # Build the graphs
            # [ns] -> [ms]
            df_latency["latency"] /= 1000 * 1000.0
            # Set the latency column as index
            df_latency = df_latency.set_index("latency")
            # Complement of the percentile
            df_latency["percentile"] = 100.0 - df_latency["percentile"]

            chart.add_series(
                list(df_latency.itertuples(index=True)),
                "line",
                series_title,
                "",
                "",
                y_axis_options={
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
            'latency_aggregator_container'
            f'{HtmlLatencyAggregator.container_id}'
        )
        HtmlLatencyAggregator.container_id += 1

        return result
