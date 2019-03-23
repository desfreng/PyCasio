#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum


class PacketType(Enum):
    Command = 0x01
    Data = 0x02
    Roleswap = 0x03
    Check = 0x05
    Ack = 0x06
    Error = 0x15
    Terminate = 0x18


class CommandPacketType:
    class System(Enum):
        Reset = "00"
        GetInfo = "01"
        SetLinkSettings = "03"

    class MCSStorage(Enum):
        CreateDirectory = "20"
        DeleteDirectory = "21"
        RenameDirectory = "22"
        ChangeWorkingDirectory = "23"

        FileTransferRequest = "24"
        FileTransferAllRequest = "29"
        FileTransfer = "25"

        DeleteFile = "26"
        RenameFile = "27"
        CopyFile = "28"

        CapacityTransmitRequest = "2"
        CapacityTransmit = "2C"

        FileInfoTransferAllRequest = "2D"
        FileInfoTransfer = "2E"

        RAMImageTransferRequest = "2F"
        RAMImageTransfer = "30"

        SetupEntryTransferRequest = "31"
        SetupEntryTransfer = "32"
        SetupEntryTransferAllRequest = "33"

    class FlashStorage(Enum):
        CreateDirectory = "40"
        DeleteDirectory = "41"
        RenameDirectory = "42"
        ChangeWorkingDirectory = "43"

        FileTransferRequest = "44"
        FileTransfer = "45"
        FileTransferAllRequest = "49"

        DeleteFile = "46"
        RenameFile = "47"
        CopyFile = "48"

        CapacityTransmitRequest = "4"
        CapacityTransmit = "4C"

        FileInfoTransferAllRequest = "4D"
        FileInfoTransfer = "4E"

        FlashImageTransferRequest = "4F"
        FlashImageTransfer = "50"

        OptimizeFileSystem = "51"


class DataPacketType:
    class MCSStorage(Enum):
        CreateDirectory = CommandPacketType.MCSStorage.CreateDirectory
        DeleteDirectory = CommandPacketType.MCSStorage.DeleteDirectory
        RenameDirectory = CommandPacketType.MCSStorage.RenameDirectory
        ChangeWorkingDirectory = CommandPacketType.MCSStorage.ChangeWorkingDirectory

        FileTransferRequest = CommandPacketType.MCSStorage.FileTransferRequest
        FileTransferAllRequest = CommandPacketType.MCSStorage.FileTransferAllRequest
        FileTransfer = CommandPacketType.MCSStorage.FileTransfer

        DeleteFile = CommandPacketType.MCSStorage.DeleteFile
        RenameFile = CommandPacketType.MCSStorage.RenameFile
        CopyFile = CommandPacketType.MCSStorage.CopyFile

        CapacityTransmitRequest = CommandPacketType.MCSStorage.CapacityTransmitRequest
        CapacityTransmit = CommandPacketType.MCSStorage.CapacityTransmit

        FileInfoTransferAllRequest = CommandPacketType.MCSStorage.FileInfoTransferAllRequest
        FileInfoTransfer = CommandPacketType.MCSStorage.FileInfoTransfer

        RAMImageTransferRequest = CommandPacketType.MCSStorage.RAMImageTransferRequest
        RAMImageTransfer = CommandPacketType.MCSStorage.RAMImageTransfer

        SetupEntryTransferRequest = CommandPacketType.MCSStorage.SetupEntryTransferRequest
        SetupEntryTransfer = CommandPacketType.MCSStorage.SetupEntryTransfer
        SetupEntryTransferAllRequest = CommandPacketType.MCSStorage.SetupEntryTransferAllRequest

    class FlashStorage(Enum):
        CreateDirectory = CommandPacketType.FlashStorage.CreateDirectory
        DeleteDirectory = CommandPacketType.FlashStorage.DeleteDirectory
        RenameDirectory = CommandPacketType.FlashStorage.RenameDirectory
        ChangeWorkingDirectory = CommandPacketType.FlashStorage.ChangeWorkingDirectory

        FileTransferRequest = CommandPacketType.FlashStorage.FileTransferRequest
        FileTransferAllRequest = CommandPacketType.FlashStorage.FileTransferAllRequest
        FileTransfer = CommandPacketType.FlashStorage.FileTransfer

        DeleteFile = CommandPacketType.FlashStorage.DeleteFile
        RenameFile = CommandPacketType.FlashStorage.RenameFile
        CopyFile = CommandPacketType.FlashStorage.CopyFile

        CapacityTransmitRequest = CommandPacketType.FlashStorage.CapacityTransmitRequest
        CapacityTransmit = CommandPacketType.FlashStorage.CapacityTransmit

        FileInfoTransferAllRequest = CommandPacketType.FlashStorage.FileInfoTransferAllRequest
        FileInfoTransfer = CommandPacketType.FlashStorage.FileInfoTransfer

        FlashImageTransferRequest = CommandPacketType.FlashStorage.FlashImageTransferRequest
        FlashImageTransfer = CommandPacketType.FlashStorage.FlashImageTransfer

        OptimizeFileSystem = CommandPacketType.FlashStorage.OptimizeFileSystem


class RoleswapPacketType(Enum):
    Default = "00"


class CheckPacketType(Enum):
    InitConnection = "00"
    CheckConnection = "01"


class AckPacketType(Enum):
    Default = "00"
    YesOverwriteReply = "01"
    ExtendedAck = "03"


class ErrorPacketType(Enum):
    Default = "00"
    ResendRequest = "01"
    Overwrite = "02"
    NoOverwriteReply = "03"
    OverwriteImpossible = "04"
    MemoryFull = "05"


class TerminatePacketType(Enum):
    Default = "00"
    UserRequest = "01"
    Timeout = "02"
    Overwrite = "03"
