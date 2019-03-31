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
    def corrupt(self) -> bool:
        return self.corrupt_data(self._bytes_received)

    @property
    def received_data(self) -> bytes:
        return bytes(self._bytes_received)

    @staticmethod
    def corrupt_data(data: bytes) -> bool:
        if not isinstance(data, bytes):
            raise TypeError

        new_checksum = 0
        old_checksum = to_integer(data[-2:])

        for i in data[1:-2]:
            new_checksum += i

        new_checksum = ~new_checksum + 1
        new_checksum %= 256

        return new_checksum != old_checksum

    def from_bytes(self, array: bytes):
        if not isinstance(array, bytes):
            raise TypeError

        self._bytes_received = array

        for p_type in PacketType:
            if p_type.value == array[0]:
                self._type = p_type
                break

    def __repr__(self) -> str:
        return "[BasePacket] Type : {:#02x}, Bytes : {}, Checksum : {}, Corrupt : {}".format(
            self.packet_type.value, self.received_data, self.received_data[-2:].decode("ascii"),
            self.corrupt)

    def __bytes__(self) -> bytes:
        return self.received_data

    def command_packet(self) -> CommandPacket:
        packet = CommandPacket.from_data(self.received_data)
        packet.disable_send()
        return packet

    def data_packet(self) -> DataPacket:
        packet = DataPacket.from_data(self.received_data)
        packet.disable_send()
        return packet

    def roleswap_packet(self) -> RoleswapPacket:
        packet = RoleswapPacket.from_data(self.received_data)
        packet.disable_send()
        return packet

    def check_packet(self) -> CheckPacket:
        packet = CheckPacket.from_data(self.received_data)
        packet.disable_send()
        return packet

    def ack_packet(self) -> AckPacket:
        packet = AckPacket.from_data(self.received_data)
        packet.disable_send()
        return packet

    def error_packet(self) -> ErrorPacket:
        packet = ErrorPacket.from_data(self.received_data)
        packet.disable_send()
        return packet

    def terminate_packet(self) -> TerminatePacket:
        packet = TerminatePacket.from_data(self.received_data)
        packet.disable_send()
        return packet
