#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 17:29:14 2019

@author: Gabriel Desfrene <desfrene.gabriel@gmail.com>
"""
import usb1

from ReceivedPacket import ReceivedPacket
from Utils import BasePacket

class PacketManager:
    def __init__(self, id_vendor=0x07cf, id_product=0x6101):
        self._context = usb1.USBContext()
        self._handle = self._context.openByVendorIDAndProductID(
            id_vendor, id_product)

        if self._handle is None:
            raise ConnectionError("Unable to find Calculator")

    def __del__(self):
        if self._handle is not None:
            self._handle.close()
        self._context.close()

    def __lshift__(self, other):
        self.send_packet(other)

    def __rshift__(self, other):
        if not isinstance(other, ReceivedPacket):
            raise TypeError("ReceivedPacket expected as argument")

        other.import_bytes(self._get_bytes())

    def receive_packet(self) -> BasePacket:
        return ReceivedPacket.from_bytes(self._get_bytes())

    def send_packet(self, packet: BasePacket):
        if not isinstance(packet, (BasePacket, bytes, bytearray)):
            raise TypeError("BasePacket instance expected as argument")

        if isinstance(packet, (bytearray, bytes)):
            self._handle.bulkWrite(0x01, packet)
        else:
            self._handle.bulkWrite(0x01, bytes(packet))

    def _get_bytes(self) -> bytes:
        buffer = bytearray()

        while len(buffer) == 0:
            buffer = self._handle.bulkRead(0x82, 4096)

        return buffer
