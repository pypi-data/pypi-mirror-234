from typing import Optional  # for type hinting

from ..data_analysis.tcp import HttpDataAnalyser
from ..helpers import to_bitrate
from ..plotting import GenericChart
from .renderer import AnalysisDetails, Renderer


class HttpRenderer(Renderer):

    __slots__ = ('_data_analyser', )

    def __init__(self, data_analyser: HttpDataAnalyser) -> None:
        super().__init__()
        self._data_analyser = data_analyser

    def render(self) -> str:
        analysis_log = self._data_analyser.log

        # Get the data
        # df_tx = self._data_analyser.df_tx
        # df_rx = self._data_analyser.df_rx
        df_dataspeed = self._data_analyser.df_dataspeed

        if df_dataspeed is not None:
            df_dataspeed_bits = to_bitrate((df_dataspeed, 'AVG dataspeed'))
        else:
            df_dataspeed_bits = None

        # Set the summary
        result = self._verbatim(analysis_log)

        # Build the graph
        chart = GenericChart(
            "HTTP statistics",
            x_axis_options={"type": "datetime"},
            chart_options={"zoomType": "x"}
        )
        # chart.add_series(list(df_tx.itertuples(index=True)), "line", "TX",
        #                  "Data count", "bytes")
        # chart.add_series(list(df_rx.itertuples(index=True)), "line", "RX",
        #                  "Data count", "bytes")
        chart.add_series(
            list(df_dataspeed_bits.itertuples(index=True)),
            "line",
            "AVG dataspeed",
            "Dataspeed",
            "bits/s",
        )
        result += chart.plot(f'http_container{HttpRenderer.container_id}')
        HttpRenderer.container_id += 1

        return result

    def details(self) -> Optional[AnalysisDetails]:

        # Get the data
        df_http_client = self._data_analyser.df_http_client
        df_http_server = self._data_analyser.df_http_server
        total_rx_client = self._data_analyser.total_rx_client
        total_tx_client = self._data_analyser.total_tx_client
        total_rx_server = self._data_analyser.total_rx_server
        total_tx_server = self._data_analyser.total_tx_server
        ts_rx_first_client = self._data_analyser.rx_first_client
        ts_rx_last_client = self._data_analyser.rx_last_client
        ts_tx_first_client = self._data_analyser.tx_first_client
        ts_tx_last_client = self._data_analyser.tx_last_client
        ts_rx_first_server = self._data_analyser.rx_first_server
        ts_rx_last_server = self._data_analyser.rx_last_server
        ts_tx_first_server = self._data_analyser.tx_first_server
        ts_tx_last_server = self._data_analyser.tx_last_server
        http_method = self._data_analyser.http_method

        df_overtimeresults_client = df_http_client[[
            'duration', 'TX Bytes', 'RX Bytes'
        ]]

        df_overtimeresults_client = df_overtimeresults_client.rename(
            columns={
                'TX Bytes': 'txBytes',
                'RX Bytes': 'rxBytes',
            }
        )

        df_overtimeresults_server = df_http_server[[
            'duration', 'TX Bytes', 'RX Bytes'
        ]]

        df_overtimeresults_server = df_overtimeresults_server.rename(
            columns={
                'TX Bytes': 'txBytes',
                'RX Bytes': 'rxBytes',
            }
        )

        details: AnalysisDetails = {
            'method': http_method,
            'httpClient': {
                'rxBytes': total_rx_client,
                'txBytes': total_tx_client,
                'rxFirst': ts_rx_first_client,
                'rxLast': ts_rx_last_client,
                'txFirst': ts_tx_first_client,
                'txLast': ts_tx_last_client,
                'overTimeResult': df_overtimeresults_client
            },
            'httpServer': {
                'rxBytes': total_rx_server,
                'txBytes': total_tx_server,
                'rxFirst': ts_rx_first_server,
                'rxLast': ts_rx_last_server,
                'txFirst': ts_tx_first_server,
                'txLast': ts_tx_last_server,
                'overTimeResult': df_overtimeresults_server
            }
        }

        return details
