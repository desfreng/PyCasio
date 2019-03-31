#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum


_HEXADECIMAL_ARRAY = bytes("0123456789ABCDEF", "ascii")


def to_hexadecimal(number: int, field_size: int = 2) -> bytearray:
    output_array = bytearray()

    while number != 0:
        output_array.insert(0, _HEXADECIMAL_ARRAY[number % 16])
        number //= 16

    while len(output_array) < field_size:
        output_array.insert(0, _HEXADECIMAL_ARRAY[0])

    return output_array


def to_integer(number: bytes) -> int:
    output_number = 0
    number_index = len(number)

    for part in number:
        number_index -= 1
        # Séparation entre les lettres et les chiffres du code Hex
        if part > _HEXADECIMAL_ARRAY[9]:
            # Les lettres A-F sont codés en uint8 entre 65 et 70
            output_number += (part - _HEXADECIMAL_ARRAY[10] + 10) * 16 ** number_index
        else:
            # Les chiffres 0-9 sont codés en uint8 entre 48 et 57
            output_number += (part - _HEXADECIMAL_ARRAY[0]) * 16 ** number_index
    return output_number


class PacketType(Enum):  # [0 - 24]
    Unknown = 0x00  # Value : 0

    Command = 0x01  # Value : 1
    Data = 0x02  # Value : 2
    Roleswap = 0x03  # Value : 3
    Check = 0x05  # Value : 5
    Ack = 0x06  # Value : 6
    Error = 0x15  # Value : 21
    Terminate = 0x18  # Value : 24


class _SubType:
    pass


class PacketSubType(_SubType, Enum):
    Unknown = b"FF"


class CommandSubType(_SubType, Enum):
    # Commands & Data Types

    # System                   # [0 - 2]
    Reset = b"00"  # Value : 0
    GetInfo = b"01"  # Value : 1
    SetLinkSettings = b"02"  # Value : 2

    # MCS Storage              # [32 - 51]
    MCSCreateDirectory = b"20"  # Value : 32
    MCSDeleteDirectory = b"21"  # Value : 33
    MCSRenameDirectory = b"22"  # Value : 34
    MCSChangeWorkingDirectory = b"23"  # Value : 35

    MCSFileTransferRequest = b"24"  # Value : 36
    MCSFileTransferAllRequest = b"29"  # Value : 41
    MCSFileTransfer = b"25"  # Value : 37

    MCSDeleteFile = b"26"  # Value : 38
    MCSRenameFile = b"27"  # Value : 39
    MCSCopyFile = b"28"  # Value : 40

    MCSCapacityTransmitRequest = b"2B"  # Value : 43
    MCSCapacityTransmit = b"2C"  # Value : 44

    MCSFileInfoTransferAllRequest = b"2D"  # Value : 45
    MCSFileInfoTransfer = b"2E"  # Value : 46

    MCSImageTransferRequest = b"2F"  # Value : 47
    MCSImageTransfer = b"30"  # Value : 48

    MCSSetupEntryTransferRequest = b"31"  # Value : 49
    MCSSetupEntryTransfer = b"32"  # Value : 50
    MCSSetupEntryTransferAllRequest = b"33"  # Value : 51

    # FlashStorage Types       # [64 - 81]
    FlashCreateDirectory = b"40"  # Value : 64
    FlashDeleteDirectory = b"41"  # Value : 65
    FlashRenameDirectory = b"42"  # Value : 66
    FlashChangeWorkingDirectory = b"43"  # Value : 67

    FlashFileTransferRequest = b"44"  # Value : 68
    FlashFileTransfer = b"45"  # Value : 69
    FlashFileTransferAllRequest = b"49"  # Value : 73

    FlashDeleteFile = b"46"  # Value : 70
    FlashRenameFile = b"47"  # Value : 71
    FlashCopyFile = b"48"  # Value : 72

    FlashCapacityTransmitRequest = b"4B"  # Value : 75
    FlashCapacityTransmit = b"4C"  # Value : 76

    FlashFileInfoTransfer = b"4E"  # Value : 78
    FlashFileInfoTransferAllRequest = b"4D"  # Value : 77

    FlashImageTransferRequest = b"4F"  # Value : 79
    FlashImageTransfer = b"50"  # Value : 80

    OptimizeFileSystem = b"51"  # Value : 81


DataSubType = CommandSubType


class RoleswapSubType(_SubType, Enum):
    # Roleswap Types              # [0]
    Default = b"00"  # Value : 0


class CheckSubType(_SubType, Enum):
    # Check Types              # [0 - 1]
    InitConnection = b"00"  # Value : 0
    CheckConnection = b"01"  # Value : 1


class AckSubType(_SubType, Enum):
    # Ack Types                # [0 - 2]
    Default = b"00"  # Value : 0
    YesOverwriteReply = b"01"  # Value : 1
    ExtendedAck = b"02"  # Value : 2


class ErrorSubType(_SubType, Enum):
    # Error Types              # [0 - 5]
    Default = b"00"  # Value : 0
    ResendRequest = b"01"  # Value : 1
    OverwriteError = b"02"  # Value : 2
    NoOverwriteReply = b"03"  # Value : 3
    OverwriteImpossible = b"04"  # Value : 4
    MemoryFull = b"05"  # Value : 5


class TerminateSubType(_SubType, Enum):
    # Terminates Types         # [0 - 3]
    Default = b"00"  # Value : 0
    UserRequest = b"01"  # Value : 1
    Timeout = b"02"  # Value : 2
    Overwrite = b"03"  # Value : 3
