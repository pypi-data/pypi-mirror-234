from dataclasses import dataclass
from random import shuffle
from typing import TYPE_CHECKING, Optional, Sequence  # for type hinting

from .._endpoint.port import Port  # for type hinting
from .._factory.frame import create_frame
from .frame import Frame  # for type hinting
from .frame import UDP_DYNAMIC_PORT_START

if TYPE_CHECKING:
    # NOTE: Import because referenced in docstrings:
    from .constants import DEFAULT_IP_DSCP, DEFAULT_IP_ECN


@dataclass
class ImixFrameConfig(object):
    """Configuration for an IMIX frame."""

    #: Frame length. This is the layer 2 (Ethernet) frame length
    #: *excluding* Ethernet FCS and *excluding* VLAN tags.
    length: int
    #: Weight of this frame size in the list of frames in the :class:`Imix`.
    weight: int


#: Default frame configuration for the :class:`Imix`.
DEFAULT_IMIX_FRAME_CONFIG = [
    ImixFrameConfig(length=72, weight=34),
    ImixFrameConfig(length=124, weight=6),
    ImixFrameConfig(length=252, weight=4),
    ImixFrameConfig(length=508, weight=4),
    ImixFrameConfig(length=1020, weight=9),
    ImixFrameConfig(length=1276, weight=25),
    ImixFrameConfig(length=1510, weight=18),
]


class Imix(object):
    """
    Configuration of an Internet mix.

    For a given UDP source and destination port,
    define a weighted collection of frame sizes.

    .. note::
       We tend to use a single UDP port for all frames. This has some benefits
       in initialization time (for example much less need for NAT resolution).
    """

    __slots__ = (
        '_frame_config',
        '_udp_src',
        '_udp_dest',
        '_ip_dscp',
        '_ip_ecn',
        '_ip_traffic_class',
        '_latency_tag',
        '_random_order',
    )

    def __init__(
        self,
        frame_config: Sequence[ImixFrameConfig] = DEFAULT_IMIX_FRAME_CONFIG,
        udp_src: int = UDP_DYNAMIC_PORT_START,
        udp_dest: int = UDP_DYNAMIC_PORT_START,
        ip_dscp: Optional[int] = None,
        ip_ecn: Optional[int] = None,
        ip_traffic_class: Optional[int] = None,
        latency_tag: bool = False,
        random_order: bool = True,
    ) -> None:
        """Create a frame based on the (source) Port type.

        :param frame_config: Collection of IMIX frame configurations,
           defaults to :const:`DEFAULT_IMIX_FRAME_CONFIG`
        :type frame_config: Sequence[ImixFrameConfig], optional
        :param udp_src: UDP source port, defaults to
           :const:`UDP_DYNAMIC_PORT_START`
        :type udp_src: int, optional
        :param udp_dest: UDP destination port, defaults to
           :const:`UDP_DYNAMIC_PORT_START`
        :type udp_dest: int, optional
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
        :param latency_tag: Enable latency tag generation in the Frame,
           defaults to ``False``
        :type latency_tag: bool, optional
        :param random_order: Enable shuffle of the generated frames,
           defaults to ``True``
        :type random_order: bool, optional
        :raises InvalidInput: When invalid configuration values are given.
        :raises ConflictingInput: When invalid combination of configuration
            parameters is given
        """
        self._frame_config = frame_config
        self._udp_src = udp_src
        self._udp_dest = udp_dest
        self._ip_dscp = ip_dscp
        self._ip_ecn = ip_ecn
        self._ip_traffic_class = ip_traffic_class
        self._latency_tag = latency_tag
        self._random_order = random_order

    def _generate(self, source_port: Port) -> Sequence[Frame]:
        udp_src = self._udp_src
        udp_dest = self._udp_dest
        latency_tag = self._latency_tag

        frame_list: Sequence[Frame] = []
        for imix_frame_config in self._frame_config:
            for _ in range(imix_frame_config.weight):
                frame = create_frame(
                    source_port,
                    length=imix_frame_config.length,
                    udp_src=udp_src,
                    udp_dest=udp_dest,
                    ip_dscp=self._ip_dscp,
                    ip_ecn=self._ip_ecn,
                    ip_traffic_class=self._ip_traffic_class,
                    latency_tag=latency_tag
                )
                frame_list.append(frame)
        if self._random_order:
            # Place the frames in a random order.
            shuffle(frame_list)
        return frame_list

    @property
    def udp_src(self) -> int:
        """UDP source port."""
        return self._udp_src

    @property
    def udp_dest(self) -> int:
        """UDP destination port."""
        return self._udp_dest
