#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Packets.BasePacket import BasePacket
from Utils import *


class TerminatePacket(BasePacket):
    def __init__(self, terminate_type: TerminateSubType = PacketSubType.Unknown, can_be_send : bool = True):
        if not isinstance(terminate_type, (TerminateSubType, PacketSubType)):
            raise TypeError

        super().__init__(PacketType.Terminate, terminate_type, can_be_sent=can_be_send)


    @classmethod
    def from_data(cls, packet_subtype, packet_data):
        if not isinstance(packet_subtype, (bytes, bytearray)):
            raise TypeError

        for subtype in TerminateSubType:
            if subtype.value == packet_subtype:
                return cls(subtype, False)
        return None

    def __repr__(self):
        return "TerminatePacket [Type : {}] at {}".format(self.packet_subtype.name, hex(id(self)))

    @classmethod
    def default(cls):
        return cls(TerminateSubType.Default)

    @classmethod
    def user_request(cls):
        return cls(TerminateSubType.UserRequest)

    @classmethod
    def timeout(cls):
        return cls(TerminateSubType.Timeout)

    @classmethod
    def on_overwrite(cls):
        return cls(TerminateSubType.Overwrite)
