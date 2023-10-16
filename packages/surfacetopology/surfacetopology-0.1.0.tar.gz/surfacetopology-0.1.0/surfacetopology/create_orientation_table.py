import itertools
import numpy as np

debug = False

for k1, k2, k3 in itertools.product(range(4), repeat=3):
    code = k1*16 + k2*4 + k3
    k = np.array([k1, k2, k3])
    s = np.sum(k == 0)

    if s == 1:
        while k[2] != 0:
            k = np.roll(k, 1)
        if k[0] == k[1]:
            result = 0
        else:
            result = tuple(k[:2]) in [(1, 2), (2, 3), (3, 1)]
            result = -1 if result else 1
    elif s == 0:
        if len(np.unique(k)) == 3:
            result = tuple(k) in [(1, 2, 3), (2, 3, 1), (3, 1, 2)]
            result = -1 if result else 1
        else:
            result = 0
    else:
        result = 0
    
    if debug:
        print(k1, k2, k3, ' ', code, ' ', result)
    else:
        if code == 0:
            print('signed char table[] = {', end='')
        print(int(result), end='')
        if code < 63:
            print(', ', end='')
        else:
            print('};')