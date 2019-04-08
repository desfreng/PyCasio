#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Packets.BasePacket import BasePacket
from Utils import *


class CommandPacket(BasePacket):
    def __init__(self, command_type: CommandSubType = PacketSubType.Unknown, command_data: bytes = bytes(),
                 can_be_send: bool = True):
        if not isinstance(command_type, (ErrorSubType, PacketSubType)):
            raise TypeError
        if not isinstance(command_data, (bytes, bytearray)):
            raise TypeError

        super().__init__(PacketType.Command, command_type, command_data, can_be_sent=can_be_send)

    @classmethod
    def from_data(cls, packet_subtype, packet_data):
        if not isinstance(packet_subtype, (bytes, bytearray)):
            raise TypeError
        if not isinstance(packet_data, (bytes, bytearray)):
            raise TypeError

        for subtype in CommandSubType:
            if subtype.value == packet_subtype:
                return cls(subtype, can_be_send=False)
        return None

    def __repr__(self):
        return "ErrorPacket [Type : {}] at {}".format(self.packet_subtype.name, hex(id(self)))

