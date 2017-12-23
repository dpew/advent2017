#!/usr/bin/env python

import sys
from collections import defaultdict


def getboxes():
    with open(sys.argv[1]) as f:
        for l in f.readlines():
            yield [int(x) for x in l.strip().split('x')]
 

total=0
for e, b in enumerate(getboxes()):
    sizes = [b[0] * b[1], b[0] * b[2], b[1] * b[2]]
    circum = [b[0] + b[1], b[0] + b[2], b[1] + b[2]]
    bow = 2 * min(circum)
    cube = reduce(lambda x, y: x * y, b)

    print "Box ", e, bow, cube, bow + cube
    total += bow + cube

print total
