#!/usr/bin/env python
#Barebones crypto module that outsources code to Crypto.Cipher.ARC4

from Crypto.Cipher import ARC4

global ARC4Cipher

def seed(key):
	global ARC4Cipher
	ARC4Cipher = ARC4.new(key)
	
def rand():
	return int.from_bytes(getrandbits(32),byteorder='big')
	
def getrandbits(k):
	"""Yield a pseudo-random stream of bits based on 256-byte array `k`."""
	global ARC4Cipher
	if k <= 0:
		raise ValueError('number of bits must be greater than zero')
	if k != int(k):
		raise TypeError('number of bits should be an integer')
	if (k % 8) != 0:
		raise TypeError('number of bits should be multiple of 8')
	numbytes = (k + 7) // 8
	return(ARC4Cipher.encrypt(bytes(numbytes)))
	
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