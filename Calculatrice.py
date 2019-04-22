#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PacketManager import PacketManager
from enum import Enum


class CalculatorMode(Enum):
    MCSStorage = Enum.auto()
    FlashStorage = Enum.auto()
    SDCard = Enum.auto()


class Calculator:
    def __init__(self, cal_mode : CalculatorMode = CalculatorMode.MCSStorage):
        if not isinstance(cal_mode, CalculatorMode):
            raise TypeError

        self._m = PacketManager()
        self._history = []
        self.mode = cal_mode

    def list_file(self):
        if self.mode == CalculatorMode.MCSStorage:
            pass
