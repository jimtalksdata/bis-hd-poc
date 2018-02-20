import random
import base64
from libs import arc4random

arc4random.rand()
p = arc4random.getrandbits(512)

print(base64.b64encode(p))