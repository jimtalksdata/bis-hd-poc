#!/usr/bin/env python

import random
import base64
from libs import arc4random
from pynput import mouse
import time
import os
	
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
    print("XY: " + str(x*y))
    print("Time: " + str(int(timeS * 1000000000)))
    print("Gathering entropy ... " + str(entropy) + " bytes gathered")
    print(base64.b64encode(bytearray(randPool)))
    if (entropy > 1024):
        return False 

def on_click(x, y, button, pressed):
    return False

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))
		
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

# Collect events until released
with mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll) as listener:
            listener.join()

arc4random.rand(randPool)
p = arc4random.getrandbits(512)

print("")
print(base64.b64encode(p))