#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Packets.BasePacket import BasePacket, Private
from Packets.Enums import PacketType, PacketSubType


class ReceivedPacket(BasePacket):
    def __init__(self):
        super().__init__()
        self._corrupt = False

    def from_bytes(self, array: bytes):
        if not isinstance(array, bytes):
            raise TypeError

        for p_type in PacketType:
            if p_type.value == array[0]:
                self._set_type(p_type)
                break

        if self.packet_type is PacketType.Ack:
            if array[1:2] == PacketSubType.Default:
                self._set_subtype(PacketSubType.Default)
            elif array[1:2] == PacketSubType.YesOverwriteReply:
                self._set_subtype(PacketSubType.YesOverwriteReply)
            elif array[1:2] == PacketSubType.ExtendedAck:
                self._set_subtype(PacketSubType.ExtendedAck)

        elif self.packet_type is PacketType.Check:
            if array[1:2] == PacketSubType.InitConnection:
                self._set_subtype(PacketSubType.InitConnection)
            elif array[1:2] == PacketSubType.CheckConnection:
                self._set_subtype(PacketSubType.CheckConnection)

        elif self.packet_type is PacketType.Roleswap:
            self._set_subtype(PacketSubType.Default)

        elif self.packet_type is PacketType.Error:
            if array[1:2] == PacketSubType.Default:
                self._set_subtype(PacketSubType.Default)
            elif array[1:2] == PacketSubType.ResendRequest:
                self._set_subtype(PacketSubType.ResendRequest)
            elif array[1:2] == PacketSubType.OverwriteError:
                self._set_subtype(PacketSubType.OverwriteError)
            elif array[1:2] == PacketSubType.NoOverwriteReply:
                self._set_subtype(PacketSubType.NoOverwriteReply)
            elif array[1:2] == PacketSubType.OverwriteImpossible:
                self._set_subtype(PacketSubType.OverwriteImpossible)
            elif array[1:2] == PacketSubType.MemoryFull:
                self._set_subtype(PacketSubType.MemoryFull)

        elif self.packet_type is PacketType.Terminate:
            if array[1:2] == PacketSubType.Default:
                self._set_subtype(PacketSubType.Default)
            elif array[1:2] == PacketSubType.UserRequest:
                self._set_subtype(PacketSubType.UserRequest)
            elif array[1:2] == PacketSubType.Timeout:
                self._set_subtype(PacketSubType.Timeout)
            elif array[1:2] == PacketSubType.Overwrite:
                self._set_subtype(PacketSubType.Overwrite)

        elif self.packet_type is PacketType.Command or self.packet_type is PacketType.Data:
            if array[1:2] == PacketSubType.Reset:
                self._set_subtype(PacketSubType.Reset)
            elif array[1:2] == PacketSubType.GetInfo:
                self._set_subtype(PacketSubType.GetInfo)
            elif array[1:2] == PacketSubType.SetLinkSettings:
                self._set_subtype(PacketSubType.SetLinkSettings)
            else:
                for p_sub_type in PacketSubType:
                    if Private.to_integer(p_sub_type) in range(0, 32):
                        break
                    if p_sub_type.value == array[1:2]:
                        self._set_subtype(p_sub_type)
                        break

        # if array[3] is b"1":
        # self._data.
