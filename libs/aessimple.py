#!/usr/bin/env python
#Barebones crypto module that outsources code to Crypto.Cipher.AES

from Crypto.Cipher import AES
from Crypto.Util import Counter

global AESCipher

def seed(keybytes, counter_wraparound=False):
	global AESCipher
	assert(len(keybytes) == 32)
	print(keybytes)
	key = keybytes[0:16]
	iv = keybytes[16:32]
	print(len(key))
	print(len(iv))
	print(key)
	print(iv)
	assert(len(key) == 16)
	assert(len(iv) == 16)
	
	ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'),
                               allow_wraparound=counter_wraparound)
	AESCipher = AES.new(key, AES.MODE_CTR, counter=ctr)
	
def rand():
	return int.from_bytes(getrandbits(32),byteorder='big')
	
def getrandbits(k):
	"""Yield a pseudo-random stream of bits based on 256-byte array `k`."""
	global AESCipher
	if k <= 0:
		raise ValueError('number of bits must be greater than zero')
	if k != int(k):
		raise TypeError('number of bits should be an integer')
	if (k % 8) != 0:
		raise TypeError('number of bits should be multiple of 8')
	numbytes = (k + 7) // 8
	return(AESCipher.encrypt(bytes(numbytes)))
	
def randint(x, y=None):
	if y:
		return (rand()%((y-x)+1))+x
	else:
		return rand()%(x+1)
		
def randrange(x, y):
	return (rand()%((y-x)+1))+x

		
def randsample(Rmin, Rmax, size):
	sample = []
	for i in range(size):
		sample.append((rand()%((Rmax-Rmin)+1))+Rmin)
	return sample