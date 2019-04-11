#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 18:56:02 2019

@author: gabriel
"""
from PacketManager import PacketManager
from Packets import *
from ReceivedPacket import ReceivedPacket

history = []

manager = PacketManager()
packet = ReceivedPacket()


def get_packet():
    manager >> packet
    print(packet)
    history.append(ReceivedPacket.from_bytes(bytes(packet)))


def send_packet(pack):
    history.append(ReceivedPacket.from_bytes(bytes(pack)))
    manager << pack


send_packet(CheckPacket.init())
get_packet()

# magic_packet = b"\x0108100190030000000000000000000012E7"
# send_packet(magic_packet)
# get_packet()
#
# send_packet(CheckPacket.check())
# get_packet()
#
# get_info = CommandPacket()
# get_info.packet_subtype = CommandSubType.GetInfo
# send_packet(get_info)
# get_packet()

com = CommandPacket()
com.packet_subtype = CommandSubType.MCSFileTransferRequest
com.overwrite = OverwriteMode.AskUser
com.data_type = b"01"
com.file_size = 0
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
    get_packet()

# manager << CheckPacket.init()
# manager >> packet
# history.append(bytes(packet))
# print(packet)
#
# com = CommandPacket()
# com.packet_subtype = CommandSubType.MCSSetupEntryTransferAllRequest
#
# manager << com
# manager >> packet
# history.append(bytes(packet))
# print(packet)
#
# manager << RoleswapPacket()
#
# go_packet = ReceivedPacket()
# manager >> packet  # DataPacket n° ?
#
# while packet.packet_type is not PacketType.Roleswap:
#     if packet.command_packet().data2 == b"ATTRACT":
#         go_packet = ReceivedPacket.from_bytes(bytes(packet)).command_packet()
#     print(packet)
#     history.append(bytes(packet))
#     manager << AckPacket.default()
#     manager >> packet  # DataPacket n° ?
#
# com = CommandPacket()
# com.packet_subtype = CommandSubType.MCSFileTransfer
# com.data_type = go_packet.data_type
# com.file_size = go_packet.file_size
# com.data1 = go_packet.data1
# com.data2 = go_packet.data2
# com.data3 = go_packet.data3
# print(com)
#
# manager << com
# manager >> packet
# history.append(bytes(packet))
# print(packet)
#
# manager << RoleswapPacket()
# manager >> packet  # DataPacket n° ?
#
# while packet.packet_type is not PacketType.Roleswap:
#     print(packet)
#     history.append(bytes(packet))
#     manager << AckPacket.default()
#     manager >> packet  # DataPacket n° ?
#
#
# manager << TerminatePacket.default()