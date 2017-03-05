#!/usr/bin/python3
"""
print("base32verify.py: script for add crc-32 code for every line of base32 information block.")
print("Usage (add crc-32): cat file | base32add.py")
print("Usage (add crc-32): cat file | base32add.py > outputfile")
"""

import sys
import base64
import zlib

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567=\n"
output = ""
for i, line in enumerate(sys.stdin):
    for pos, ch in enumerate(line):
        if (ch not in alphabet):
            print("Error base 32 symbol in line {0}, col {1}".format(i + 1, pos + 1))
    without_wrap = line.replace("\n", "")
    l = without_wrap.replace("=", "")
    l = l + "A" * (8 - len(l) % 8)
    bytes_line = base64.b32decode(l)
    crc32 = base64.b32encode(zlib.crc32(bytes_line).to_bytes(4, byteorder="big"))
    output += "{0}?{1}\n".format(without_wrap, str(crc32)[2:-1])
print(output)