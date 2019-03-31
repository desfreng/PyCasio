#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC

from Utils import *


class BasePacket(ABC):
    def __init__(self, packet_type=PacketType.Unknown, packet_subtype=PacketSubType.Unknown, packet_data=bytearray()):
        if not isinstance(packet_type, PacketType):
            raise TypeError
        if not isinstance(packet_subtype, SubTypes):
            raise TypeError
        if not isinstance(packet_data, (bytearray, bytes)):
            raise TypeError

        self._type = packet_type
        self._sub_type = packet_subtype
        self._data = bytearray(packet_data)
        self._buffer = bytearray()
        self._checksum = 0
        self._can_be_send = True

    @property
    def extended(self) -> bool:
        return len(self._data) != 0

    @property
    def packet_type(self) -> PacketType:
        return self._type

    @property
    def packet_subtype(self) -> PacketSubType:
        return self._sub_type

    @property
    def checksum(self) -> int:
        self.compute_checksum()
        return self._checksum

    @property
    def data(self) -> bytes:
        return bytes(self._data)

    @property
    def valid(self) -> bool:
        if self.extended:
            return len(self._buffer) == 10 + to_integer(self._buffer[4:8]) and \
                   self._type is not PacketType.Unknown
        else:
            return len(self._buffer) == 6 and \
                   self._type is not PacketType.Unknown

    @property
    def ready(self) -> bool:
        return self._can_be_send and self.valid

    def disable_send(self):
        self._can_be_send = False

    def enable_send(self):
        self._can_be_send = True

    def compute_checksum(self):
        self._buffer.clear()

        self._buffer.append(self._type.value)
        self._buffer += self._sub_type.value

        if self.extended:
            self._buffer += b"1"
            self._buffer += to_hexadecimal(len(self._data), 4)
            self._buffer += self._data
        else:
            self._buffer += b"0"

        checksum = 0
        for i in self._buffer[1:]:
            checksum += i

        checksum = ~checksum + 1
        checksum %= 256

        self._checksum = checksum
        self._buffer += to_hexadecimal(checksum)

    @classmethod
    # @abstractmethod
    def from_data(cls, packet_subtype, packet_data):
        pass

    def __repr__(self):
        self.compute_checksum()
        if self.extended:
            return "[BasePacket] Type : {:#02x}, Subtype : {}, Extended : True, Data : {}, Checksum : {}".format(
                self._type.value, self._sub_type.value.decode("ascii"), self._data, self._buffer[-2:].decode("ascii"))
        else:
            return "[BasePacket] Type : {:#02x}, Subtype : {}, Extended : False, Checksum : {}".format(
                self._type.value, self._sub_type.value.decode("ascii"), self._buffer[-2:].decode("ascii"))

    def __bytes__(self):
        self.compute_checksum()
        return bytes(self._buffer)
