from typing import Optional  # for type hinting

from pandas import DataFrame, Timestamp  # for type hinting

from ..helpers import MEGA, to_bitrate
from ..storage.tcp import HttpData
from .data_analyser import DataAnalyser


class HttpDataAnalyser(DataAnalyser):

    __slots__ = (
        '_http_data',
        '_df_dataspeed',
    )

    def __init__(self, http_data: HttpData) -> None:
        super().__init__()
        self._http_data = http_data
        self._df_dataspeed: DataFrame = None

    def analyse(self) -> None:
        """
        .. note::
           Currently, no pass/fail criteria.
        """
        # Get the data
        df_tcp = self._http_data.df_tcp_client
        self._df_dataspeed = df_tcp[['AVG dataspeed']]
        avg_data_speed = self._http_data.avg_data_speed

        if avg_data_speed is not None:
            avg_data_speed = to_bitrate(avg_data_speed, scaling_factor=MEGA)

        self._set_log(
            f'Average data speed: {(avg_data_speed or 0):0.3f} Mbits/s'
        )
        # Actually nothing is analysed here
        # self._set_result(True)

    @property
    def http_method(self):
        """Return the configured HTTP Request Method."""
        return self._http_data.http_method

    @property
    def df_http_client(self) -> DataFrame:
        return self._http_data.df_tcp_client

    @property
    def df_http_server(self) -> DataFrame:
        return self._http_data.df_tcp_server

    @property
    def df_dataspeed(self) -> DataFrame:
        return self._df_dataspeed

    @property
    def total_rx_client(self) -> int:
        """Number of received bytes at HTTP Client."""
        return self._http_data.total_rx_client

    @property
    def total_tx_client(self) -> int:
        """Number of transmitted bytes at HTTP Client."""
        return self._http_data.total_tx_client

    @property
    def total_rx_server(self) -> int:
        """Number of received bytes at HTTP Server."""
        return self._http_data.total_rx_server

    @property
    def total_tx_server(self) -> int:
        """Number of transmitted bytes at HTTP Server."""
        return self._http_data.total_tx_server

    @property
    def rx_first_client(self) -> Optional[Timestamp]:
        """Time when the first packet was received at the HTTP Client."""
        return self._http_data.ts_rx_first_client

    @property
    def rx_last_client(self) -> Optional[Timestamp]:
        """Time when the last packet was received at the HTTP Client."""
        return self._http_data.ts_rx_last_client

    @property
    def tx_first_client(self) -> Optional[Timestamp]:
        """Time when the first packet was transmitted at the HTTP Client."""
        return self._http_data.ts_tx_first_client

    @property
    def tx_last_client(self) -> Optional[Timestamp]:
        """Time when the last packet was transmitted at the HTTP Client."""
        return self._http_data.ts_tx_last_client

    @property
    def rx_first_server(self) -> Optional[Timestamp]:
        """Time when the first packet was received at the HTTP Server."""
        return self._http_data.ts_rx_first_server

    @property
    def rx_last_server(self) -> Optional[Timestamp]:
        """Time when the last packet was received at the HTTP Server."""
        return self._http_data.ts_rx_last_server

    @property
    def tx_first_server(self) -> Optional[Timestamp]:
        """Time when the first packet was transmitted at the HTTP Server."""
        return self._http_data.ts_tx_first_server

    @property
    def tx_last_server(self) -> Optional[Timestamp]:
        """Time when the last packet was transmitted at the HTTP Server."""
        return self._http_data.ts_tx_last_server
