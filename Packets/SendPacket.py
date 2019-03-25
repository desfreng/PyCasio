#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Packets.BasePacket import BasePacket


class SendPacket(BasePacket):
    def __init__(self):
        super().__init__()
        self._can_be_send = True

    def _disable_send(self):
        self._can_be_send = False

    def _enable_send(self):
        self._can_be_send = True
