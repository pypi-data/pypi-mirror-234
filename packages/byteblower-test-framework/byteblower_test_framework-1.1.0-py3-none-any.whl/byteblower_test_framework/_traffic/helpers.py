"""Helper functions for data traffic configuration."""
from typing import Optional, Union  # for type hinting

from ..exceptions import ConflictingInput, InvalidInput
from .constants import DEFAULT_IP_DSCP, DEFAULT_IP_ECN

__all__ = (
    'get_ip_traffic_class',
    'build_ip_traffic_class',
    'string_array_to_int',
)


def get_ip_traffic_class(
    ip_field_name: str,
    ip_traffic_class: Optional[int] = None,
    ip_dscp: Optional[int] = None,
    ip_ecn: Optional[int] = None,
) -> int:
    """Select values and build the IP traffic class field.

    The IP traffic class field is the Type of Service (ToS) field in IPv4
    or the Traffic Class field in IPv6.

    The field value can be built from either:

    * ``ip_traffic_class``: Exact value value of the IPv4 ToS field
      and/or IPv6 Traffic Class field.
    * ``ip_dscp`` + ``ip_ecn``: Combine the IP DS and IP ECN values

    .. note::
       The ``ip_traffic_class`` and ``ip_dscp`` + ``ip_ecn`` combination
       is mutual exclusive. Either provide ``ip_traffic_class`` **or**
       ``ip_dscp`` and/or ``ip_ecn``, but never both.

    :param ip_field_name: Name of the field where you want to use the
       returned value. For example "IPv4 ToS" or "IPv6 Traffic Class".
    :type ip_field_name: str
    :param ip_traffic_class: The IP traffic class value is used to
       specify the exact value of either the *IPv4 ToS field* or the
       *IPv6 Traffic Class field*,
       mutual exclusive with ``ip_dscp`` and ``ip_ecn``,
       defaults to field value composed from ``ip_dscp`` and ``ip_ecn``.
    :type ip_traffic_class: Optional[int], optional
    :param ip_dscp: IP Differentiated Services Code Point (DSCP),
        mutual exclusive with ``ip_traffic_class``,
        defaults to :const:`DEFAULT_IP_DSCP`
    :type ip_dscp: Optional[int], optional
    :param ip_ecn: IP Explicit Congestion Notification (ECN),
        mutual exclusive with ``ip_traffic_class``,
        defaults to :const:`DEFAULT_IP_ECN`
    :type ip_ecn: Optional[int], optional
    :raises ConflictingInput: When invalid combination of configuration
       parameters is given
    :raises InvalidInput: When invalid configuration values are given.
    :return: IPv4 ToS / IPv6 Traffic Class field value
    :rtype: int
    """
    if ip_traffic_class is not None:
        if ip_dscp is not None or ip_ecn is not None:
            raise ConflictingInput(
                f"Provide either {ip_field_name} or DSCP/ECN but not both"
            )
        return ip_traffic_class

    # Convert DSCP/ECN to IPv4 ToS field
    return build_ip_traffic_class(ip_dscp=ip_dscp, ip_ecn=ip_ecn)


def build_ip_traffic_class(
    ip_dscp: Optional[int] = None,
    ip_ecn: Optional[int] = None,
) -> int:
    """Convert DSCP/ECN to IPv4 ToS / IPv6 Traffic Class.

    :param ip_dscp: IP Differentiated Services Code Point (DSCP),
        defaults to :const:`DEFAULT_IP_DSCP`
    :type ip_dscp: Optional[int], optional
    :param ip_ecn: IP Explicit Congestion Notification (ECN),
        defaults to :const:`DEFAULT_IP_ECN`
    :type ip_ecn: Optional[int], optional
    :raises InvalidInput: When invalid configuration values are given.
    :return: IPv4 ToS / IPv6 Traffic Class field value
    :rtype: int
    """
    # Perform a sanity check if the user provided ECN and DSCP values:
    if ip_dscp is not None:
        if ip_dscp < 0 or ip_dscp > 0x3f:
            raise InvalidInput(
                'Invalid DSCP value: Should a positive 6-bit integer'
            )
    else:
        ip_dscp = DEFAULT_IP_DSCP
    if ip_ecn is not None:
        if ip_ecn < 0 or ip_ecn > 0x03:
            raise InvalidInput(
                'Invalid ECN value: Should a positive 2-bit integer'
            )
    else:
        ip_ecn = DEFAULT_IP_ECN

    # Convert IPv4 ToS / IPv6 Traffic Class field
    return ((ip_dscp & 0x3f) << 2) + ip_ecn


def string_array_to_int(value: Union[int, str, bytes, bytearray]) -> int:
    """Assure that a given value is an integer.

    The ``value`` will be parsed from string if it is not already
    an integer type.

    This function can help to allow script users to provide values in a
    human-readable format. For example IP DSCP values in hexadecimal string
    format in a JSON file. Where JSON only supports integer values in
    decimal format.

    :param value: Value to convert
    :type value: Union[int, str, bytes, bytearray]
    :return: Integer value converted from the input
    :rtype: int
    """
    if isinstance(value, (str, bytes, bytearray)):
        return int(value, 0)

    return value
