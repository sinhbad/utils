#!/usr/bin/python3
"""
print("base32verify.py: script for verify crc-32 code for every line of base32 information block.")
print("Usage (verify crc-32): cat file | base32verify.py")
print("Usage (verify crc-32): cat file | base32verify.py > outputfile")
"""

import sys
import base64
import zlib

def check_line(line, alphabet, i):
    result = True
    for pos, ch in enumerate(line):
        if (ch not in alphabet):
            result = False
            print("Bad base32 char in line {0}, col {1}".format(i + 1, pos + 1))
    return result

def get_data(line):
    without_wrap = line.replace("\n", "")
    l = without_wrap.replace("=", "")
    l = l + "A" * (8 - len(l) % 8)
    return base64.b32decode(l)

errors = 0
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567=\n"
for i, line in enumerate(sys.stdin):
    if (line.replace(" ", "").replace("\n", "") == ""):
        continue
    cols = line.split("?")
    if not check_line(cols[0], alphabet, i):
        errors += 1
        continue
    if (len(cols) != 2):
        errors += 1
        print("Line {0} doesn't contain or contains bad crc-32 data".format(i+1))
        continue
    if not check_line(cols[1], alphabet, i):
        errors += 1
        continue
    #Check crc-32
    data = get_data(cols[0])
    crc32 = str(base64.b32encode(zlib.crc32(data).to_bytes(4, byteorder="big")))[2:-1]
    if (crc32 != cols[1].replace("\n", "")):
        errors += 1
        print("Bad crc32 value of line {0}".format(i+1))
        continue
print("Number of errors: {0}".format(errors))