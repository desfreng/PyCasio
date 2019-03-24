#!/usr/bin/env python3
# -*- coding: utf-8 -*-


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
    def _init__(self):
        self._type = 0x0
        self._sub_type = "00"
        self._is_extended = False
        self._data = None

        self._buffer = bytearray()

    def compute_checksum(self):
        self._update_buffer()

        checksum = 0
        for i in self._buffer[1:]:
            checksum += i

        checksum = ~checksum + 1
        checksum %= 256

        self._data += Private.to_hexadecimal(checksum)

    def _update_buffer(self):
        self._buffer.clear()

        self._buffer.append(self._type)
        # TODO : Check This
        self._buffer += bytearray(self._sub_type[0:2], "ascii")

        if self._is_extended:
            self._buffer += b"1"
            self._buffer += Private.to_hexadecimal(len(self._data), 4)
            self._buffer += self._data
        else:
            self._buffer += b"0"

    def is_ready_to_send(self) -> bool:
        if self._is_extended:
            # TODO : Check This
            return len(self._data) == 6 + Private.to_integer(self._data[4:8])
        else:
            return len(self._data) == 6
