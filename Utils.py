#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
