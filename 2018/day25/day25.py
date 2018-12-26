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


if len(sys.argv) < 2:
    import doctest
    doctest.testmod()
    sys.exit(3)


with open(sys.argv[1]) as f:
    points = [ tuple(int(i) for i in tokenize(line.strip(), ",")) for line in f.readlines() ]

constellations=[[points.pop()]]

def constdistance(point, const):
    return min(mdistance(point, c) for c in const)

while points:
   con = constellations[-1]
   closest = min(points, key=lambda p: constdistance(p, con))
   if constdistance(closest, con) <= 3:
       con.append(closest)
   else:
       constellations.append([closest])

   points.remove(closest)


print len(constellations)
