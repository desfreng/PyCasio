#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Packets.BasePacket import BasePacket
from Utils import *


class ErrorPacket(BasePacket):
    def __init__(self, error_type: ErrorSubType = PacketSubType.Unknown):
        if not isinstance(error_type, (ErrorSubType, PacketSubType)):
            raise TypeError

        super().__init__(PacketType.Error, error_type)

    @classmethod
    def from_data(cls, packet_subtype, packet_data):
        if not isinstance(packet_subtype, (bytes, bytearray)):
            raise TypeError

        for subtype in ErrorSubType:
            if subtype.value == packet_subtype:
                return cls(subtype)
        return None

    def __repr__(self):
        return "ErrorPacket [Type : {}] at {}".format(self.packet_subtype.name, hex(id(self)))

    @classmethod
    def default(cls):
        return cls(ErrorSubType.Default)

    @classmethod
    def resend_request(cls):
        return cls(ErrorSubType.ResendRequest)

    @classmethod
    def overwrite_error(cls):
        return cls(ErrorSubType.OverwriteError)

    @classmethod
    def no_overwrite_reply(cls):
        return cls(ErrorSubType.NoOverwriteReply)

    @classmethod
    def overwrite_impossible(cls):
        return cls(ErrorSubType.OverwriteImpossible)

    @classmethod
    def memory_full(cls):
        return cls(ErrorSubType.MemoryFull)
