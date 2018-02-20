#!/usr/bin/env python

from libs.rsa_py import rsa_functions
from Crypto.PublicKey import RSA
from Crypto.Protocol.KDF import PBKDF2
import time

iterations = 4096
length = 512

seed = "394329483729326593276493274932573289462347364374877847832487348"
salt = "911043357914429888194562610468866919009913916826495585249693846506602119428340566558534146092917724673924692633758" #sqrt 83
master_key = PBKDF2(seed.encode('utf-8'), salt.encode('utf-8'), dkLen=length, count=iterations)

print("Master key (" + str(length) + "-byte, " + str(iterations) + " iterations): ")
print(master_key)

start = time.time()
n = 4096
rsa = rsa_functions.RSAPy(n,master_key)
rsak = RSA.construct(rsa.keypair)

private_key_readable = rsak.exportKey().decode("utf-8")
public_key_readable = rsak.publickey().exportKey().decode("utf-8")

end = time.time()
print(str(n) + "-bit RSA public:")
print(str(public_key_readable))
print(str(n) + "-bit RSA private:")
print(str(private_key_readable))
print("Time elapsed: " + str(end - start))
print("")
