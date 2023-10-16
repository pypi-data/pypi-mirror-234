#
# Copyright (c) 2023 SICK AG
# SPDX-License-Identifier: MIT
#

import numpy as np
import struct

"""This module contains helper functions which decode binary data contained in the
MSGPACK data format to numpy arrays
"""


def DecodeFloatChannel(channel: dict) -> np.array:
    """Interprets the binary data as an array of float32 values.

    Args:
        channel (dict): Dictionary containing the channel data and meta information

    Returns:
        np.array: Array of the decoded values
    """

    return _decodeChannel(channel, 'f')


def DecodeUint32Channel(channel: dict):
    """Interprets the binary data as an array of uint32 values.

    Args:
        channel (dict): Dictionary containing the channel data and meta information

    Returns:
        np.array: Array of the decoded values
    """
    return _decodeChannel(channel, 'I')


def DecodeUint16Channel(channel: dict):
    """Interprets the binary data as an array of uint16 values.

    Args:
        channel (dict): Dictionary containing the channel data and meta information

    Returns:
        np.array: Array of the decoded values
    """
    return _decodeChannel(channel, 'H')


def DecodeInt16Channel(channel: dict):
    """Interprets the binary data as an array of int16 values.

    Args:
        channel (dict): Dictionary containing the channel data and meta information

    Returns:
        np.array: Array of the decoded values
    """
    return _decodeChannel(channel, 'h')


def DecodeUint8Channel(channel: dict):
    """Interprets the binary data as an array of uint8 values.

    Args:
        channel (dict): Dictionary containing the channel data and meta information

    Returns:
        np.array: Array of the decoded values
    """
    return _decodeChannel(channel, 'B')


def _decodeChannel(channel: dict, format: str) -> np.array:
    """Interprets the binary data as an array of values of the type specified in format.

    Args:
        channel (dict): dictionary containing the channel data and meta information
        format (str): The format that the data is encoded with

    Returns:
        np.array: Array of the decoded values
    """

    nbBeams = channel['numOfElems']
    # < explicitly states little endianess
    formatArray = "<" + str(nbBeams) + format
    channelData = np.asarray(struct.unpack(formatArray, channel['data']))
    return channelData
