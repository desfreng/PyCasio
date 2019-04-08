#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Packets.BasePacket import BasePacket
from Utils import *


class AckPacket(BasePacket):
    def __init__(self, ack_type: AckSubType = AckSubType.Default, ack_data=bytearray(), can_be_send : bool = True):
        if not isinstance(ack_type, (AckSubType, PacketSubType)):
            raise TypeError
        if not isinstance(ack_data, (bytearray, bytes)):
            raise TypeError

        super().__init__(PacketType.Ack, ack_type, ack_data, can_be_send)

        if ack_type is AckSubType.ExtendedAck:
            self._hardware = ack_data[0:8].replace(b"\xff", b"").decode("ascii")
            self._processor = ack_data[8:24].replace(b"\xff", b"").decode("ascii")

            self._rom_capacity = to_integer(ack_data[24:32].replace(b"\xff", b""))
            self._flash_rom_capacity = to_integer(ack_data[32:40].replace(b"\xff", b""))
            self._ram_capacity = to_integer(ack_data[40:48].replace(b"\xff", b""))

            self._rom_version = ack_data[48:64].replace(b"\xff", b"").decode("ascii")

            self._boot_code_version = ack_data[64:80].replace(b"\xff", b"").decode("ascii")
            self._boot_code_offset = to_integer(ack_data[80:88].replace(b"\xff", b""))
            self._boot_code_size = to_integer(ack_data[88:96].replace(b"\xff", b""))

            self._os_code_version = ack_data[96:112].replace(b"\xff", b"").decode("ascii")
            self._os_code_offset = to_integer(ack_data[112:120].replace(b"\xff", b""))
            self._os_code_size = to_integer(ack_data[120:128].replace(b"\xff", b""))

            self._protocol_version = ack_data[128:132].replace(b"\xff", b"").decode("ascii")
            self._product_id = ack_data[132:148].replace(b"\xff", b"").decode("ascii")
            self._user_name = ack_data[148:164].replace(b"\xff", b"").decode("ascii", "ignore")

    @property
    def hardware(self) -> str:
        if self.packet_subtype is not AckSubType.ExtendedAck:
            return
        return self._hardware

    @property
    def processor(self) -> str:
        if self.packet_subtype is not AckSubType.ExtendedAck:
            return
        return self._processor

    @property
    def rom_capacity(self) -> int:
        if self.packet_subtype is not AckSubType.ExtendedAck:
            return
        return self._rom_capacity

    @property
    def flash_rom_capacity(self) -> int:
        if self.packet_subtype is not AckSubType.ExtendedAck:
            return
        return self._flash_rom_capacity

    @property
    def ram_capacity(self) -> int:
        if self.packet_subtype is not AckSubType.ExtendedAck:
            return
        return self._ram_capacity

    @property
    def rom_version(self) -> str:
        if self.packet_subtype is not AckSubType.ExtendedAck:
            return
        return self._rom_version

    @property
    def boot_code_version(self) -> str:
        if self.packet_subtype is not AckSubType.ExtendedAck:
            return
        return self._boot_code_version

    @property
    def boot_code_offset(self) -> int:
        if self.packet_subtype is not AckSubType.ExtendedAck:
            return
        return self._boot_code_offset

    @property
    def boot_code_size(self) -> int:
        if self.packet_subtype is not AckSubType.ExtendedAck:
            return
        return self._boot_code_size

    @property
    def os_code_version(self) -> str:
        if self.packet_subtype is not AckSubType.ExtendedAck:
            return
        return self._os_code_version

    @property
    def os_code_offset(self) -> int:
        if self.packet_subtype is not AckSubType.ExtendedAck:
            return
        return self._os_code_offset

    @property
    def os_code_size(self) -> int:
        if self.packet_subtype is not AckSubType.ExtendedAck:
            return
        return self._os_code_size

    @property
    def protocol_version(self) -> str:
        if self.packet_subtype is not AckSubType.ExtendedAck:
            return
        return self._protocol_version

    @property
    def product_id(self) -> str:
        if self.packet_subtype is not AckSubType.ExtendedAck:
            return
        return self._product_id

    @property
    def user_name(self) -> str:
        if self.packet_subtype is not AckSubType.ExtendedAck:
            return
        return self._user_name

    @classmethod
    def from_data(cls, packet_subtype, packet_data):
        if not isinstance(packet_subtype, (bytearray, bytes)):
            raise TypeError
        if not isinstance(packet_data, (bytearray, bytes)):
            raise TypeError

        if packet_subtype == AckSubType.Default.value:
            return cls(AckSubType.Default, can_be_send=False)

        elif packet_subtype == AckSubType.YesOverwriteReply.value:
            return cls(AckSubType.YesOverwriteReply, can_be_send=False)

        elif packet_subtype == AckSubType.ExtendedAck.value:
            return cls(AckSubType.ExtendedAck, packet_data, can_be_send=False)

        else:
            return None

    def __repr__(self):
        if self.packet_subtype is AckSubType.ExtendedAck:
            return "Extended AckPacket at  {}\n" \
                   "--------------- Data : ---------------" \
                   "Hardware :           {}\n" \
                   "Processor :          {}\n" \
                   "ROM Capacity :       {}\n" \
                   "Flash ROM Capacity : {}\n" \
                   "RAM Capacity :       {}\n" \
                   "ROM Version :        {}\n" \
                   "Boot Code Version :  {}\n" \
                   "Boot Code Offset :   {}\n" \
                   "Boot Code Size :     {}\n" \
                   "OS Code Version :    {}\n" \
                   "OS Code Offset :     {}\n" \
                   "OS Code Size :       {}\n" \
                   "Protocol Version :   {}\n" \
                   "Product ID :         {}\n" \
                   "User Name :          {}\n" \
                   "--------------------------------------"\
                .format(hex(id(self)), self.hardware, self.processor, self.rom_capacity,self.flash_rom_capacity,
                        self.ram_capacity, self.rom_capacity, self.boot_code_version, self.boot_code_offset,
                        self.boot_code_size, self.os_code_version, self.os_code_offset, self.os_code_size,
                        self.protocol_version, self.product_id, self.user_name)
        else:
            return "AckPacket [Type : {}] at {}".format(self.packet_subtype.name, hex(id(self)))

    @classmethod
    def yes_overwrite(cls):
        return cls(AckSubType.YesOverwriteReply)

    @classmethod
    def default(cls):
        return cls(AckSubType.Default)
