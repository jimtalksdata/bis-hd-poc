import base64, os, getpass, hashlib
import time
import random
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2
from Crypto.PublicKey import RSA
from libs.mnemonic import Mnemonic
from libs.rsa_py import rsa_functions

question = 0
mnemo = Mnemonic('english')
iterations = 20000
length = 32
n = 4096

cointype = 209 # Provisionally, 209 (atomic weight of bismuth) (see https://github.com/satoshilabs/slips/blob/master/slip-0044.md )
		
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
		passphrase = input("Passphrase (hit return for empty): ")
		addressList = []
		
		start = time.time()
		# Reverted change back to urandom. For all modern versions of Python on Linux and Windows, urandom returns cryptographically strong randomness.
		# https://docs.python.org/2/library/os.html
		# https://docs.python.org/3/library/os.html
		# RSA key generation still uses Arcfour due to immurability criterion
		pwd_a = mnemo.generate(strength=256)   # for testing
		
		passP = "mnemonic" + passphrase
		master_key = PBKDF2(pwd_a.encode('utf-8'), passP.encode('utf-8'), dkLen=length, count=iterations)
		print("Master key: " + str(base64.b64encode(master_key)))
		
		for i in range(0, addrs):
			deriv_path = "m/44'/"+ str(cointype) +"'/" + str(aid) + "'/0/" + str(i) #HD path

			account_key = PBKDF2(master_key, deriv_path.encode('utf-8'), dkLen=length, count=1)
			print("Account key: " + str(base64.b64encode(account_key)))
			
			rsa = rsa_functions.RSAPy(n,account_key)
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
			
			deriv_path = "m/44'/"+ str(cointype) +"'/" + str(aid) + "'/0/" + str(i)
			print(deriv_path + ": " + addressList[i])
		
		
		print(str(addrs) + " addresses generated in " + str(elapsed) + " seconds.")
		print("")
		print("")
				
	elif(question == 2):
	
		aid = int(input("Account ID: "))
		addrs = int(input("Address Index ID (from 0): "))
		passphrase = input("Passphrase (hit return for empty): ")
		pwd_a = input("Mnemonic (BIP39 format): ")   # for testing
		
		if(mnemo.check(pwd_a)):
		
			start = time.time()
			
			passP = "mnemonic" + passphrase
			master_key = PBKDF2(pwd_a.encode('utf-8'), passP.encode('utf-8'), dkLen=length, count=iterations)
			print("Master key: " + str(base64.b64encode(master_key)))
			
			deriv_path = "m/44'/"+ str(cointype) +"'/" + str(aid) + "'/0/" + str(addrs) #HD path
			account_key = PBKDF2(master_key, deriv_path.encode('utf-8'), dkLen=length, count=1)
			
			print("Account key: " + str(base64.b64encode(account_key)))
			
			rsa = rsa_functions.RSAPy(n,account_key)
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
		
	
		
