#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Utils import *


class OverwriteMode(Enum):
    AskUser = b"00"
    Terminate = b"00"
    ForceOverwrite = b"00"
    Default = AskUser


class CommandPacket(BasePacket):
    def __init__(self, command_type: CommandSubType = PacketSubType.Unknown, command_data: bytes = bytes(),
                 can_be_send: bool = True):
        if not isinstance(command_type, (CommandSubType, PacketSubType)):
            raise TypeError
        if not isinstance(command_data, (bytes, bytearray)):
            raise TypeError

        super().__init__(PacketType.Command, command_type, command_data, can_be_sent=can_be_send)

        self._overwrite = OverwriteMode.Default
        self._data_type = b"00"
        self._file_size = 0
        self._data1 = bytearray()
        self._data2 = bytearray()
        self._data3 = bytearray()
        self._data4 = bytearray()
        self._data5 = bytearray()
        self._data6 = bytearray()

        if len(command_data) > 0:
            for a in OverwriteMode:
                if a.value == command_data[0:2]:
                    self._overwrite = a

            self._file_size = to_integer(command_data[4:12])

            self._data_type = command_data[2:4]

            relative_offset = 24

            self._data1 = command_data[relative_offset:relative_offset + to_integer(command_data[12:14])]
            relative_offset += to_integer(command_data[12:14])

            self._data2 = command_data[relative_offset:relative_offset + to_integer(command_data[14:16])]
            relative_offset += to_integer(command_data[14:16])

            self._data3 = command_data[relative_offset:relative_offset + to_integer(command_data[16:18])]
            relative_offset += to_integer(command_data[16:18])

            self._data4 = command_data[relative_offset:relative_offset + to_integer(command_data[18:20])]
            relative_offset += to_integer(command_data[18:20])

            self._data5 = command_data[relative_offset:relative_offset + to_integer(command_data[20:22])]
            relative_offset += to_integer(command_data[20:22])

            self._data6 = command_data[relative_offset:relative_offset + to_integer(command_data[22:24])]

    @classmethod
    def from_data(cls, packet_subtype, packet_data):
        if not isinstance(packet_subtype, (bytes, bytearray)):
            raise TypeError
        if not isinstance(packet_data, (bytes, bytearray)):
            raise TypeError

        for subtype in CommandSubType:
            if subtype.value == packet_subtype:
                return cls(subtype, packet_data, can_be_send=False)
        return None

    def __repr__(self):
        return "CommandPacket at {}\n" \
               "--------------- Data : ---------------\n"\
               "SubType :           {}\n" \
               "Overwrite Mode :    {}\n" \
               "Data Type :         {}\n" \
               "File Size :         {}\n" \
               "Data 1 :            {}\n" \
               "Data 2 :            {}\n" \
               "Data 3 :            {}\n" \
               "Data 4 :            {}\n" \
               "Data 5 :            {}\n" \
               "Data 6 :            {}\n" \
               "--------------------------------------"\
            .format(hex(id(self)), self.packet_subtype.name, self.overwrite.name, self.data_type, self.file_size,
                    self.data1, self.data2, self.data3, self.data4, self.data5, self.data6)

    @property
    def packet_subtype(self) -> CommandSubType:
        return self._sub_type

    @packet_subtype.setter
    def packet_subtype(self, type: CommandSubType):
        if not isinstance(type, CommandSubType):
            raise TypeError

        self._sub_type = type

    @property
    def overwrite(self) -> OverwriteMode:
        return self._overwrite

    @overwrite.setter
    def overwrite(self, mode: OverwriteMode):
        if not isinstance(mode, OverwriteMode):
            raise TypeError
        self._overwrite = mode

    @property
    def data_type(self) -> bytes:
        return bytes(self._data_type)

    @data_type.setter
    def data_type(self, data_typee: bytes):
        if not isinstance(data_typee, (bytearray, bytes)):
            raise TypeError
        if len(data_typee) < 2:
            raise ValueError

        self._data_type = data_typee[0:2]

    @property
    def file_size(self) -> int:
        return self._file_size

    @file_size.setter
    def file_size(self, size: int):
        if size > to_integer(b"FFFFFFFF"):
            raise ValueError("File size to big !")

        self._file_size = size

    @property
    def data1(self) -> bytes:
        return bytes(self._data1)

    @data1.setter
    def data1(self, data: bytes):
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError

        if len(data) > 255:
            self._data1 = data[0:255]
        else:
            self._data1 = data

    @property
    def data2(self) -> bytes:
        return bytes(self._data2)

    @data2.setter
    def data2(self, data: bytes):
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError
        if len(data) > 255:
            self._data2 = data[0:255]
        else:
            self._data2 = data

    @property
    def data3(self) -> bytes:
        return bytes(self._data3)

    @data3.setter
    def data3(self, data: bytes):
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError
        if len(data) > 255:
            self._data3 = data[0:255]
        else:
            self._data3 = data

    @property
    def data4(self) -> bytes:
        return bytes(self._data4)

    @data4.setter
    def data4(self, data: bytes):
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError
        if len(data) > 255:
            self._data4 = data[0:255]
        else:
            self._data4 = data

    @property
    def data5(self) -> bytes:
        return bytes(self._data5)

    @data5.setter
    def data5(self, data: bytes):
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError
        if len(data) > 255:
            self._data5 = data[0:255]
        else:
            self._data5 = data

    @property
    def data6(self) -> bytes:
        return bytes(self._data6)

    @data6.setter
    def data6(self, data: bytes):
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError
        if len(data) > 255:
            self._data6 = data[0:255]
        else:
            self._data6 = data

    def compute_checksum(self):
        self._data.clear()

        if len(self.data1) == 0 and len(self.data2) == 0 and len(self.data3) == 0 and len(self.data4) == 0 and \
                len(self.data5) == 0 and len(self.data6) == 0 and self.file_size == 0 and \
                self.overwrite.value == b"00":
            super().compute_checksum()
        else:
            self._data += self.overwrite.value
            self._data += self.data_type
            self._data += to_hexadecimal(self.file_size, 8)

            self._data += to_hexadecimal(len(self.data1), 2)
            self._data += to_hexadecimal(len(self.data2), 2)
            self._data += to_hexadecimal(len(self.data3), 2)
            self._data += to_hexadecimal(len(self.data4), 2)
            self._data += to_hexadecimal(len(self.data5), 2)
            self._data += to_hexadecimal(len(self.data6), 2)

            self._data += self.data1
            self._data += self.data2
            self._data += self.data3
            self._data += self.data4
            self._data += self.data5
            self._data += self.data6

            super().compute_checksum()


class DataPacket(BasePacket):
    def __init__(self, data_type: DataSubType = PacketSubType.Unknown, packet_data: bytes = bytes(), can_be_send: bool = True):
        if not isinstance(data_type, (DataSubType, PacketSubType)):
            raise TypeError
        if not isinstance(packet_data, (bytes, bytearray)):
            raise TypeError

        super().__init__(PacketType.Error, data_type, can_be_sent=can_be_send)

        if len(packet_data) > 8:
            self._total_packet_number = to_integer(packet_data[0:4])
            self._packet_number = to_integer(packet_data[4:8])
            self._packet_data = packet_data[8:]
        else:
            self._total_packet_number = 0
            self._packet_number = 0
            self._packet_data = bytearray()

    @classmethod
    def from_data(cls, packet_subtype, packet_data):
        if not isinstance(packet_subtype, (bytes, bytearray)):
            raise TypeError

        for subtype in DataSubType:
            if subtype.value == packet_subtype:
                return cls(subtype, packet_data, False)
        return None

    @property
    def total_packet_number(self) -> int:
        return self._total_packet_number

    @total_packet_number.setter
    def total_packet_number(self, value):
        if value > 65535 or value < 1:
            raise ValueError

        self._total_packet_number = value

    @property
    def packet_number(self) -> int:
        return self._packet_number

    @packet_number.setter
    def packet_number(self, value):
        if value > 65535 or value < 1:
            raise ValueError

        self._packet_number = value

    @property
    def packet_data(self) -> bytes:
        return bytes(self._packet_data)

    @packet_data.setter
    def packet_data(self, data):
        if not isinstance(data, (bytearray, bytes)):
            raise TypeError

        if len(data) > 512:
            raise ValueError

        self._packet_data = data

    def __repr__(self):
        return "DataPacket [Type : {}] at {}\n" \
               "--------------- Data : ---------------\n"\
               "Total Packet Number :       {}\n" \
               "Packet Number :             {}\n" \
               "Data :                      {}\n" \
               "--------------------------------------"\
            .format(self.packet_subtype.name, hex(id(self)), self.total_packet_number, self.packet_number,
                    self.packet_data)

    def compute_checksum(self):
        self._data.clear()

        self._data += to_hexadecimal(self.total_packet_number, 4)
        self._data += to_hexadecimal(self.packet_number, 4)
        self._data += self.packet_data

        super().compute_checksum()


class RoleswapPacket(BasePacket):
    def __init__(self, can_be_send: bool = True):
        super().__init__(PacketType.Roleswap, RoleswapSubType.Default, can_be_sent=can_be_send)

    @classmethod
    def from_data(cls, packet_subtype, packet_data):
        return cls(False)

    def __repr__(self):
        return "RoleswapPacket at {}".format(hex(id(self)))


class CheckPacket(BasePacket):
    def __init__(self, check_type: CheckSubType = PacketSubType.Unknown, can_be_send : bool = True):
        if not isinstance(check_type, (CheckSubType, PacketSubType)):
            raise TypeError

        super().__init__(PacketType.Check, check_type, can_be_sent=can_be_send)

    @classmethod
    def from_data(cls, packet_subtype, packet_data):
        if not isinstance(packet_subtype, (bytes, bytearray)):
            raise TypeError

        if packet_subtype == CheckSubType.CheckConnection.value:
            return cls(CheckSubType.CheckConnection, False)
        elif packet_subtype == CheckSubType.InitConnection.value:
            return cls(CheckSubType.InitConnection, False)
        else:
            return None

    def __repr__(self):
        return "CheckPacket [Type : {}] at {}".format(self.packet_subtype.name, hex(id(self)))

    @classmethod
    def init(cls):
        return cls(CheckSubType.InitConnection)

    @classmethod
    def check(cls):
        return cls(CheckSubType.CheckConnection)


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
                   "--------------- Data : ---------------\n" \
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


class ErrorPacket(BasePacket):
    def __init__(self, error_type: ErrorSubType = PacketSubType.Unknown, can_be_send : bool = True):
        if not isinstance(error_type, (ErrorSubType, PacketSubType)):
            raise TypeError

        super().__init__(PacketType.Error, error_type, can_be_sent=can_be_send)

    @classmethod
    def from_data(cls, packet_subtype, packet_data):
        if not isinstance(packet_subtype, (bytes, bytearray)):
            raise TypeError

        for subtype in ErrorSubType:
            if subtype.value == packet_subtype:
                return cls(subtype, False)
        return None

    def __repr__(self):
        return "ErrorPacket [Type : {}] at {}".format(self.packet_subtype.name, hex(id(self)))

    @classmethod
    def default(cls):
        return cls(ErrorSubType.Default)

    @classmethod
    def resend_request(cls):
        return cls(ErrorSubType.ResendRequest)

    @classmethod
    def overwrite_error(cls):
        return cls(ErrorSubType.OverwriteError)

    @classmethod
    def no_overwrite_reply(cls):
        return cls(ErrorSubType.NoOverwriteReply)

    @classmethod
    def overwrite_impossible(cls):
        return cls(ErrorSubType.OverwriteImpossible)

    @classmethod
    def memory_full(cls):
        return cls(ErrorSubType.MemoryFull)


class TerminatePacket(BasePacket):
    def __init__(self, terminate_type: TerminateSubType = PacketSubType.Unknown, can_be_send : bool = True):
        if not isinstance(terminate_type, (TerminateSubType, PacketSubType)):
            raise TypeError

        super().__init__(PacketType.Terminate, terminate_type, can_be_sent=can_be_send)


    @classmethod
    def from_data(cls, packet_subtype, packet_data):
        if not isinstance(packet_subtype, (bytes, bytearray)):
            raise TypeError

        for subtype in TerminateSubType:
            if subtype.value == packet_subtype:
                return cls(subtype, False)
        return None

    def __repr__(self):
        return "TerminatePacket [Type : {}] at {}".format(self.packet_subtype.name, hex(id(self)))

    @classmethod
    def default(cls):
        return cls(TerminateSubType.Default)

    @classmethod
    def user_request(cls):
        return cls(TerminateSubType.UserRequest)

    @classmethod
    def timeout(cls):
        return cls(TerminateSubType.Timeout)

    @classmethod
    def on_overwrite(cls):
        return cls(TerminateSubType.Overwrite)
