#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PacketManager import PacketManager


class Calculatrice:
    def __init__(self):
        self._m = PacketManager()
        self._history = []