#!/usr/bin/env python

from libs import arc4random
import binascii
from Crypto.Cipher import ARC4

# Reference: https://tools.ietf.org/html/rfc6229

key = bytearray.fromhex("0102030405")
print(key)
print(hex(arc4random.rand(key))) # d8 72 9d b4

key = bytearray.fromhex("0102030405060708090a0b0c0d0e0f10")
print(key)
print(hex(arc4random.rand(key))) # ff a0 b5 14 

key = bytearray.fromhex("1ada31d5cf688221c109163908ebe51debb46227c6cc8b37641910833222772a")
print(key)
print(hex(arc4random.rand(key))) # 8c 3c 13 f8