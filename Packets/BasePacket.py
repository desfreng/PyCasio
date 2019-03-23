#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 17:29:28 2019

@author: Gabriel Desfrene <desfrene.gabriel@gmail.com>
"""
import PacketEnums


class BasePacket:
    def __init__(self):
        self._type = PacketEnums.PacketType.Unknown
        self._subType = PacketEnums.UnknownPacketType.Unknown
        self._extended = False
        self._dataSize = None
        self._data = bytearray()
        self._checkSum = None

    @property
    def packet_type(self):
        return self._type
