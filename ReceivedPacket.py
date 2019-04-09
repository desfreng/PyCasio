#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Packets import *
from Utils import *


class ReceivedPacket:
    def __init__(self, type: PacketType = PacketType.Unknown, data_received: bytes = bytes()):
        if not isinstance(type, PacketType):
            raise TypeError

        if not isinstance(data_received, (bytes, bytearray)):
            raise TypeError

        self._type = type
        self._bytes_received = data_received

    @property
    def packet_type(self) -> PacketType:
        return self._type

    @property
    def packet_subtype(self) -> bytes:
        return self._bytes_received[1:3]

    @property
    def packet_data_received(self) -> bytes:
        if self._bytes_received[3:4] == b"1":
            return bytes(self._bytes_received[8:8 + to_integer(self._bytes_received[4:8])])
        return bytes()

    @property
    def corrupt(self) -> bool:
        return self.corrupt_data(self._bytes_received)

    @staticmethod
    def corrupt_data(data: bytes) -> bool:
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError

        new_checksum = 0
        old_checksum = to_integer(data[-2:])

        for i in data[1:-2]:
            new_checksum += i

        new_checksum = ~new_checksum + 1
        new_checksum %= 256

        return new_checksum != old_checksum

    @classmethod
    def from_bytes(cls, array: bytes):
        if not isinstance(array, (bytes, bytearray)):
            raise TypeError

        if ReceivedPacket.corrupt_data(array):
            raise BaseException("Corrupt Data !")

        p_type = PacketType.Unknown
        for a in PacketType:
            if a.value == array[0]:
                p_type = a
                break

        return cls(p_type, array)

    def import_bytes(self, array: bytes):
        if not isinstance(array, (bytes, bytearray)):
            raise TypeError

        if self.corrupt_data(array):
            raise BaseException("Corrupt Data !")

        p_type = PacketType.Unknown
        for a in PacketType:
            if a.value == array[0]:
                p_type = a
                break

        self._type = p_type
        self._bytes_received = array

    def __repr__(self) -> str:
        if self.packet_type is PacketType.Ack:
            return "(From ReceivedPacket [Status : {}]) {}".format("Corrupt" if self.corrupt else "Ok",
                                                                   self.ack_packet())

        elif self.packet_type is PacketType.Check:
            return "(From ReceivedPacket [Status : {}]) {}".format("Corrupt" if self.corrupt else "Ok",
                                                                   self.check_packet())

        elif self.packet_type is PacketType.Error:
            return "(From ReceivedPacket [Status : {}]) {}".format("Corrupt" if self.corrupt else "Ok",
                                                                   self.error_packet())

        elif self.packet_type is PacketType.Terminate:
            return "(From ReceivedPacket [Status : {}]) {}".format("Corrupt" if self.corrupt else "Ok",
                                                                   self.terminate_packet())

        elif self.packet_type is PacketType.Roleswap:
            return "(From ReceivedPacket [Status : {}]) {}".format("Corrupt" if self.corrupt else "Ok",
                                                                   self.roleswap_packet())

        elif self.packet_type is PacketType.Data:
            return "(From ReceivedPacket [Status : {}]) {}".format("Corrupt" if self.corrupt else "Ok",
                                                                   self.data_packet())

        elif self.packet_type is PacketType.Command:
            return "(From ReceivedPacket [Status : {}]) {}".format("Corrupt" if self.corrupt else "Ok",
                                                                   self.command_packet())

        else:
            return "[ReceivedPacket] Type : {:#02x}, SubType : {}, Data : {}, Checksum : {}, Corrupt : {}".format(
                self.packet_type.value, self.packet_subtype.decode("ascii"), self.packet_data_received,
                self._bytes_received[-2:].decode("ascii"), self.corrupt)

    def __bytes__(self) -> bytes:
        return bytes(self._bytes_received)

    def command_packet(self) -> CommandPacket:
        return CommandPacket.from_data(self.packet_subtype, self.packet_data_received)

    def data_packet(self) -> DataPacket:
        return DataPacket.from_data(self.packet_subtype, self.packet_data_received)

    def roleswap_packet(self) -> RoleswapPacket:
        return RoleswapPacket.from_data(self.packet_subtype, self.packet_data_received)

    def check_packet(self) -> CheckPacket:
        return CheckPacket.from_data(self.packet_subtype, self.packet_data_received)

    def ack_packet(self) -> AckPacket:
        return AckPacket.from_data(self.packet_subtype, self.packet_data_received)

    def error_packet(self) -> ErrorPacket:
        return ErrorPacket.from_data(self.packet_subtype, self.packet_data_received)

    def terminate_packet(self) -> TerminatePacket:
        return TerminatePacket.from_data(self.packet_subtype, self.packet_data_received)
