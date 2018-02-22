#!/usr/bin/env python

from libs import rc4simple
import binascii
from pyentrp import entropy as ent
import numpy as np
import struct
import time

# Reference: https://tools.ietf.org/html/rfc6229

key = bytearray.fromhex("0102030405")
print(bytes(key))
state = rc4simple.seed(bytes(key))

print(binascii.hexlify(rc4simple.getrandbits(64))) # b2 39 63 05  f0 3d c0 27
print(binascii.hexlify(rc4simple.getrandbits(64))) # cc c3 52 4a  0a 11 18 a8
for i in range(5):
	print(rc4simple.randsample(0,5,50))
for i in range(30):
	print(rc4simple.randint(5,10))

#print(hex(arc4random.rand(state)))

#print(binascii.hexlify(arc4random.getrandbits(256)))

key = bytearray.fromhex("0102030405060708090a0b0c0d0e0f10")
print(bytes(key))
state = rc4simple.seed(bytes(key))

print(binascii.hexlify(rc4simple.getrandbits(64))) # 9a c7 cc 9a  60 9d 1e f7 
print(binascii.hexlify(rc4simple.getrandbits(64))) # b2 93 28 99  cd e4 1b 97

key = bytearray.fromhex("1ada31d5cf688221c109163908ebe51debb46227c6cc8b37641910833222772a")
print(bytes(key))
state = rc4simple.seed(bytes(key))

print(binascii.hexlify(rc4simple.getrandbits(64))) # dd 5b cb 00  18 e9 22 d4
print(binascii.hexlify(rc4simple.getrandbits(64))) # 94 75 9d 7c  39 5d 02 d3

key = bytearray.fromhex("1ada31d5cf688221c109163908ebe51debb46227c6cc8b37641910833222772a")
print(bytes(key))
state = rc4simple.seed(bytes(key))

# Discard first 1536 bytes of the keystream according to RFC4345 as they may reveal information
# about key used (a set of these keys could reveal information about the source for our key)
rc4simple.getrandbits(1536*8)
print("Discarding 1536 bytes...")
print(binascii.hexlify(rc4simple.getrandbits(64))) # 8c 3c 13 f8  c2 38 8b b7
print(binascii.hexlify(rc4simple.getrandbits(64))) # 3f 38 57 6e  65 b7 c4 46


# Generate 20MB of random data and time

start = time.time()
start = time.time()
file_object  = open("testrand", "wb")
key = bytearray.fromhex("1ada31d5cf688221c109163908ebe51debb46227c6cc8b37641910833222772a")
print(bytes(key))
state = rc4simple.seed(bytes(key))
bytes = rc4simple.getrandbits(1000000*8*20)
file_object.write(struct.pack('20000000B', *bytes))
end = time.time()
print("20MB generated in: " + str(end - start))

# Test results of 20MB file:
'''
Entropy = 7.999990 bits per byte.

Optimum compression would reduce the size
of this 20000000 byte file by 0 percent.

Chi square distribution for 20000000 samples is 273.78, and randomly
would exceed this value 20.01 percent of the times.

Arithmetic mean value of data bytes is 127.5225 (127.5 = random).
Monte Carlo value for Pi is 3.141276314 (error 0.01 percent).
Serial correlation coefficient is 0.000033 (totally uncorrelated = 0.0).'''
