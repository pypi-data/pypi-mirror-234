"""Module for voice traffic generation."""
from datetime import timedelta  # for type hinting
from typing import TYPE_CHECKING, Optional, Union  # for type hinting

from .._endpoint.ipv4.port import IPv4Port  # for type hinting
from .._endpoint.ipv6.port import IPv6Port  # for type hinting
from .._endpoint.port import Port  # for type hinting
from .._factory.frame import create_frame
from ..exceptions import InvalidInput
from .frame import ETHERNET_HEADER_LENGTH
from .frameblastingflow import DEFAULT_NUMBER_OF_FRAMES, FrameBlastingFlow
from .ipv4.frame import IPV4_HEADER_LENGTH
from .ipv6.frame import IPV6_HEADER_LENGTH

if TYPE_CHECKING:
    # NOTE: Import because referenced in docstrings:
    from .constants import DEFAULT_IP_DSCP, DEFAULT_IP_ECN
    from .frame import UDP_DYNAMIC_PORT_START

DEFAULT_PACKETIZATION: int = 20  # ms


class VoiceFlow(FrameBlastingFlow):
    """Flow for simulating voice traffic.

    The implementation simulates G.711 RTP traffic.
    """

    def __init__(
        self,
        source: Port,
        destination: Port,
        name: Optional[str] = None,
        packetization: Optional[int] = None,
        number_of_frames: Optional[int] = None,
        duration: Optional[Union[timedelta, float, int]] = None,  # [seconds]
        initial_time_to_wait: Optional[Union[timedelta, float,
                                             int]] = None,  # [seconds]
        udp_src: Optional[int] = None,
        udp_dest: Optional[int] = None,
        ip_dscp: Optional[int] = None,
        ip_ecn: Optional[int] = None,
        ip_traffic_class: Optional[int] = None,
        enable_latency: Optional[bool] = False,
        **kwargs
    ) -> None:
        """Create a G.711 voice flow with the given packetization.

        Typical packetization times are:

        * 20ms packetization
           - Packet rate = 50 pps
           - RTP packet size = 160 Bytes
        * 10ms packetization
           - Packet rate = 100 pps
           - RTP packet size = 80 Bytes

        :param source: Sending port of the voice stream
        :type source: Port
        :param destination: Receiving port of the voice stream
        :type destination: Port
        :param name: Name of this Flow, defaults to auto-generated name
           when set to ``None``.
        :type name: Optional[str], optional
        :param packetization: Packetization time of the RTP packets in
           milliseconds, defaults to :const:`DEFAULT_PACKETIZATION`.
        :type packetization: Optional[int], optional
        :param number_of_frames: Number of frames to transmit,
           defaults to :const:`DEFAULT_NUMBER_OF_FRAMES`
        :type number_of_frames: Optional[int], optional
        :param duration: Duration of the flow in seconds,
           defaults to None (use number_of_frames instead)
        :type duration: Optional[Union[timedelta, float, int]], optional
        :param initial_time_to_wait: Initial time to wait to start the flow.
           In seconds, defaults to None (start immediately)
        :type initial_time_to_wait: Optional[Union[timedelta, float, int]],
           optional
        :param udp_src: UDP src port, defaults to
           :const`UDP_DYNAMIC_PORT_START`
        :type udp_src: Optional[int], optional
        :param udp_dest: UDP dest port, defaults to
           :const`UDP_DYNAMIC_PORT_START`
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
        :param enable_latency: Enable latency tag in the packets
           (required for latency measurements at the destination port),
           defaults to False
        :type enable_latency: Optional[bool], optional
        :raises InvalidInput:
           When the type of the given source port is not supported.
        """
        if packetization is None:
            packetization = DEFAULT_PACKETIZATION
        if number_of_frames is None:
            number_of_frames = DEFAULT_NUMBER_OF_FRAMES
        frame_rate: float = 1000 / packetization  # pps
        udp_length: int = int(8000 / 1000 * packetization)  # Bytes
        header_length = ETHERNET_HEADER_LENGTH
        if isinstance(source, IPv4Port):
            header_length += IPV4_HEADER_LENGTH
        elif isinstance(source, IPv6Port):
            header_length += IPV6_HEADER_LENGTH
        else:
            raise InvalidInput(
                f'Unsupported Port type: {type(source).__name__!r}'
            )
        frame_length = header_length + udp_length
        frame = create_frame(
            source,
            length=frame_length,
            udp_src=udp_src,
            udp_dest=udp_dest,
            ip_dscp=ip_dscp,
            ip_ecn=ip_ecn,
            ip_traffic_class=ip_traffic_class,
            latency_tag=enable_latency
        )
        super().__init__(
            source,
            destination,
            name=name,
            frame_rate=frame_rate,
            number_of_frames=number_of_frames,
            duration=duration,
            initial_time_to_wait=initial_time_to_wait,
            frame_list=[frame],
            **kwargs
        )
