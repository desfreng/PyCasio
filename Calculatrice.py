#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Utils import Devices
from PacketManager import PacketManager


class Calculator:
    def __init__(self, cal_mode: Devices = Devices.MCS):
        if not isinstance(cal_mode, Devices):
            raise TypeError

        self._m = PacketManager()
        self._history = []
        self.mode = cal_mode

    def list_file(self):
        if self.mode == Devices.MCS:
            pass
