#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 18:56:02 2019

@author: gabriel
"""
from PacketManager import PacketManager
from Packets import *
from ReceivedPacket import ReceivedPacket
from Utils import PacketType
from copy import copy

history = []
file = []

manager = PacketManager()
packet = ReceivedPacket()


def get_packet():
    manager >> packet
    # print(packet)
    history.append(copy(packet))


def send_packet(pack):
    history.append(copy(pack))
    manager << pack


send_packet(CheckPacket.init())
get_packet()

com = CommandPacket()
com.packet_subtype = CommandSubType.MCSFileTransferRequest
com.overwrite = OverwriteMode.AskUser
com.data_type = b"01"
com.file_size = 1192
com.data1 = b"system"
com.data2 = b"SNDDEGRE"
com.data3 = b"PROGRAM"
send_packet(com)
get_packet()

send_packet(RoleswapPacket())
get_packet()

send_packet(AckPacket.default())
get_packet()

while packet.packet_type != PacketType.Roleswap:
    send_packet(AckPacket.default())
    if packet.packet_type is PacketType.Data:
        file += packet.data_packet().packet_data
    get_packet()

send_packet(TerminatePacket.default())
print(bytes(file))
