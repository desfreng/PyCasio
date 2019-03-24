#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Packets import Enums


class Private:
    _HEXADECIMAL_ARRAY = bytearray("0123456789ABCDEF", "ascii")

    @staticmethod
    def to_hexadecimal(number: int, field_size: int = 2) -> bytearray:
        output_array = bytearray()

        while number != 0:
            output_array.insert(0, Private._HEXADECIMAL_ARRAY[number % 16])
            number //= 16

        while len(output_array) < field_size:
            output_array.insert(0, Private._HEXADECIMAL_ARRAY[0])

        return output_array

    @staticmethod
    def to_integer(number: bytearray) -> int:
        output_number = 0
        number_index = len(number)

        for part in number:
            number_index -= 1
            # Séparation entre les lettres et les chiffres du code Hex
            if part > Private._HEXADECIMAL_ARRAY[9]:
                # Les lettres A-F sont codés en uint8 entre 65 et 70
                output_number += (part - Private._HEXADECIMAL_ARRAY[10] + 10) * 16 ** number_index
            else:
                # Les chiffres 0-9 sont codés en uint8 entre 48 et 57
                output_number += (part - Private._HEXADECIMAL_ARRAY[0]) * 16 ** number_index
        return output_number


class BasePacket:
    def __init__(self):
        self._type = Enums.PacketType.Unknown
        self._sub_type = Enums.PacketSubType.Default
        self._data = bytearray()
        self._buffer = bytearray()

    @property
    def extended(self) -> bool:
        return len(self._data) != 0

    @property
    def packet_type(self) -> Enums.PacketType:
        return self._type

    @property
    def packet_subtype(self) -> Enums.PacketSubType:
        return self._sub_type

    @property
    def checksum(self) -> int:
        self.compute_checksum()
        return Private.to_integer(self._buffer[-2:])

    @property
    def data(self) -> bytes:
        return bytes(self._data)

    def compute_checksum(self):
        self._buffer.clear()

        self._buffer.append(self._type.value)
        self._buffer += self._sub_type.value

        if self.extended:
            self._buffer += b"1"
            self._buffer += Private.to_hexadecimal(len(self._data), 4)
            self._buffer += self._data
        else:
            self._buffer += b"0"

        checksum = 0
        for i in self._buffer[1:]:
            checksum += i

        checksum = ~checksum + 1
        checksum %= 256

        self._buffer += Private.to_hexadecimal(checksum)

    def is_ready_to_send(self) -> bool:
        if self.extended:
            return len(self._buffer) == 10 + Private.to_integer(self._buffer[4:8])
        else:
            return len(self._buffer) == 6

    def __repr__(self):
        self.compute_checksum()
        if self.extended:
            return "Type : {:#02x}, Subtype : {}, Extended : True, Data : {}, Checksum : {}".format(
                self._type.value, self._sub_type.value.decode("ascii"), self._data, self._buffer[-2:].decode("ascii"))
        else:
            return "Type : {:#02x}, Subtype : {}, Extended : False, Checksum : {}".format(
                self._type.value, self._sub_type.value.decode("ascii"), self._buffer[-2:].decode("ascii"))

    def __bytes__(self):
        self.compute_checksum()
        return bytes(self._buffer)

    def _set_type(self, packet_type: Enums.PacketType):
        if not isinstance(packet_type, Enums.PacketType):
            raise TypeError

        self._type = packet_type.value

    def _set_subtype(self, packet_subtype: Enums.PacketSubType):
        if not isinstance(packet_subtype, Enums.PacketSubType):
            raise TypeError

        self._sub_type = packet_subtype
