import random as rnd

import struct

with open("generated_10k.rnd", "w+") as f:
    data = []
    for i in range(0, int(100e6)):
        r = rnd.randint(0, 2**32)
        data.append(r)
        f.write(str(r))
        f.write("\n")