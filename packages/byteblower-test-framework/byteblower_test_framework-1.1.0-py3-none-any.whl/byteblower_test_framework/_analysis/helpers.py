"""Helper functions for traffic result analysis."""
from collections import abc
from typing import Optional, Tuple, Union  # for type hinting

from pandas import DataFrame

from .._report.options import Layer2Speed
from .._traffic.frame import ETHERNET_FCS_LENGTH, ETHERNET_PHYSICAL_OVERHEAD
from ..exceptions import ByteBlowerTestFrameworkException

__all__ = (
    'BITS_PER_BYTE',
    'include_ethernet_overhead',
    'to_bitrate',
)

# Type aliases
DataKey = str
DataWithKey = Tuple[DataFrame, DataKey]
ByteOrCountData = Union[int, float, DataWithKey]
ByteOrCountStorage = Union[int, float, DataFrame]
ByteOrCountValue = Union[int, float, DataFrame]

BITS_PER_BYTE: int = 8
NO_SCALING: int = 1
KILO: int = 1000
MEGA: int = KILO * KILO


def to_bitrate(
    byte_rate_data: ByteOrCountValue, *, scaling_factor: int = NO_SCALING
):
    value_storage, value_key = _check_byte_or_count_data(
        'byte_rate_data', byte_rate_data
    )

    # TODO: Should we always return the filtered view?
    if value_key is not None:
        # Return filtered view on the value storage
        filtered_value_storage = value_storage[[value_key]]
    else:
        filtered_value_storage = value_storage

    # Where will we store the converted value(s) ?
    return_value_storage = _ensure_copy(filtered_value_storage)

    # ! FIXME: in-place conversion does not work on Windows 10/Python 3.10 !?
    return_value_storage = _to_bitrate(
        return_value_storage, scaling_factor=scaling_factor
    )

    return return_value_storage


def _to_bitrate(
    byte_rate: ByteOrCountValue, *, scaling_factor: int = NO_SCALING
):
    """Convert the byte_rate in-place and return the converted value."""
    # NOTE: More efficient to do it in one conversion (especially with pandas DataFrames)
    byte_rate *= BITS_PER_BYTE / scaling_factor
    return byte_rate


def include_ethernet_overhead(
    layer2_speed: Optional[Layer2Speed],
    value_data: ByteOrCountData,
    count_data: ByteOrCountData,
) -> ByteOrCountStorage:
    """Include Ethernet Layer 1/2 overhead in the value data.

    When the ``value_data`` or ``count_data`` are :class:`DataFrame` objects,
    they must be provided as a tuple of the ``DataFrame`` and a "key".
    The "key" defines which column of the ``DataFrame`` to process.

    With a ``value_data`` being a :class:`DataFrame`, the "key" will also be
    used to *filter* the output. The returned value will be a ``DataFrame``,
    only containing the (adjusted) values for column defined by the "key".

    For use with numeric values:

    >>> total_tx_bytes = include_ethernet_overhead(
    >>>     Layer2Speed.physical, total_tx_bytes, total_tx_packets
    >>> )

    For use with ``DataFrame`` values:

    >>> df_rx_bytes = include_ethernet_overhead(
    >>>     Layer2Speed.frame_with_fcs, (df_rx, 'Bytes interval'),
    >>>     (df_rx, 'Packets interval')
    >>> )

    .. note::
       If necessary, this function will create a copy of ``value_data``
       to avoid ``SettingWithCopyWarning`` errors on :class:`DataFrame`.

    :param layer2_speed: Defines which overhead to include
    :type layer2_speed: Optional[Layer2Speed]
    :param value_data: Input value(s).

       .. note::
          It MUST contain the number of Ethernet bytes excluding Ethernet FCS.
    :type value_data: ByteOrCountData
    :param count_data: Packet count(s) for the values in ``value_data``.
    :type count_data: ByteOrCountData
    :raises ByteBlowerTestFrameworkException:
       When providing invalid input value(s) or count(s).
    :return: (filtered) ``value_data`` adjusted to the ``layer2_speed``.
    :rtype: ByteOrCountStorage
    """
    # Sanity checks
    value_storage, value_key = _check_byte_or_count_data(
        'value_data', value_data
    )
    count_storage, count_key = _check_byte_or_count_data(
        'count_data', count_data
    )

    # TODO: Should we always return the filtered view?
    if value_key is not None:
        # Return filtered view on the value storage
        filtered_value_storage = value_storage[[value_key]]
    else:
        filtered_value_storage = value_storage

    # How do we need to convert the value ?
    if layer2_speed is None:
        # Don't do any conversion
        return filtered_value_storage
    if layer2_speed == Layer2Speed.frame:
        # Values already are in the correct format
        return filtered_value_storage
    if layer2_speed == Layer2Speed.frame_with_fcs:
        include_overhead_function = _include_fcs_overhead
    elif layer2_speed == Layer2Speed.physical:
        include_overhead_function = _include_fcs_physical_overhead
    else:
        raise ByteBlowerTestFrameworkException(
            f'Unsupported Layer 2 speed: {layer2_speed}'
        )

    # Where will we store the converted value(s) ?
    return_value_storage = _ensure_byte_or_count_applicable(
        layer2_speed, filtered_value_storage
    )

    #  Where to get the input values from ?
    if count_key is not None:
        count_storage_ = count_storage[count_key]
    else:
        count_storage_ = count_storage

    if value_key is not None:
        return_value_storage[value_key] = include_overhead_function(
            value_storage[value_key], count_storage_
        )
    else:
        return_value_storage = include_overhead_function(
            value_storage, count_storage_
        )

    return return_value_storage


def _check_byte_or_count_data(
    _name: str, byte_or_count_data: ByteOrCountData
) -> Tuple[ByteOrCountStorage, DataKey]:
    if isinstance(byte_or_count_data, abc.Sequence):
        return _check_byte_or_count_data_tuple(_name, byte_or_count_data)

    return byte_or_count_data, None


def _check_byte_or_count_data_tuple(
    _name: str, byte_or_count_data: DataWithKey
) -> Tuple[ByteOrCountStorage, DataKey]:
    if len(byte_or_count_data) != 2:
        raise ByteBlowerTestFrameworkException(
            f'Invalid content of {_name}.'
            f' Requires tuple of pandas DataFrame and {_name} string'
        )

    data_storage, data_key = byte_or_count_data

    if not isinstance(data_storage, DataFrame):
        raise ByteBlowerTestFrameworkException(
            'Data storage MUST be pandas DataFrame'
        )
    if not isinstance(data_key, str):
        raise ByteBlowerTestFrameworkException(
            f'{_name} is required for use with pandas DataFrame'
        )

    return data_storage, data_key


def _ensure_byte_or_count_applicable(
    layer2_speed: Optional[Layer2Speed], value_storage: ByteOrCountStorage
) -> ByteOrCountStorage:
    if (isinstance(value_storage, DataFrame)
            and layer2_speed not in (None, Layer2Speed.frame)):
        # NOTE - Create a copy to avoid SettingWithCopyWarning !
        #
        #     pandas/core/indexing.py:1951: SettingWithCopyWarning:
        #     A value is trying to be set on a copy of a slice
        #     from a DataFrame.
        #     Try using .loc[row_indexer,col_indexer] = value instead

        #     See the caveats in the documentation:
        #       https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy  # noqa: E501, pylint: disable=line-too-long
        #     self.obj[selected_item_labels] = value
        return value_storage.copy()
    return value_storage


def _ensure_copy(value_storage: ByteOrCountStorage) -> ByteOrCountStorage:
    if isinstance(value_storage, DataFrame):
        return value_storage.copy()
    return value_storage


def _include_fcs_overhead(
    value: ByteOrCountValue, count: ByteOrCountValue
) -> ByteOrCountValue:
    # NOTE - Also returns the correct value when value or count is zero.
    return value + ETHERNET_FCS_LENGTH * count


def _include_physical_overhead(
    value: ByteOrCountValue, count: ByteOrCountValue
) -> ByteOrCountValue:
    # NOTE - Also returns the correct value when value or count is zero.
    return value + ETHERNET_PHYSICAL_OVERHEAD * count


def _include_fcs_physical_overhead(
    value: ByteOrCountValue, count: ByteOrCountValue
) -> ByteOrCountValue:
    # NOTE - Also returns the correct value when value or count is zero.
    # Cfr.
    # return _include_physical_overhead(
    #     _include_fcs_overhead(value, count), count
    # )
    return value + (ETHERNET_FCS_LENGTH + ETHERNET_PHYSICAL_OVERHEAD) * count
