#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Packets.BasePacket import BasePacket
from Utils import *


class CheckPacket(BasePacket):
    def __init__(self, check_type: CheckSubType = PacketSubType.Unknown, can_be_send : bool = True):
        if not isinstance(check_type, (CheckSubType, PacketSubType)):
            raise TypeError

        super().__init__(PacketType.Check, check_type, can_be_sent=can_be_send)

    @classmethod
    def from_data(cls, packet_subtype, packet_data):
        if not isinstance(packet_subtype, (bytes, bytearray)):
            raise TypeError

        if packet_subtype == CheckSubType.CheckConnection.value:
            return cls(CheckSubType.CheckConnection, False)
        elif packet_subtype == CheckSubType.InitConnection.value:
            return cls(CheckSubType.InitConnection, False)
        else:
            return None

    def __repr__(self):
        return "CheckPacket [Type : {}] at {}".format(self.packet_subtype.name, hex(id(self)))

    @classmethod
    def init(cls):
        return cls(CheckSubType.InitConnection)

    @classmethod
    def check(cls):
        return cls(CheckSubType.CheckConnection)
