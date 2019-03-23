#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ctypes
import time

import usb1

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


def compute_checksum(packet) -> int:
    if not isinstance(packet, bytearray):
        return -1

    check_sum = ctypes.c_ubyte(0)
    for i in packet[1:]:
        check_sum.value += i

    check_sum.value = ~check_sum.value + 1
    return check_sum.value


def make_packet(request_type, data):
    if not isinstance(data, bytearray):
        return None

    packet = bytearray()
    packet.insert(1, request_type)
    packet += data
    packet += to_hexadecimal(compute_checksum(packet))
    return packet


with usb1.USBContext() as context:
    calculatrice = context.openByVendorIDAndProductID(0x07cf, 0x6101)

    if calculatrice is None:
        print("Erreur ! Calculatrice introuvable !")
        exit(1)

    print("Calculatrice Détectée")

    calculatrice.bulkWrite(0x01, make_packet(0x05, bytearray("000", "ascii")))
    calculatrice.bulkWrite(0x01, make_packet(0x03, bytearray("000", "ascii")))

    try:
        while True:
            temp = calculatrice.bulkRead(0x82, 1024)
            if len(temp) != 0:
                print("[{}] Received : {:#002x}".format(
                    time.strftime("%H:%M:%S"), temp[0]))

                temp = temp[1:]
                print(temp.decode("ascii", "backslashreplace"))
                print()
    except KeyboardInterrupt:
        print("Quit Application")
        calculatrice.bulkWrite(0x01, make_packet(0x18, bytearray("000", "ascii")))
