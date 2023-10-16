"""Factory functions to create and initialize :class:`~Port` instances."""
import logging
from typing import Any, Dict  # for type hinting

from byteblower_test_framework.endpoint import Port  # for type hinting
from byteblower_test_framework.endpoint import IPv4Port, IPv6Port, NattedPort
from byteblower_test_framework.exceptions import InvalidInput
from byteblower_test_framework.host import Server  # for type hinting

from ._definitions import LOGGING_PREFIX as _LOGGING_PREFIX

__all__ = ('initialize_port', )

# Type aliases
PortConfig = Dict[str, Any]


class PortFactory(object):  # pylint: disable=too-few-public-methods
    """Factory for :class:`Port` objects."""

    PORT_COUNT = 0

    @staticmethod
    def build_port(
        server: Server, _autonumber: bool = True, **port_config
    ) -> Port:
        """Create a :class:`Port`.

        The function can create either :class:`IPv4Port`,  :class:`NattedPort`
        or :class:`IPv6Port` objects.

        :param server: The :class:`Server` object to create the port on
        :type server: Server
        :param port_config: The configuration for the port.
        :type port_config: PortConfig
        :param _autonumber: When the *name* of the port is not given in the
           configuration of the port, use autonumbered name for the port,
           defaults to True
        :type _autonumber: bool, optional
        :return: The newly created port
        :rtype: Port
        """
        if 'ipv4' in port_config:
            nat = port_config.pop('nat', False)
            if nat:
                port_class = NattedPort
            else:
                port_class = IPv4Port
        elif 'ipv6' in port_config:
            port_class = IPv6Port
        else:
            raise InvalidInput(
                'Please provide either IPv4 or IPv6 configuration'
            )
        name = port_config.pop('name', None)
        if name is None:
            if _autonumber:
                name = f'PORT {PortFactory.PORT_COUNT + 1}'
            else:
                name = 'PORT'
        port = port_class(server, name=name, **port_config)
        PortFactory.PORT_COUNT += 1
        return port


def initialize_port(
    server: Server, port_config: PortConfig, _autonumber: bool = True
) -> Port:
    """Create a :class:`Port`.

    The function can create either :class:`IPv4Port`,  :class:`NattedPort`
    or :class:`IPv6Port` objects.

    :param server: The :class:`Server` object to create the port on
    :type server: Server
    :param port_config: The configuration for the port.
    :type port_config: PortConfig
    :param _autonumber: When the *name* of the port is not given in the
       configuration of the port, use autonumbered name for the port,
       defaults to True
    :type _autonumber: bool, optional
    :return: The newly created port
    :rtype: Port
    """
    logging.info('%sInitializing port', _LOGGING_PREFIX)
    port: Port = PortFactory.build_port(
        server, _autonumber=_autonumber, **port_config
    )
    logging.info(
        '%sInitialized port %r'
        ' with IP address %r, network %r', _LOGGING_PREFIX, port.name, port.ip,
        port.network
    )

    return port
