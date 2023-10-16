"""Module for simplified Frame creation."""
from typing import TYPE_CHECKING, Any, Mapping, Optional  # for type hinting

from .._endpoint.ipv4.port import IPv4Port
from .._endpoint.ipv6.port import IPv6Port
from .._endpoint.port import Port  # for type hinting
from .._traffic.frame import Frame  # for type hinting
from .._traffic.ipv4.frame import IPv4Frame
from .._traffic.ipv6.frame import IPv6Frame
from ..exceptions import InvalidInput

if TYPE_CHECKING:
    # NOTE: Import because referenced in docstrings:
    from .._traffic.constants import DEFAULT_IP_DSCP, DEFAULT_IP_ECN
    from .._traffic.frame import DEFAULT_FRAME_LENGTH, UDP_DYNAMIC_PORT_START
    from ..exceptions import ConflictingInput

FrameConfig = Mapping[str, Any]


def create_frame(
    source_port: Port,
    length: Optional[int] = None,
    udp_src: Optional[int] = None,
    udp_dest: Optional[int] = None,
    ip_ecn: Optional[int] = None,
    ip_dscp: Optional[int] = None,
    ip_traffic_class: Optional[int] = None,
    latency_tag: bool = False
) -> Frame:
    """Create a frame based on the (source) Port type.

    :param source_port: Port which will be transmitting the Frame.
       Used to identify which Frame implementation we need
       (:class:`~traffic.IPv4Frame` or :class:`~traffic.IPv6Frame`)
    :type source_port: Port
    :param length: Frame length. This is the layer 2 (Ethernet) frame length
       *excluding* Ethernet FCS and *excluding* VLAN tags,
       defaults to :const:`DEFAULT_FRAME_LENGTH`
    :type length: Optional[int], optional
    :param udp_src: UDP source port, defaults to
       :const:`UDP_DYNAMIC_PORT_START`
    :type udp_src: Optional[int], optional
    :param udp_dest: UDP destination port, defaults to
       :const:`UDP_DYNAMIC_PORT_START`
    :type udp_dest: Optional[int], optional
    :param ip_dscp: IP Differentiated Services Code Point (DSCP),
        mutual exclusive with ``ip_traffic_class``,
        defaults to :const:`DEFAULT_IP_DSCP`
    :type ip_dscp: Optional[int], optional
    :param ip_ecn: IP Explicit Congestion Notification (ECN),
        mutual exclusive with ``ip_traffic_class``,
        defaults to :const:`DEFAULT_IP_ECN`
    :type ip_ecn: Optional[int], optional
    :param ip_traffic_class: The IP traffic class value is used to
       specify the exact value of either the *IPv4 ToS field* or the
       *IPv6 Traffic Class field*,
       mutual exclusive with ``ip_dscp`` and ``ip_ecn``,
       defaults to field value composed from ``ip_dscp`` and ``ip_ecn``.
    :type ip_traffic_class: Optional[int], optional
    :param latency_tag: Enable latency tag generation in the Frame,
       defaults to ``False``
    :type latency_tag: bool, optional
    :raises InvalidInput: When an unknown Port implementation is given.
    :raises InvalidInput: When invalid configuration values are given.
    :raises ConflictingInput: When invalid combination of configuration
        parameters is given
    :return: New instance of an IPv4 or IPv6 Frame interface
    :rtype: Frame
    """
    if isinstance(source_port, IPv4Port):
        ipv4_tos = ip_traffic_class

        return IPv4Frame(
            length=length,
            udp_src=udp_src,
            udp_dest=udp_dest,
            ip_dscp=ip_dscp,
            ip_ecn=ip_ecn,
            ipv4_tos=ipv4_tos,
            latency_tag=latency_tag
        )

    if isinstance(source_port, IPv6Port):
        ipv6_tc = ip_traffic_class

        return IPv6Frame(
            length=length,
            udp_src=udp_src,
            udp_dest=udp_dest,
            ip_dscp=ip_dscp,
            ip_ecn=ip_ecn,
            ipv6_tc=ipv6_tc,
            latency_tag=latency_tag
        )

    raise InvalidInput('Unsupported Port type')
