#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

import usb1

from Packets.CheckPacket import *
from Packets.ErrorPacket import *
from Packets.ReceivedPacket import *


def send2Calto(calto: usb1.USBDeviceHandle, packet: BasePacket):
    calto.bulkWrite(0x01, bytes(packet))


def receive2Calto(calto: usb1.USBDeviceHandle):
    temp = bytearray()
    while len(temp) is 0:
        temp = calto.bulkRead(0x82, 1024)

    packet = ReceivedPacket()
    packet.from_bytes(temp)
    return packet


with usb1.USBContext() as context:
    calculatrice = context.openByVendorIDAndProductID(0x07cf, 0x6101)

    if calculatrice is None:
        print("Erreur ! Calculatrice introuvable !")
        exit(1)

    print("Calculatrice Détectée")

    send2Calto(calculatrice, CheckPacket.init())
    send2Calto(calculatrice, BasePacket(PacketType.Command, CommandSubType.GetInfo))
    send2Calto(calculatrice, ErrorPacket.resend_request())

    try:
        while True:
            packet = receive2Calto(calculatrice)

            if packet.packet_type is PacketType.Ack:
                print("[{}] Received : {}".format(datetime.now().strftime("%H:%M:%S.%f"), packet.ack_packet()))

            elif packet.packet_type is PacketType.Check:
                print("[{}] Received : {}".format(datetime.now().strftime("%H:%M:%S.%f"), packet.check_packet()))

            elif packet.packet_type is PacketType.Error:
                print("[{}] Received : {}".format(datetime.now().strftime("%H:%M:%S.%f"), packet.error_packet()))

            elif packet.packet_type is PacketType.Terminate:
                print("[{}] Received : {}".format(datetime.now().strftime("%H:%M:%S.%f"), packet.terminate_packet()))

            elif packet.packet_type is PacketType.Roleswap:
                print("[{}] Received : {}".format(datetime.now().strftime("%H:%M:%S.%f"), packet.roleswap_packet()))

            elif packet.packet_type is PacketType.Data:
                print("[{}] Received : {}".format(datetime.now().strftime("%H:%M:%S.%f"), packet.data_packet()))

            elif packet.packet_type is PacketType.Command:
                print("[{}] Received : {}".format(datetime.now().strftime("%H:%M:%S.%f"), packet.command_packet()))

    except KeyboardInterrupt:
        print()
        print("Quit Application")

    finally:
        print("Close Connection")
        send2Calto(calculatrice, TerminatePacket.default())
