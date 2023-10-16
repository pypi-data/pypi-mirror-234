from datetime import timedelta
from typing import Iterable, Optional, Union  # for type hinting

from .._endpoint.port import Port  # for type hinting
from .._helpers.syncexec import SynchronizedExecutable
from ..exceptions import NotDurationBased
from .helpers import get_ip_traffic_class
from .tcpflow import HttpMethod, TcpFlow


class HTTPFlow(TcpFlow):

    __slots__ = (
        '_tcp_server_port',
        '_tcp_client_port',
        '_request_duration',
        '_request_size',
        '_initial_time_to_wait',
        '_rate_limit',
        '_receive_window_scaling',
        '_slow_start_threshold',
        '_ip_traffic_class',
    )

    _CONFIG_ELEMENTS = TcpFlow._CONFIG_ELEMENTS + (
        'tcp_server_port',
        'rate_limit',
        'receive_window_scaling',
        'slow_start_threshold',
    )

    def __init__(
        self,
        source: Port,
        destination: Port,
        name: Optional[str] = None,
        http_method: HttpMethod = HttpMethod.AUTO,
        tcp_server_port: Optional[int] = None,
        tcp_client_port: Optional[int] = None,
        request_duration: Optional[Union[timedelta, float, int]] = None,
        request_size: Optional[int] = None,
        initial_time_to_wait: Optional[Union[timedelta, float,
                                             int]] = None,  # [seconds]
        rate_limit: Optional[int] = None,
        receive_window_scaling: Optional[int] = None,
        slow_start_threshold: Optional[int] = None,
        ip_dscp: Optional[int] = None,
        ip_ecn: Optional[int] = None,
        ip_traffic_class: Optional[int] = None,
        **kwargs
    ) -> None:
        super().__init__(
            source, destination, name=name, http_method=http_method, **kwargs
        )
        self._tcp_server_port = tcp_server_port
        self._tcp_client_port = tcp_client_port
        self._request_size = request_size

        if isinstance(request_duration, (float, int)):
            # Convert to timedelta
            self._request_duration = timedelta(seconds=request_duration)
        else:
            # Either already timedelta or None:
            self._request_duration = request_duration
        if isinstance(initial_time_to_wait, (float, int)):
            # Convert to timedelta
            self._initial_time_to_wait = timedelta(
                seconds=initial_time_to_wait
            )
        else:
            # Either already timedelta or None:
            # Default to 0s
            self._initial_time_to_wait = initial_time_to_wait or timedelta()
        self._rate_limit = rate_limit
        self._receive_window_scaling = receive_window_scaling
        self._slow_start_threshold = slow_start_threshold
        self._ip_traffic_class = get_ip_traffic_class(
            "IP Traffic Class",
            ip_traffic_class=ip_traffic_class,
            ip_ecn=ip_ecn,
            ip_dscp=ip_dscp,
        )

        # Sanity check
        if self._request_duration is not None and self._request_size is not None:
            raise ValueError(
                f'Flow {self._name!r}: Please provide'
                ' either request duration or request size but not both.'
            )

    @property
    def tcp_server_port(self) -> Optional[int]:
        """TCP port of the HTTP server."""
        return self._tcp_server_port

    @property
    def rate_limit(self) -> Optional[int]:
        """Return the requested HTTP rate limit.

        :return: The rate limit, in bytes per second.
        :rtype: Optional[int]
        """
        return self._rate_limit

    @property
    def receive_window_scaling(self) -> Optional[int]:
        """TCP Receive Window scaling."""
        return self._receive_window_scaling

    @property
    def slow_start_threshold(self) -> Optional[int]:
        """TCP Slow Start Threshold."""
        return self._slow_start_threshold

    @property
    def duration(self) -> timedelta:
        """Returns the duration of the HTTP flow.

        :raises NotDurationBased: If the HTTPFlow is sized based.
        :returns: duration of the flow.
        :rtype: timedelta
        """
        if self._request_duration is not None:
            return self._request_duration
        raise NotDurationBased()

    @property
    def initial_time_to_wait(self) -> timedelta:
        """Return the time to wait before the flow starts."""
        return self._initial_time_to_wait

    def apply(
        self,
        maximum_run_time: Optional[Union[timedelta, float, int]] = None,
        **kwargs
    ) -> Iterable[SynchronizedExecutable]:
        """Open a session, send the file and close the connection."""
        if self._request_duration is None and self._request_size is None:
            if isinstance(maximum_run_time, (float, int)):
                # Convert to timedelta
                # duration = maximum_run_time - self._initial_time_to_wait
                # self._request_duration = timedelta(seconds=duration)
                self._request_duration = (
                    timedelta(seconds=maximum_run_time) -
                    self._initial_time_to_wait
                )
            elif maximum_run_time is not None:
                # Must be a timedelta:
                self._request_duration = (
                    maximum_run_time - self._initial_time_to_wait
                )
            else:
                self._request_duration = maximum_run_time
        # Create a TCP server on the destination.
        http_server = self._set_tcp_server(
            tcp_port=self._tcp_server_port,
            receive_window_scaling=self._receive_window_scaling,
            slow_start_threshold=self._slow_start_threshold
        )

        # NOTE: Persisting value, so they are available after self.release() !
        self._tcp_server_port = self._bb_tcp_server.PortGet()
        if self._bb_tcp_server.ReceiveWindowScalingIsEnabled():
            self._receive_window_scaling = (
                self._bb_tcp_server.ReceiveWindowScalingValueGet()
            )
        else:
            self._receive_window_scaling = None
        self._slow_start_threshold = (
            self._bb_tcp_server.SlowStartThresholdGet()
        )

        if http_server is not None:
            # New HTTP server (not re-using existing one)
            # NOTE: Does not support scheduled start!
            http_server.Start()

        # Create the first client session so we will get started
        http_client = self._add_client_session(
            request_duration=self._request_duration,
            request_size=self._request_size,
            rate_limit=self._rate_limit,
            ittw=self._initial_time_to_wait,
            receive_window_scaling=self._receive_window_scaling,
            slow_start_threshold=self._slow_start_threshold,
            tcp_port=self._tcp_client_port,
            ip_traffic_class=self._ip_traffic_class,
        )
        yield from super().apply(**kwargs)
        yield SynchronizedExecutable(http_client)

    def release(self) -> None:
        super().release()
        super()._release()
