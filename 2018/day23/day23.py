#!/usr/bin/env python

import sys
import os
import math
import pprint
import re
import doctest
import itertools
from collections import defaultdict
from functools import reduce

# create absolute mydir
mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(mydir, '../lib'))

from advent import *


UP=(0, -1)
DOWN=(0, 1)
LEFT=(-1, 0)
RIGHT=(1, 0)

DIRS={
   'N': UP,
   'S': DOWN,
   'W': LEFT,
   'E': RIGHT
}


def addpos(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def distance(p1, p2):
    '''
        >>> distance((8, 9), (8, 9))
        0
        >>> distance((8, 9), (9, 9))
        1
        >>> distance((8, 9), (9, 10))
        2
        >>> distance((8, 9), (9, 7))
        3
    '''
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


if len(sys.argv) < 2:
    import doctest
    doctest.testmod()
    sys.exit(3)

with open(sys.argv[1]) as f:
    nanobots = []
    for l in f.readlines():
        nanobots.append(tuple(int(t) for t in tokenize(l, 'pos=<>, r=')))

maxnano = max(nanobots, key=lambda k: k[3])
print sum(1 if mdistance(maxnano[:3], n[:3]) <= maxnano[3] else 0 for n in nanobots)
#pprint.pprint(nanobots)
