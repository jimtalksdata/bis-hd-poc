import base64, os, getpass, hashlib
from Crypto import Random
from simplecrypt import decrypt
from Crypto.Protocol.KDF import PBKDF2
from Crypto.PublicKey import RSA
from libs.mnemonic import Mnemonic
from libs.rsa_py import rsa_functions
import time


question = 0
mnemo = Mnemonic('english')
iterations = 4096
length = 512
n = 4096

while(question != 3):

	print("Test functions for deterministic Bismuth wallet:")
	print("")
	print("1) Generate new keypair (random)")
	print("2) Generate keypair from mnemonic")
	print("3) Exit")
	print("")
	question = int(input("Please make a selection: "))
	
	if(question == 1):
	
		aid = int(input("Account ID: "))
		addrs = int(input("Number of addresses to generate: "))
		addressList = []
		
		start = time.time()
		pwd_a = mnemo.generate(strength=256)   # for testing
		
		for i in range(0, addrs):
			deriv_path = "m/44'/1'/" + str(aid) + "/0/" + str(i) #HD path

			master_key = PBKDF2(pwd_a.encode('utf-8'), deriv_path.encode('utf-8'), dkLen=length, count=iterations)

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
			addressList.append(address)
			
		end = time.time()	
		elapsed = end - start		
		
		print("")
		print("Mnemonic:")
		print(pwd_a)
		
		print("Addreses:")
		for i in range(0, addrs):
			
			deriv_path = "m/44'/1'/" + str(aid) + "/0/" + str(i)
			print(deriv_path + ": " + addressList[i])
		
		
		print(str(addrs) + " addresses generated in " + str(elapsed) + " seconds.")
		print("")
		print("")
				
	elif(question == 2):
	
		aid = int(input("Account ID: "))
		addrs = int(input("Address Index ID (from 0): "))
		pwd_a = input("Mnemonic (BIP39 format): ")   # for testing
		
		if(mnemo.check(pwd_a)):
		
			start = time.time()
			deriv_path = "m/44'/1'/" + str(aid) + "/0/" + str(addrs) #HD path
			
			master_key = PBKDF2(pwd_a.encode('utf-8'), deriv_path.encode('utf-8'), dkLen=length, count=iterations)

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
			print("1 address generated in " + str(elapsed) + " seconds.")
			print("")
		
		else:

			print("Mnemonic invalid!!!")
		
	
		
