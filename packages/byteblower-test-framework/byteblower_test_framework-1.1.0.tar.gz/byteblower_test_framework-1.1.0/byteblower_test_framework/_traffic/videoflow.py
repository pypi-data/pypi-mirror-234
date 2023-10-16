import logging
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Iterable, Optional, Union  # for type hinting

from byteblowerll.byteblower import DomainError

from .._analysis.bufferanalyser import BufferAnalyser
from .._endpoint.port import Port  # for type hinting
from ..exceptions import ByteBlowerTestFrameworkException, InfiniteDuration
from .helpers import get_ip_traffic_class
from .tcpflow import TCPCongestionAvoidanceAlgorithm, TcpFlow

if TYPE_CHECKING:
    # NOTE: Used for type hinting only
    from .._helpers.syncexec import SynchronizedExecutable


class VideoFlow(TcpFlow):

    __slots__ = (
        '_segment_size',
        '_segment_duration',
        '_buffering_goal',
        '_bytes_per_ms',
        '_bufferanalyser',
        '_last_consume_time',
        '_ip_traffic_class',
    )

    _CONFIG_ELEMENTS = TcpFlow._CONFIG_ELEMENTS + (
        "segment_size",
        "segment_duration",
        "buffering_goal",
    )

    def __init__(
        self,
        source: Port,
        destination: Port,
        name: Optional[str] = None,
        segment_size: int = 2 * 1000 * 1000,
        segment_duration: Union[timedelta, float] = timedelta(seconds=2.500),
        buffering_goal: Union[timedelta, float] = timedelta(seconds=60),
        play_goal: Union[timedelta, float] = timedelta(seconds=5),
        ip_dscp: Optional[int] = None,
        ip_ecn: Optional[int] = None,
        ip_traffic_class: Optional[int] = None,
        # *args,
        **kwargs
    ) -> None:
        super().__init__(source, destination, name=name, **kwargs)
        # super().__init__(source, destination, *args, name=name, **kwargs)
        self._segment_size = segment_size
        if isinstance(segment_duration, timedelta):
            # Already timedelta
            self._segment_duration = segment_duration
        elif isinstance(segment_duration, (float, int)):
            # Convert to timedelta
            self._segment_duration = timedelta(seconds=segment_duration)
        else:
            raise ValueError(
                f'Invalid value for segment_duration: {segment_duration!r}'
            )
        if isinstance(buffering_goal, timedelta):
            # Already timedelta
            self._buffering_goal = buffering_goal
        elif isinstance(buffering_goal, (float, int)):
            # Convert to timedelta
            self._buffering_goal = timedelta(seconds=buffering_goal)
        else:
            raise ValueError(
                f'Invalid value for buffering_goal: {buffering_goal!r}'
            )
        if isinstance(play_goal, timedelta):
            # Already timedelta
            pass
        elif isinstance(play_goal, (float, int)):
            # Convert to timedelta
            play_goal = timedelta(seconds=play_goal)
        else:
            raise ValueError(
                f'Invalid value for buffering_goal: {play_goal!r}'
            )
        self._ip_traffic_class = get_ip_traffic_class(
            "IP Traffic Class",
            ip_traffic_class=ip_traffic_class,
            ip_dscp=ip_dscp,
            ip_ecn=ip_ecn,
        )
        self._bytes_per_ms = (
            self._segment_size / self._segment_duration.total_seconds() / 1000
        )  # video bitrate expressed in bytes/s
        bitrate = 8000 * self._bytes_per_ms
        logging.info(
            "Video bitrate will be {BITRATE} MBit/s".format(
                BITRATE=bitrate / 1000000.0
            )
        )
        buffering_goal_segments = (
            self._buffering_goal.total_seconds() /
            self._segment_duration.total_seconds()
        )

        buffering_goal_bytes = \
            int(buffering_goal_segments * self._segment_size)
        play_goal_bytes = int(
            play_goal.total_seconds() / self._segment_duration.total_seconds()
        ) * self._segment_size
        self._bufferanalyser = BufferAnalyser(
            buffering_goal_bytes, play_goal_bytes
        )
        self.add_analyser(self._bufferanalyser)
        self._last_consume_time: datetime = None

    @property
    def segment_size(self) -> int:
        return self._segment_size

    @property
    def segment_duration(self) -> timedelta:
        return self._segment_duration

    @property
    def buffering_goal(self) -> timedelta:
        return self._buffering_goal

    @property
    def initial_time_to_wait(self) -> timedelta:
        """Return the time to wait before the flow starts."""
        return timedelta()

    @property
    def duration(self) -> timedelta:
        """Returns the duration of the Video flow.

        :raises InfiniteDuration: The video flow always runs forever.
        :returns: duration of the flow.
        :rtype: timedelta
        """
        raise InfiniteDuration()

    def apply(self, **kwargs) -> Iterable['SynchronizedExecutable']:
        bb_tcp_server = self._set_tcp_server(
            server_port=self.source,
            receive_window_scaling=7,
            slow_start_threshold=1000000000,
            caa=TCPCongestionAvoidanceAlgorithm.sack_with_cubic
        )
        if bb_tcp_server is not None:
            # New HTTP server (not re-using existing one)
            # NOTE: Does not support scheduled start!
            bb_tcp_server.Start()
        self._last_consume_time = datetime.now()
        # Set the initial stats:
        self._bufferanalyser.updatestats()
        # ! FIXME - Is this required/wanted?
        yield from super().apply(**kwargs)

    def _elapsed_time_ms(self) -> float:
        now = datetime.now()
        difference: timedelta = now - self._last_consume_time
        self._last_consume_time = now
        return difference.total_seconds() * 1000

    def _download_segment(self) -> None:
        bb_tcp_client = self._add_client_session(
            client_port=self.destination,
            server_port=self.source,
            request_size=self._segment_size,
            receive_window_scaling=7,
            slow_start_threshold=1000000000,
            caa=TCPCongestionAvoidanceAlgorithm.sack_with_cubic,
            ip_traffic_class=self._ip_traffic_class,
        )
        bb_tcp_client.RequestStart()

    def _segment_download_required(self) -> bool:
        return (
            self._bufferanalyser.size + self._segment_size <
            self._bufferanalyser.size_max
        )

    def process(self) -> None:
        try:
            bb_tcp_client = self._last_client_session()
        except ByteBlowerTestFrameworkException:
            if self._segment_download_required():
                self._download_segment()
        else:
            # Wait maximum 10 milliseconds
            try:
                if bb_tcp_client.WaitUntilFinished(10000000):
                    # Destroy the http client
                    test_tcp_client = self._bb_tcp_clients.pop()
                    assert test_tcp_client == bb_tcp_client, \
                        'OOPS, clearing invalid TCP client'
                    self.destination.bb_port.ProtocolHttpClientRemove(
                        bb_tcp_client
                    )
                    self._bufferanalyser.buffer_fill(self._segment_size)

            except DomainError as e:
                logging.error(
                    "No video statistics available. Unexpected error: %s",
                    e.getMessage(),
                )
            except Exception as e:
                logging.error(
                    "No video statistics available. Unexpected error: %s", e
                )

        elapsed_bytes = self._elapsed_time_ms() * self._bytes_per_ms
        self._bufferanalyser.buffer_consume(elapsed_bytes)

        super().process()

    def updatestats(self) -> None:
        return super().updatestats()

    def analyse(self) -> None:
        """Pass or fail for this test."""
        self.updatestats()

        return super().analyse()

    def release(self) -> None:
        super().release()
        super()._release(client_port=self.destination, server_port=self.source)
