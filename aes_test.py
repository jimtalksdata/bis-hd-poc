#!/usr/bin/env python

from libs import aessimple
import binascii
from pyentrp import entropy as ent
import numpy as np
import struct
import time
import math

# Reference: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38a.pdf

#AES-128
print("Testing AES-128-CTR...")
key = bytearray.fromhex("2b7e151628aed2a6abf7158809cf4f3c" + "f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff")
print(bytes(key))
state = aessimple.seed(bytes(key))

plaintext = bytearray.fromhex("6bc1bee22e409f96e93d7e117393172a")
cipher = bytearray(aessimple.getrandbits(128))
for i in range(len(cipher)):
    plaintext[i] ^= cipher[i]
assert(plaintext == bytes.fromhex("874d6191b620e3261bef6864990db6ce"))

plaintext = bytearray.fromhex("ae2d8a571e03ac9c9eb76fac45af8e51")
cipher = bytearray(aessimple.getrandbits(128))
for i in range(len(cipher)):
    plaintext[i] ^= cipher[i]
assert(plaintext == bytes.fromhex("9806f66b7970fdff8617187bb9fffdff"))

plaintext = bytearray.fromhex("30c81c46a35ce411e5fbc1191a0a52ef")
cipher = bytearray(aessimple.getrandbits(128))
for i in range(len(cipher)):
    plaintext[i] ^= cipher[i]
assert(plaintext == bytes.fromhex("5ae4df3edbd5d35e5b4f09020db03eab"))

plaintext = bytearray.fromhex("f69f2445df4f9b17ad2b417be66c3710")
cipher = bytearray(aessimple.getrandbits(128))
for i in range(len(cipher)):
    plaintext[i] ^= cipher[i]
assert(plaintext == bytes.fromhex("1e031dda2fbe03d1792170a0f3009cee"))

#AES-192
print("Testing AES-192-CTR...")
key = bytearray.fromhex("8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b" + "f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff")
print(bytes(key))
state = aessimple.seed(bytes(key))

plaintext = bytearray.fromhex("6bc1bee22e409f96e93d7e117393172a")
cipher = bytearray(aessimple.getrandbits(128))
for i in range(len(cipher)):
    plaintext[i] ^= cipher[i]
assert(plaintext == bytes.fromhex("1abc932417521ca24f2b0459fe7e6e0b"))

plaintext = bytearray.fromhex("ae2d8a571e03ac9c9eb76fac45af8e51")
cipher = bytearray(aessimple.getrandbits(128))
for i in range(len(cipher)):
    plaintext[i] ^= cipher[i]
assert(plaintext == bytes.fromhex("090339ec0aa6faefd5ccc2c6f4ce8e94"))

plaintext = bytearray.fromhex("30c81c46a35ce411e5fbc1191a0a52ef")
cipher = bytearray(aessimple.getrandbits(128))
for i in range(len(cipher)):
    plaintext[i] ^= cipher[i]
assert(plaintext == bytes.fromhex("1e36b26bd1ebc670d1bd1d665620abf7"))

plaintext = bytearray.fromhex("f69f2445df4f9b17ad2b417be66c3710")
cipher = bytearray(aessimple.getrandbits(128))
for i in range(len(cipher)):
    plaintext[i] ^= cipher[i]
assert(plaintext == bytes.fromhex("4f78a7f6d29809585a97daec58c6b050"))

#AES-256
print("Testing AES-256-CTR...")
key = bytearray.fromhex("603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4" + "f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff")
print(bytes(key))
state = aessimple.seed(bytes(key))

plaintext = bytearray.fromhex("6bc1bee22e409f96e93d7e117393172a")
cipher = bytearray(aessimple.getrandbits(128))
for i in range(len(cipher)):
    plaintext[i] ^= cipher[i]
assert(plaintext == bytes.fromhex("601ec313775789a5b7a7f504bbf3d228"))

plaintext = bytearray.fromhex("ae2d8a571e03ac9c9eb76fac45af8e51")
cipher = bytearray(aessimple.getrandbits(128))
for i in range(len(cipher)):
    plaintext[i] ^= cipher[i]
assert(plaintext == bytes.fromhex("f443e3ca4d62b59aca84e990cacaf5c5"))

plaintext = bytearray.fromhex("30c81c46a35ce411e5fbc1191a0a52ef")
cipher = bytearray(aessimple.getrandbits(128))
for i in range(len(cipher)):
    plaintext[i] ^= cipher[i]
assert(plaintext == bytes.fromhex("2b0930daa23de94ce87017ba2d84988d"))

plaintext = bytearray.fromhex("f69f2445df4f9b17ad2b417be66c3710")
cipher = bytearray(aessimple.getrandbits(128))
for i in range(len(cipher)):
    plaintext[i] ^= cipher[i]
assert(plaintext == bytes.fromhex("dfc9c58db67aada613c2dd08457941a6"))

print("Pi normality test...")

count = 0
iters = 500000
for i in range(iters):
	if math.pow(aessimple.random(), 2) + math.pow(aessimple.random(), 2) <= 1.0:
		count += 1
pi = 4.0 * count / iters
print("pi = " + str(pi))

print("All tests passed")
