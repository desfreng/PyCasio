#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Packets.BasePacket import BasePacket
from Utils import *


class RoleswapPacket(BasePacket):
    def __init__(self):
        super().__init__(PacketType.Roleswap, RoleswapSubType.Default)

    @classmethod
    def from_data(cls, packet_subtype, packet_data):
        return cls()

    def __repr__(self):
        return "RoleswapPacket at {}".format(hex(id(self)))
