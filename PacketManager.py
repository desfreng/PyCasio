#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 17:29:14 2019

@author: Gabriel Desfrene <desfrene.gabriel@gmail.com>
"""
import usb1

from Packets.BasePacket import BasePacket


class PacketManager:
    def __init__(self, id_vendor=0x07cf, id_product=0x6101):
        self._context = usb1.USBContext()
        self._handle = self._context.openByVendorIDAndProductID(
            id_vendor, id_product)

        if self._handle is None:
            raise ConnectionError("Unable to find Calculator")

    def __del__(self):
        self._handle.close()
        self._context.close()

    def __lshift__(self, other):
        if isinstance(other, BasePacket):
            raise TypeError("Casio Packet Expected as argument")

        self.send_packet(other)

    def __rshift__(self, other):
        if isinstance(other, BasePacket):
            raise TypeError("Casio Packet Expected as argument")

        other = self.receive_packet()

    def receive_packet(self) -> BasePacket:
        pass

    #     outputPacket = BasePacket()
    #     outputPacket.fromByteArray(self._handle.bulkRead(0x82, 4096))
    #     return outputPacket
    #

    def send_packet(self, packet: BasePacket):
        pass
    #     if isinstance(packet, BasePacket):
    #         raise TypeError("Casio Packet Expected as argument")
    #
    #     self._handle.bulkWrite(0x01, packet.toByteArray())
