#!/usr/bin/env python
#Barebones crypto module that outsources code to Crypto.Cipher.AES

from Crypto.Cipher import AES
from Crypto.Util import Counter
import random

request_count = 0

BPF = 53        # Number of bits in a float
RECIP_BPF = 2**-BPF
_RESEED_INTERVAL = 1 << 48

global AESCipher

def seed(keybytes, counter_wraparound=False):
	"""Initializes AES in CTR mode (128, 192, or 256 bit key with 128 bit IV)"""
	global AESCipher
	assert(len(keybytes) == 32 or len(keybytes) == 40 or len(keybytes) == 48)
	if (len(keybytes) == 32): # AES-128-CTR
		key = keybytes[0:16]
		iv = keybytes[16:32]
	if (len(keybytes) == 40): # AES-192-CTR
		key = keybytes[0:24]
		iv = keybytes[24:40]
	if (len(keybytes) == 48): # AES-256-CTR
		key = keybytes[0:32]
		iv = keybytes[32:48]
	assert(len(key) == 16 or len(key) == 24 or len(key) == 32)
	assert(len(iv) == 16)
	
	ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'),
                               allow_wraparound=counter_wraparound)
	AESCipher = AES.new(key, AES.MODE_CTR, counter=ctr)
	request_count = 0
	
def random():
	return (int.from_bytes(getrandbits(7 * 8),byteorder='big') >> 3) * RECIP_BPF
	
def rand():
	return int.from_bytes(getrandbits(32),byteorder='big')
	
def getrandbits(k):
	"""Yield a pseudo-random stream of bits."""
	global AESCipher, request_count, _RESEED_INTERVAL
	if k <= 0:
		raise ValueError('number of bits must be greater than zero')
	if k != int(k):
		raise TypeError('number of bits should be an integer')
	if (k % 8) != 0:
		raise ValueError('number of bits should be multiple of 8')
	numbytes = (k + 7) // 8
	request_count += numbytes
	if (request_count > _RESEED_INTERVAL):
		raise ValueError('output exceeds safe deterministic reseed interval; please reseed generator by calling seed()')
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