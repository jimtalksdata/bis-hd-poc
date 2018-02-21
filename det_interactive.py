import base64, os, getpass, hashlib
import time
import random
from Crypto import Random
from simplecrypt import decrypt
from Crypto.Protocol.KDF import PBKDF2
from Crypto.PublicKey import RSA
from pynput import mouse
from libs.mnemonic import Mnemonic
from libs.rsa_py import rsa_functions
from libs import arc4random

question = 0
mnemo = Mnemonic('english')
iterations = 4096
length = 512
n = 4096

cointype = 209 # Provisionally, 209 (atomic weight of bismuth) (see https://github.com/satoshilabs/slips/blob/master/slip-0044.md )

# rand parameters
poolsize = 256
randPool = random.sample(range(256), poolsize)	
pptr = 0
entropy = 0

def on_move(x, y):
    timeS = time.time() - int(time.time())
    global entropy
    global randPool
	
    seedInt16(x * y)
    seedInt(int(timeS * 1000000000))
	
    os.system('cls') # on windows
    print("Gathering entropy ... " + str(entropy) + " bytes gathered")
    print(base64.b64encode(bytearray(randPool)))
    if (entropy > 1024):
        return False 
		
def seedInt (x):
	seedInt8(x)
	seedInt8((x >> 8))
	seedInt8((x >> 16))
	seedInt8((x >> 24))

def seedInt16 (x):
	seedInt8(x)
	seedInt8((x >> 8))

def seedInt8 (x):
	global poolsize
	global randPool
	global entropy
	global pptr
	randPool[pptr] ^= x & 255
	entropy += 1
	pptr += 1

	if (pptr >= poolsize): 
		pptr -= poolsize

os.system('cls') # on windows
print("Move the mouse to gather entropy...")
		
with mouse.Listener(
	on_move=on_move) as listener:
		listener.join()

arc4random.rand(randPool)
		
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
		pwd_a = mnemo.to_mnemonic(arc4random.getrandbits(256))   # for testing
		
		for i in range(0, addrs):
			deriv_path = "m/44'/"+ str(cointype) +"'/" + str(aid) + "/0/" + str(i) #HD path

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
			
			deriv_path = "m/44'/"+ str(cointype) +"'/" + str(aid) + "/0/" + str(i)
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
			deriv_path = "m/44'/"+ str(cointype) +"'/" + str(aid) + "/0/" + str(addrs) #HD path
			
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
		
	
		
