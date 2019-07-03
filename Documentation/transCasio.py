#!/usr/bin/python3

import sys

if len(sys.argv) != 2:
    print("usage: transCasio <fichier G1M>")
    sys.exit(1)

with open(sys.argv[1], "rb") as f:
    b = f.read()

esc7f = False
esce5 = False
esce6 = False
escf7 = False

table = {
    0x0e: "->",
    0x11: "!=",
    0x86: "rac",
    0x87: "(-)", ## moins unaire (opposé)
    0x89: "+",
    0x8b: "²",
    0x99: "-",
    0xb9: " div ",
    0xe2: "Lbl ",
    0xec: "Goto ",
    0xa8: "^",
    0xa9: " mult ",
    0xaa: "or",
    0xbb: " frac ", ## l inversé (fraction)

}
table7f = {
    0x1f: "é",
    0x26: "d/dx(",
    0x8f: "Getkey",
    0xf0: "[Fonc Y]",
}
tablee5 = {
    0x43: "Delta",
}
tablee6 = {
    0x40: "alpha",
    0x41: "beta",
}
tablef7 = {
    0x00: "If ",
    0x01: "Then ",
    0x02: "Else ",
    0x03: "IfEnd",
    0x04: "For ",
    0x05: " To ",
    0x06: " Step ", ## À vérifier...
    0x07: "Next ",
    0x0a: "Do",
    0x0b: "LpWhile ",
    0x10: "Locate ",
    0x18: "ClrTxt",
    0x9e: "Menu ",
}

# le programme commence à l'offset 86
for i in b[0:]:
    if i == 0x0d:
        print()
    elif esc7f == True:
        esc7f = False
        if i in table7f:
            print(table7f[i], end = "")
        else:
            print("[Code 7f inconnu "+hex(i)+"]", end = "")
    elif esce5 == True:
        esce5 = False
        if i in tablee5:
            print(tablee5[i], end = "")
        else:
            print("[Code e5 inconnu "+hex(i)+"]", end = "")
    elif esce6 == True:
        esce6 = False
        if i in tablee6:
            print(tablee6[i], end = "")
        else:
            print("[Code e6 inconnu "+hex(i)+"]", end = "")
    elif escf7 == True:
        escf7 = False
        if i in tablef7:
            print(tablef7[i], end = "")
        else:
            print("[Code f7 inconnu "+hex(i)+"]", end = "")
    elif i == 0x7f:
        esc7f = True
    elif i == 0xe5:
        esce5 = True
    elif i == 0xe6:
        esce6 = True
    elif i == 0xf7:
        escf7 = True
    elif i in table:
        print(table[i], end = "")
    elif i == 0:
        pass
    elif i == 0x0c:
        print("[triangle]")
    else:
        print(chr(i), end = "")
sys.exit(0)

