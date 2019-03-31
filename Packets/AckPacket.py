#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Packets.BasePacket import BasePacket
from Utils import *


class AckPacket(BasePacket):
    def __init__(self, ack_type: AckSubType = AckSubType.Default, ack_data=bytearray()):
        if not isinstance(ack_type, (AckSubType, PacketSubType)):
            raise TypeError
        if not isinstance(ack_data, (bytearray, bytes)):
            raise TypeError

        super().__init__(PacketType.Check, ack_type, ack_data)

    @classmethod
    def from_data(cls, packet_subtype, packet_data):
        if not isinstance(packet_subtype, (bytearray, bytes)):
            raise TypeError
        if not isinstance(packet_data, (bytearray, bytes)):
            raise TypeError

        if packet_subtype == AckSubType.Default.value:
            return cls(AckSubType.Default)

        elif packet_subtype == AckSubType.YesOverwriteReply.value:
            return cls(AckSubType.YesOverwriteReply)

        elif packet_subtype == AckSubType.ExtendedAck.value:
            return cls(AckSubType.ExtendedAck, packet_data)

        else:
            return None

    def __repr__(self):
        return "AckPacket [Type : {}] at {}".format(self.packet_subtype.name, hex(id(self)))
