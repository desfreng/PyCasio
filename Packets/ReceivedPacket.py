#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Packets.AckPacket import AckPacket
from Packets.CheckPacket import CheckPacket
from Packets.CommandPacket import CommandPacket
from Packets.DataPacket import DataPacket
from Packets.ErrorPacket import ErrorPacket
from Packets.RoleswapPacket import RoleswapPacket
from Packets.TerminatePacket import TerminatePacket
from Utils import *


class ReceivedPacket:
    def __init__(self):
        self._type = PacketType.Unknown
        self._bytes_received = bytes()

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

    def from_bytes(self, array: bytes):
        if not isinstance(array, (bytes, bytearray)):
            raise TypeError

        self._bytes_received = array

        if self.corrupt_data(self._bytes_received):
            self._bytes_received = None
            raise BaseException("Corrupt Data !")

        for p_type in PacketType:
            if p_type.value == array[0]:
                self._type = p_type
                break

    def __repr__(self) -> str:
        return "[BasePacket] Type : {:#02x}, SubType : {}, Data : {}, Checksum : {}, Corrupt : {}".format(
            self.packet_type.value, self.packet_subtype.decode("ascii"), self.packet_data_received, self._bytes_received[-2:].decode("ascii"),
            self.corrupt)

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
