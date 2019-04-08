#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Packets.BasePacket import BasePacket
from Utils import *


class RoleswapPacket(BasePacket):
    def __init__(self, can_be_send : bool = True):
        super().__init__(PacketType.Roleswap, RoleswapSubType.Default, can_be_send=can_be_send)

    @classmethod
    def from_data(cls, packet_subtype, packet_data):
        return cls(False)

    def __repr__(self):
        return "RoleswapPacket at {}".format(hex(id(self)))
