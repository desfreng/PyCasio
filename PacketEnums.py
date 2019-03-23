#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 22:21:50 2019

@author: gabriel
"""

from enum import Enum


class PacketType(Enum):
    Command = 0x01
    Data = 0x02
    Roleswap = 0x03
    Check = 0x05
    Ack = 0x06
    Error = 0x15
    Terminate = 0x18

    Unknown = 0x0


class UnknownPacketType(Enum):
    Unknown = b"00"


class CommandPacketType:
    class System(Enum):
        Reset = b"00"
        GetInfo = b"01"
        SetLinkSettings = b"03"

    class MCSStorage(Enum):
        CreateDirectory = b"20"
        DeleteDirectory = b"21"
        RenameDirectory = b"22"
        ChangeWorkingDirectory = b"23"

        FileTransferRequest = b"24"
        FileTransferAllRequest = b"29"
        FileTransfer = b"25"

        DeleteFile = b"26"
        RenameFile = b"27"
        CopyFile = b"28"

        CapacityTransmitRequest = b"2B"
        CapacityTransmit = b"2C"

        FileInfoTransferAllRequest = b"2D"
        FileInfoTransfer = b"2E"

        RAMImageTransferRequest = b"2F"
        RAMImageTransfer = b"30"

        SetupEntryTransferRequest = b"31"
        SetupEntryTransfer = b"32"
        SetupEntryTransferAllRequest = b"33"

    class FlashStorage(Enum):
        CreateDirectory = b"40"
        DeleteDirectory = b"41"
        RenameDirectory = b"42"
        ChangeWorkingDirectory = b"43"

        FileTransferRequest = b"44"
        FileTransfer = b"45"
        FileTransferAllRequest = b"49"

        DeleteFile = b"46"
        RenameFile = b"47"
        CopyFile = b"48"

        CapacityTransmitRequest = b"4B"
        CapacityTransmit = b"4C"

        FileInfoTransferAllRequest = b"4D"
        FileInfoTransfer = b"4E"

        FlashImageTransferRequest = b"4F"
        FlashImageTransfer = b"50"

        OptimizeFiseSystem = b"51"


class DataPacketType:
    class MCSStorage(Enum):
        CreateDirectory = b"20"
        DeleteDirectory = b"21"
        RenameDirectory = b"22"
        ChangeWorkingDirectory = b"23"

        FileTransferRequest = b"24"
        FileTransferAllRequest = b"29"
        FileTransfer = b"25"

        DeleteFile = b"26"
        RenameFile = b"27"
        CopyFile = b"28"

        CapacityTransmitRequest = b"2B"
        CapacityTransmit = b"2C"

        FileInfoTransferAllRequest = b"2D"
        FileInfoTransfer = b"2E"

        RAMImageTransferRequest = b"2F"
        RAMImageTransfer = b"30"

        SetupEntryTransferRequest = b"31"
        SetupEntryTransfer = b"32"
        SetupEntryTransferAllRequest = b"33"

    class FlashStorage(Enum):
        CreateDirectory = b"40"
        DeleteDirectory = b"41"
        RenameDirectory = b"42"
        ChangeWorkingDirectory = b"43"

        FileTransferRequest = b"44"
        FileTransfer = b"45"
        FileTransferAllRequest = b"49"

        DeleteFile = b"46"
        RenameFile = b"47"
        CopyFile = b"48"

        CapacityTransmitRequest = b"4B"
        CapacityTransmit = b"4C"

        FileInfoTransferAllRequest = b"4D"
        FileInfoTransfer = b"4E"

        FlashImageTransferRequest = b"4F"
        FlashImageTransfer = b"50"

        OptimizeFiseSystem = b"51"


class RoleswapPacketType(Enum):
    Default = b"00"


class CheckPacketType(Enum):
    InitConnection = b"00"
    CheckConnection = b"01"


class AckPacketType(Enum):
    Default = b"00"
    YesOverwriteReply = b"01"
    ExtendedAck = b"03"


class ErrorPacketType(Enum):
    Default = b"00"
    ResendRequest = b"01"
    Overwrite = b"02"
    NoOverwriteReply = b"03"
    OverwriteImpossible = b"04"
    MemoryFull = b"05"


class TerminatePacketType(Enum):
    Default = b"00"
    UserRequest = b"01"
    Timeout = b"02"
    Overwrite = b"03"
