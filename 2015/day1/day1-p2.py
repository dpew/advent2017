#!/usr/bin/env python

import sys
from collections import defaultdict

with open(sys.argv[1]) as f:
    elevator=f.readline()

ELEVATOR=defaultdict(lambda:0, {'(': 1, ')': -1})
floor=0
for m, f in enumerate(elevator):
    floor += ELEVATOR[f]
    if floor == -1:
        print m+1
