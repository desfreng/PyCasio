#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from PacketManager import PacketManager
from Packets import *
from ReceivedPacket import ReceivedPacket

manager = PacketManager()
packet = ReceivedPacket()

manager << CheckPacket.init()

while True:
    manager >> packet
    print("[{}] Received : {}".format(datetime.now().strftime("%H:%M:%S.%f"), packet))

print("Ok")