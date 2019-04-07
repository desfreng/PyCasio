#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 18:56:02 2019

@author: gabriel
"""
from Utils import to_integer

recvPacket = b"\x0600100A4Gy36300FRENESAS SH735501000000000000409600000512\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff02.05.2201\xff\xff\xff\xff\xff\xff00010000000024327.00R0SUMQUU\xff\xff\xff\xff\xff\xff\xff\xffGABRIEL\xff\xff\xff\xff\xff\xff\xff\xff\xff20"

hardware = recvPacket[0:8].replace(b"\xff", b"").decode("ascii")
processor = recvPacket[8:24].replace(b"\xff", b"").decode("ascii")

rom_capacity = to_integer(recvPacket[24:32].replace(b"\xff", b""))
flash_rom_capacity = to_integer(recvPacket[32:40].replace(b"\xff", b""))
ram_capacity = to_integer(recvPacket[40:48].replace(b"\xff", b""))

rom_version = recvPacket[48:64].replace(b"\xff", b"").decode("ascii")

boot_code_version = recvPacket[64:80].replace(b"\xff", b"").decode("ascii")
boot_code_offset = to_integer(recvPacket[80:88].replace(b"\xff", b""))
boot_code_size = to_integer(recvPacket[88:96].replace(b"\xff", b""))

os_code_version = recvPacket[96:112].replace(b"\xff", b"").decode("ascii")
os_code_offset = to_integer(recvPacket[112:120].replace(b"\xff", b""))
os_code_size = to_integer(recvPacket[120:128].replace(b"\xff", b""))

protocol_version = recvPacket[128:132].replace(b"\xff", b"").decode("ascii")
product_id = recvPacket[132:148].replace(b"\xff", b"").decode("ascii")
user_name = recvPacket[148:164].replace(b"\xff", b"").decode("ascii")

"Hardware :           {}"
"Processor :          {}"

"ROM Capacity :       {}"
"Flash ROM Capacity : {}"
"RAM Capacity :       {}"

"ROM Version :        {}"

"Boot Code Version :  {}"
"Boot Code Offset :   {}"
"Boot Code Size :     {}"

"OS Code Version :    {}"
"OS Code Offset :     {}"
"OS Code Size :       {}"

"Protocol Version :   {}"
"Product ID :         {}"
"User Name :          {}"
