"""ByteBlower Server interface module."""
import logging
from typing import TYPE_CHECKING  # for type hinting

from byteblowerll.byteblower import ByteBlowerPort  # for type hinting
from byteblowerll.byteblower import ByteBlowerServer  # for type hinting
from byteblowerll.byteblower import ByteBlower, ConfigError

if TYPE_CHECKING:
    # NOTE: Used in documentation only
    from .._endpoint.port import Port
    from .._scenario import Scenario
    from .._traffic.flow import Flow


class Server(object):
    """ByteBlower Server interface."""

    __slots__ = (
        '_host_ip',
        '_bb_server',
    )

    def __init__(self, ip_or_host: str) -> None:
        """
        Connect to the ByteBlower server.

        :param ip_or_host: The connection address. This can be
           the hostname or IPv4/IPv6 address of the ByteBlower server.
        """
        self._host_ip = ip_or_host
        bb_root: ByteBlower = ByteBlower.InstanceGet()
        self._bb_server: ByteBlowerServer = bb_root.ServerAdd(self._host_ip)

    @property
    def info(self) -> str:
        """Return connection address this server."""
        return self._host_ip

    def start(self) -> None:
        """
        Start all ByteBlower Ports configured on this server.

        .. warning::
           This call will start *all* traffic generation/analysis on *all*
           ByteBlowerPorts created for this Server.

           This might not be intended when you run multiple test scenarios
           in parallel.
        """
        logging.debug('Starting all ByteBlowerPorts')
        port: ByteBlowerPort
        for port in self._bb_server.PortGet():
            try:
                port.Start()
            except ConfigError as error:
                logging.error(
                    'Failed to start Port %r @ %s: %s',
                    port,
                    port.InterfaceNameGet(),
                    error.getMessage(),
                )
                continue

    def stop(self) -> None:
        """
        Stop all ByteBlower Ports configured on this server.

        .. warning::
           This call will stop *all* traffic generation/analysis on *all*
           ByteBlowerPorts created for this Server.

           This might not be intended when you run multiple test scenarios
           in parallel.
        """
        logging.debug('Stopping all ByteBlowerPorts')
        port: ByteBlowerPort
        for port in self._bb_server.PortGet():
            port.Stop()

    @property
    def bb_server(self) -> ByteBlowerServer:
        """Server object from the ByteBlower API."""
        return self._bb_server

    def release(self) -> None:
        """
        Release this host related resources used on the ByteBlower system.

        .. warning::
           Releasing resources related to traffic generation and analysis
           should be done *first* via the :meth:`Scenario.release()`
           and/or :meth:`Flow.release()`.

        .. warning::
           Releasing endpoint resources should be done *first*
           via :meth:`Port.release()`.
        """
        bb_root: ByteBlower = ByteBlower.InstanceGet()
        bb_root.ServerRemove(self._bb_server)
        del self._bb_server
