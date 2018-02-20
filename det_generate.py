import base64, os, getpass, hashlib
from Crypto import Random
from simplecrypt import decrypt
from Crypto.Protocol.KDF import PBKDF2
from Crypto.PublicKey import RSA
from libs.mnemonic import Mnemonic
from libs.rsa_py import rsa_functions
import time

start = time.time()
salt_a = "911043357914429888194562610468866919009913916826495585249693846506602119428340566558534146092917724673924692633758" #sqrt 83

mnemo = Mnemonic('english')
pwd_a = mnemo.generate(strength=256)   # for testing
iterations = 4096
length = 512
n = 4096

print("Mnemonic:")
print(pwd_a)

if(mnemo.check(pwd_a)):

	master_key = PBKDF2(pwd_a.encode('utf-8'), salt_a.encode('utf-8'), dkLen=length, count=iterations)

	rsa = rsa_functions.RSAPy(n,master_key)
	key = RSA.construct(rsa.keypair)

	private_key_readable = key.exportKey().decode("utf-8")
	public_key_readable = key.publickey().exportKey().decode("utf-8")
	address = hashlib.sha224(public_key_readable.encode("utf-8")).hexdigest()  # hashed public key

	print("Public key:")
	print(public_key_readable)

	print("Private key:")
	print(private_key_readable)

	print("Address:")
	print(address)
	end = time.time()
	elapsed = end - start
	print("Elapsed time: " + str(elapsed))

else:

	print("Mnemonic invalid!!!")