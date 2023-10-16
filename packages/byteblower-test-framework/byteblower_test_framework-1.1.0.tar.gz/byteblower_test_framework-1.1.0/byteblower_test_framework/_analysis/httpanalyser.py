import logging
from typing import Optional  # for type hinting

from pandas import Timestamp  # for type hinting

from .._traffic.tcpflow import TcpFlow  # for type hinting
from .data_analysis.tcp import HttpDataAnalyser
from .data_gathering.tcp import HttpDataGatherer
from .flow_analyser import AnalysisDetails, FlowAnalyser
from .render.tcp import HttpRenderer
from .storage.tcp import HttpData


class HttpAnalyser(FlowAnalyser):
    """Analyse HTTP and TCP statistics over time.

    The analyser currently only provides the HTTP goodput over time
    and the average HTTP goodput over the duration of the test.

    .. note::
       There is no specific analysis performed and the test
       will always state no analysis is done.

    This analyser is intended for use with a :class:`~.traffic.HTTPFlow`.

    Supports:

    * Analysis of a single flow

    .. warning::
        Does not support aggregation data from multiple flows
        (via :class:`~.analysis.AnalyserAggregator`).
    """

    __slots__ = (
        '_http_data',
        '_data_gatherer',
        '_data_analyser',
        '_renderer',
    )

    def __init__(self):
        """Create the HTTP and TCP statistics over time analyser."""
        super().__init__("HTTP analyser")
        self._http_data = HttpData()
        self._data_gatherer = None
        self._data_analyser = None
        self._renderer = None

    @property
    def flow(self) -> TcpFlow:
        """Return Flow implementation.

        Useful for correct type hinting.
        """
        return self._flow

    def _initialize(self) -> None:
        self._data_gatherer = HttpDataGatherer(
            self._http_data, self.flow._bb_tcp_clients
        )
        self._data_analyser = HttpDataAnalyser(self._http_data)
        self._renderer = HttpRenderer(self._data_analyser)

    def apply(self) -> None:
        super().apply()
        if self.flow._bb_tcp_server is None:
            logging.warning(
                'Flow %r: No TCP server available.'
                ' No data gathering done for TCP server.',
                self.flow.name,
            )
        self._data_gatherer.set_http_server(self.flow._bb_tcp_server)
        self._data_gatherer.prepare()
        self._data_analyser.prepare()

    def process(self) -> None:
        self._data_gatherer.process()

    def updatestats(self) -> None:
        """Analyse the result.

        What would be bad?

        * TCP sessions not going to Finished
        """
        # Let's analyse the result
        self._data_gatherer.updatestats()

    def analyse(self) -> None:
        # Currently, no pass/fail criteria.
        self._data_gatherer.summarize()
        self._data_analyser.analyse()
        self._set_result(self._data_analyser.has_passed)
        self._add_failure_causes(self._data_analyser.failure_causes)

    def release(self) -> None:
        super().release()
        self._data_gatherer.release()

    @property
    def log(self) -> str:
        """Return the summary log text.

        .. note::
           Used for unit test report.

        :return: Summary log text.
        :rtype: str
        """
        return self._data_analyser.log

    def render(self) -> str:
        return self._renderer.render()

    def details(self) -> Optional[AnalysisDetails]:
        return self._renderer.details()

    @property
    def http_method(self):
        """Return the configured HTTP Request Method."""
        return self._data_analyser.http_method

    @property
    def total_rx_client(self) -> int:
        """Number of received bytes at HTTP Client."""
        return self._data_analyser.total_rx_client

    @property
    def total_tx_client(self) -> int:
        """Number of transmitted bytes at HTTP Client."""
        return self._data_analyser.total_tx_client

    @property
    def total_rx_server(self) -> int:
        """Number of received bytes at HTTP Server."""
        return self._data_analyser.total_rx_server

    @property
    def total_tx_server(self) -> int:
        """Number of transmitted bytes at HTTP Server."""
        return self._data_analyser.total_tx_server

    @property
    def rx_first_client(self) -> Optional[Timestamp]:
        """Time when the first packet was received at the HTTP Client."""
        return self._data_analyser.rx_first_client

    @property
    def rx_last_client(self) -> Optional[Timestamp]:
        """Time when the last packet was received at the HTTP Client."""
        return self._data_analyser.rx_last_client

    @property
    def tx_first_client(self) -> Optional[Timestamp]:
        """Time when the first packet was transmitted at the HTTP Client."""
        return self._data_analyser.tx_first_client

    @property
    def tx_last_client(self) -> Optional[Timestamp]:
        """Time when the last packet was transmitted at the HTTP Client."""
        return self._data_analyser.tx_last_client

    @property
    def rx_first_server(self) -> Optional[Timestamp]:
        """Time when the first packet was received at the HTTP Server."""
        return self._data_analyser.rx_first_server

    @property
    def rx_last_server(self) -> Optional[Timestamp]:
        """Time when the last packet was received at the HTTP Server."""
        return self._data_analyser.rx_last_server

    @property
    def tx_first_server(self) -> Optional[Timestamp]:
        """Time when the first packet was transmitted at the HTTP Server."""
        return self._data_analyser.tx_first_server

    @property
    def tx_last_server(self) -> Optional[Timestamp]:
        """Time when the last packet was transmitted at the HTTP Server."""
        return self._data_analyser.tx_last_server
