"""Interfaces for traffic generation."""
# `Flow` is not really needed, but is useful for type hinting:
from ._traffic.constants import DEFAULT_IP_DSCP  # for user convenience
from ._traffic.constants import DEFAULT_IP_ECN  # for user convenience
from ._traffic.flow import Flow  # noqa: F401; pylint: disable=unused-import
from ._traffic.frame import DEFAULT_FRAME_LENGTH  # for user convenience
from ._traffic.frame import ETHERNET_FCS_LENGTH  # for user convenience
from ._traffic.frame import ETHERNET_HEADER_LENGTH  # for user convenience
from ._traffic.frame import ETHERNET_PAUSE_LENGTH  # for user convenience
from ._traffic.frame import ETHERNET_PHYSICAL_OVERHEAD  # for user convenience
from ._traffic.frame import ETHERNET_PREAMBLE_LENGTH  # for user convenience
from ._traffic.frame import ETHERNET_SFD_LENGTH  # for user convenience
from ._traffic.frame import UDP_DYNAMIC_PORT_START  # for user convenience
from ._traffic.frame import UDP_HEADER_LENGTH  # for user convenience
from ._traffic.frame import VLAN_HEADER_LENGTH  # for user convenience
from ._traffic.frame import Frame
from ._traffic.frameblastingflow import FrameBlastingFlow
from ._traffic.gamingflow import GamingFlow
from ._traffic.helpers import string_array_to_int  # for user convenience
from ._traffic.httpflow import HTTPFlow
from ._traffic.imix import DEFAULT_IMIX_FRAME_CONFIG  # for user convenience
from ._traffic.imix import Imix, ImixFrameConfig
from ._traffic.ipv4.frame import \
    IPV4_FULL_HEADER_LENGTH  # for user convenience
from ._traffic.ipv4.frame import IPV4_HEADER_LENGTH  # for user convenience
from ._traffic.ipv4.frame import IPv4Frame
from ._traffic.ipv6.frame import \
    IPV6_FULL_HEADER_LENGTH  # for user convenience
from ._traffic.ipv6.frame import IPV6_HEADER_LENGTH  # for user convenience
from ._traffic.ipv6.frame import IPv6Frame
from ._traffic.tcpflow import HttpMethod, TCPCongestionAvoidanceAlgorithm
from ._traffic.videoflow import VideoFlow
from ._traffic.voiceflow import VoiceFlow

# Export the user interfaces.
#
# Outcomes:
# * Limits import on `from byteblower_test_framework.traffic import *`
# * Exposes the interfaces in the (Sphinx) documentation
#
# NOTE
#   Exporting imported variables does not introduce them in the (Sphinx) docs.
#   For example 'DEFAULT_FRAME_LENGTH', 'IPV4_HEADER_LENGTH',
#   'IPV6_HEADER_LENGTH', ...
#   It does introduce their name and value in `help()` of this module though.
#
__all__ = (
    # Constants:
    'DEFAULT_FRAME_LENGTH',
    'DEFAULT_IMIX_FRAME_CONFIG',
    # OSI Layer 1/2 constants:
    'ETHERNET_PREAMBLE_LENGTH',
    'ETHERNET_SFD_LENGTH',
    'ETHERNET_PAUSE_LENGTH',
    'ETHERNET_PHYSICAL_OVERHEAD',
    'ETHERNET_FCS_LENGTH',
    'ETHERNET_HEADER_LENGTH',
    'VLAN_HEADER_LENGTH',
    # OSI Layer 3 constants:
    'IPV4_FULL_HEADER_LENGTH',
    'IPV4_HEADER_LENGTH',
    'IPV6_FULL_HEADER_LENGTH',
    'IPV6_HEADER_LENGTH',
    'DEFAULT_IP_DSCP',
    'DEFAULT_IP_ECN',
    # OSI Layer 4 constants:
    'UDP_HEADER_LENGTH',
    'UDP_DYNAMIC_PORT_START',
    # Frames:
    Imix.__name__,
    ImixFrameConfig.__name__,
    Frame.__name__,
    IPv4Frame.__name__,
    IPv6Frame.__name__,
    # Basic/generic flows:
    FrameBlastingFlow.__name__,
    HTTPFlow.__name__,
    HttpMethod.__name__,
    TCPCongestionAvoidanceAlgorithm.__name__,
    # Application simulation:
    VoiceFlow.__name__,
    GamingFlow.__name__,
    VideoFlow.__name__,
    # Helper functions
    string_array_to_int.__name__,  # exported to include in docs
)
