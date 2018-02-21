#!/usr/bin/env python
#Code from https://github.com/rolandshoemaker/py-arc4random

import random

def rand(key=None):
	if (key == None):
		key=random.sample(range(256), 256)
	seeds = _RC4PRGA(_RC4keySchedule(key))
	return (seeds[0]<<24)|(seeds[1]<<16)|(seeds[2]<<8)|seeds[3]

def randrange(x, y=None):
	if y:
		return (rand()%((y-x)+1))+x
	else:
		return rand()%(x+1)

def randsample(Rmin, Rmax, size):
	sample = []
	for i in range(size):
		sample.append((rand()%((Rmax-Rmin)+1))+Rmin)
	return sample
	
def getrandbits(k):
	"""getrandbits(k) -> x.  Generates an int with k random bits."""
	if k <= 0:
		raise ValueError('number of bits must be greater than zero')
	if k != int(k):
		raise TypeError('number of bits should be an integer')
	if (k % 8) != 0:
		raise TypeError('number of bits should be multiple of 8')
	numbytes = (k + 7) // 8
	return bytearray(randsample(0,255,numbytes))
	
def _RC4keySchedule(key):
	sbox = list(range(256))
	x = 0
	keySize = len(key)
	for i in range(256):
		x = (x+sbox[i]+key[i%keySize])%256
		_swap(sbox, i, x)
	return sbox

def _RC4PRGA(state):
	x, y = 0, 0
	seeds = []
	# Discard first 1536 bytes of the keystream according to RFC4345 as they may reveal information
	# about key used (a set of these keys could reveal information about the source for our key)
	for i in range(1536+4):
		x = (x+1)%256
		y = (y+state[x])%256
		_swap(state, x, y)
		if i >= (1536):
			seeds.append(state[(state[x]+state[y])%256])
	return seeds

def _swap(listy, n1, n2):
	listy[n1], listy[n2] = listy[n2], listy[n1]