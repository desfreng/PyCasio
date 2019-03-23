#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ctypes import c_ubyte

_HEXADECIMAL_ARRAY = bytearray("0123456789ABCDEF", "ascii")

_HEXADECIMAL_VALUE = {48: 0, 49: 1, 50: 2, 51: 3, 52: 4, 53: 5, 54: 6, 55: 7,
                      56: 8, 57: 9, 65: 10, 66: 11, 67: 12, 68: 13, 69: 14,
                      70: 15}


def to_hexadecimal(number: int, field_size: int = 2) -> bytearray:
    output_array = bytearray()

    while number != 0:
        output_array.insert(0, _HEXADECIMAL_ARRAY[number % 16])
        number //= 16

    while len(output_array) < field_size:
        output_array.insert(0, _HEXADECIMAL_ARRAY[0])

    return output_array


def to_integer(number: bytearray) -> int:
    output_number = 0
    number_index = len(number)

    for part in number:
        number_index -= 1
        output_number += _HEXADECIMAL_VALUE[part] * 16 ** number_index

    return output_number


class BasePacket:
    def __init__(self):
        self._type = 0x0
        self._sub_type = "00"
        self._is_extended = False
        self._data = None

        self._buffer = bytearray()

    def compute_checksum(self):
        self._update_buffer()

        checksum = c_ubyte(0)
        for i in self._buffer[1:]:
            checksum.value += i

        checksum.value = ~checksum.value + 1
        self._data += to_hexadecimal(checksum.value)

    def _update_buffer(self):
        self._buffer.clear()

        self._buffer.append(self._type)
        # TODO : Check This
        self._buffer += bytearray(self._sub_type[0:2], "ascii")

        if self._is_extended:
            self._buffer += b"1"
            self._buffer += to_hexadecimal(len(self._data), 4)
            self._buffer += self._data
        else:
            self._buffer += b"0"

    def is_ready_to_send(self) -> bool:
        if self._is_extended:
            # TODO : Check This
            return len(self._data) == 6 + to_integer(self._data[4:8])
        else:
            return len(self._data) == 6
