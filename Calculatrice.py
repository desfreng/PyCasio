#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PacketManager import PacketManager
from Utils import Devices, PacketType
from Packets import AckPacket, CheckPacket, CommandPacket, DataPacket, ErrorPacket, RoleswapPacket, TerminatePacket
from ReceivedPacket import ReceivedPacket
from Nodes import DirectoryNode, FileNode
from copy import copy


class Calculator:
    def __init__(self, cal_mode: Devices = Devices.MCS):
        if not isinstance(cal_mode, Devices):
            raise TypeError

        self.mode = cal_mode
        self._root = DirectoryNode("Root")

        self._m = PacketManager()
        self._is_passive_side = False

        self._history = []
        self._rp = ReceivedPacket()

        self._send_packet(CheckPacket.init())
        self._get_packet()

        if not self._rp.packet_type == PacketType.Ack:
            pass

    def _get_packet(self):
        self >> self._rp
        self._history.append(copy(self._rp))

    def _send_packet(self, packet):
        self._history.append(copy(packet))
        self << packet

    def copy_file(self, origin, new):
        pass

    def delete_file(self, file):
        pass

    def rename_file(self, file, new_name):
        pass

    def get_file_data(self, file):
        pass

    def send_file_from_buffer(self, buffer):
        pass

    def send_file(self, path):
        pass

    def optimize(self):
        pass

    def rename_directory(self, directory, new_name):
        pass

    def delete_directory(self, directory):
        pass

    def create_directory(self, directory):
        pass

    @property
    def capacity(self):
        pass

    @property
    def file_system(self):
        pass

    def find_file(self, name, recursive=False):
        pass

    def __iter__(self):
        pass

    def print_files(self):
        pass

    def file_list(self):
        pass

    def __getitem__(self, item):
        pass

    def __getattr__(self, item):
        pass

    def __delitem__(self, key):
        pass

    def __delattr__(self, item):
        pass
