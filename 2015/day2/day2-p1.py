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
    size = 2 * sum(sizes) + min(sizes)

    print "Box ", e, size
    total += size

print total
