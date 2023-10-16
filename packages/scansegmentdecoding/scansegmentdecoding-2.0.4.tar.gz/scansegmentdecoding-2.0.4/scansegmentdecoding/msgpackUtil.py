#
# Copyright (c) 2023 SICK AG
# SPDX-License-Identifier: MIT
#

import msgpack

"""This module contains functions to process data in the MSGPACK format.
"""

_KeywordIntegerLUT = {
    # General [0x10 - 0x2F]
    "class":                0x10,
    "data":                 0x11,
    "numOfElems":           0x12,
    "elemSz":              0x13,
    "endian":               0x14,
    "elemTypes":            0x15,
    # Constant values [0x30 - 0x4F]
    "little":              0x30,
    "float32":             0x31,
    "uint32":              0x32,
    "uint8":               0x33,
    "uint16":              0x34,
    "int16":               0x35,
    # Channels [0x50 - 0x6F]
    "ChannelTheta":        0x50,
    "ChannelPhi":          0x51,
    "DistValues":          0x52,
    "RssiValues":          0x53,
    "PropertiesValues":    0x54,
    # Scan fields [0x70 - 0x8F]
    "Scan":                0x70,
    "TimestampStart":      0x71,
    "TimestampStop":       0x72,
    "ThetaStart":          0x73,
    "ThetaStop":           0x74,
    "ScanNumber":          0x75,
    "ModuleID":            0x76,
    "BeamCount":           0x77,
    "EchoCount":           0x78,
    # Segment fields [0x90 - 0xAF]
    "ScanSegment":         0x90,
    "SegmentCounter":      0x91,
    "FrameNumber":         0x92,
    "Availability":        0x93,
    "SenderId":            0x94,
    "SegmentSize":         0x95,
    "SegmentData":         0x96,
    "LayerId":             0xA0,
    # Telegram Fields
    "TelegramCounter":     0xB0,
    "TimestampTransmit":    0xB1
}

_IntegerKeywordLUT = {value: key for (
    key, value) in _KeywordIntegerLUT.items()}


def UnpackMsgpackAndReplaceIntegerKeywords(buffer: bytes) -> dict:
    """
    Unpacks the given msgpack structure. Integers are replaced by string keywords.

    Args:
        msgpackValue (bytes): The buffer to unpack

    Returns:
        dict: The unpacked msgpack buffer
    """
    unpacked = msgpack.unpackb(buffer, strict_map_key=False)
    ReplaceKeywordsInDict(unpacked)
    return unpacked


def ReplaceKeywordsInDict(msgpackValue: dict) -> dict:
    """
    Replaces the integers in the given msgpack object serving as keywords with human-readable
    strings (see self.keywordIntegerLUT).

    Args:
        msgpackValue (dict): msgpack object for which to replace the integer keywords

    Returns:
        dict: The msgpack dictionary with replaced integer keys
    """
    if isinstance(msgpackValue, dict):
        intKeys = list(msgpackValue)
        for ikey in intKeys:
            stringKey = _IntegerKeywordLUT[ikey]
            if stringKey in ["class", "endian"]:
                msgpackValue[stringKey] = _IntegerKeywordLUT[msgpackValue.pop(
                    ikey)]
            else:
                msgpackValue[stringKey] = msgpackValue.pop(ikey)

            if isinstance(msgpackValue[stringKey], dict):
                msgpackValue[stringKey] = ReplaceKeywordsInDict(
                    msgpackValue[stringKey])
            if isinstance(msgpackValue[stringKey], list):
                for idx, elem in enumerate(msgpackValue[stringKey]):
                    if stringKey == "elemTypes":
                        msgpackValue[stringKey][
                            idx] = _IntegerKeywordLUT[elem]
                    else:
                        elem = ReplaceKeywordsInDict(elem)
    return msgpackValue
