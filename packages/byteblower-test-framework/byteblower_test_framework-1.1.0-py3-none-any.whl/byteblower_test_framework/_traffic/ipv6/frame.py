"""IPv6 Frame interface module."""
from typing import TYPE_CHECKING, Optional

from scapy.layers.inet6 import UDP, Ether, IPv6
from scapy.packet import Raw

from ..._endpoint.ipv6.port import IPv6Port  # for type hinting
from ..frame import ETHERNET_HEADER_LENGTH, UDP_HEADER_LENGTH, Frame
from ..helpers import get_ip_traffic_class

if TYPE_CHECKING:
    # NOTE: Import because referenced in docstrings:
    from ...exceptions import ConflictingInput
    from ..constants import DEFAULT_IP_DSCP, DEFAULT_IP_ECN
    from ..frame import DEFAULT_FRAME_LENGTH, UDP_DYNAMIC_PORT_START

IPV6_HEADER_LENGTH: int = 40

IPV6_FULL_HEADER_LENGTH = (
    ETHERNET_HEADER_LENGTH +  # noqa: W504
    IPV6_HEADER_LENGTH + UDP_HEADER_LENGTH
)
assert IPV6_FULL_HEADER_LENGTH == 62, 'Incorrect IPv6 full header length'


class IPv6Frame(Frame):
    """Frame interface for IPv6."""

    __slots__ = ("_ip_tc", )

    def __init__(
        self,
        length: Optional[int] = None,
        udp_src: Optional[int] = None,
        udp_dest: Optional[int] = None,
        ip_dscp: Optional[int] = None,
        ip_ecn: Optional[int] = None,
        ipv6_tc: Optional[int] = None,
        latency_tag: bool = False
    ) -> None:
        """Create the interface to an IPv6 frame.

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
           mutual exclusive with ``ipv6_tc``,
           defaults to :const:`DEFAULT_IP_DSCP`
        :type ip_dscp: Optional[int], optional
        :param ip_ecn: IP Explicit Congestion Notification (ECN),
           mutual exclusive with ``ipv6_tc``,
           defaults to :const:`DEFAULT_IP_ECN`
        :type ip_ecn: Optional[int], optional
        :param ipv6_tc: Exact IPv6 Traffic Class field,
           mutual exclusive with ``ip_dscp`` and ``ip_ecn``,
           defaults to field value composed from ``ip_dscp`` and ``ip_ecn``.
        :type ipv6_tc: Optional[int], optional
        :param latency_tag: Enable latency tag generation in the Frame,
           defaults to ``False``
        :type latency_tag: bool, optional
        :raises InvalidInput: When invalid configuration values are given.
        :raises ConflictingInput: When invalid combination of configuration
           parameters is given
        """
        super().__init__(
            IPV6_FULL_HEADER_LENGTH, length, udp_src, udp_dest, latency_tag
        )

        self._ip_tc = get_ip_traffic_class(
            "IPv6 Traffic Class",
            ip_traffic_class=ipv6_tc,
            ip_dscp=ip_dscp,
            ip_ecn=ip_ecn,
        )

    def _build_frame_content(
        self, source_port: IPv6Port, destination_port: IPv6Port
    ) -> Ether:
        udp_dest = self._udp_dest
        udp_src = self._udp_src
        ip_dest = str(destination_port.ip)
        ip_src = str(source_port.ip)
        ipv6_tc = self._ip_tc
        mac_src = source_port.mac
        mac_dst = source_port.layer3.Resolve(ip_dest)

        scapy_layer2_5_headers = self._build_layer2_5_headers(source_port)

        payload = self._build_payload(IPV6_FULL_HEADER_LENGTH)

        scapy_udp_payload = Raw(payload.encode('ascii', 'strict'))
        scapy_udp_header = UDP(dport=udp_dest, sport=udp_src)
        scapy_ip_header = IPv6(src=ip_src, dst=ip_dest, tc=ipv6_tc)
        scapy_ethernet_header = Ether(src=mac_src, dst=mac_dst)
        for scapy_layer2_5_header in scapy_layer2_5_headers:
            scapy_ethernet_header /= scapy_layer2_5_header
        scapy_frame = (
            scapy_ethernet_header / scapy_ip_header / scapy_udp_header /
            scapy_udp_payload
        )

        return scapy_frame
