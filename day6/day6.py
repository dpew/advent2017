#!/usr/bin/env python

import sys
from copy import deepcopy

class Banks(object):
    def __init__(self, iterable):
        self.banks = [int(x) for x in iterable]

    def __hash__(self):
        return hash('.'.join(str(x) for x in self.banks))

    def __repr__(self):
        return repr(self.banks)

    def __eq__(self, other):
        return self.banks == other.banks

    def rebalance(self):
        rebal = list(self.banks)
        pos = rebal.index(max(rebal))
        val = rebal[pos]
        rebal[pos] = 0
        for x in xrange(val):
            pos = (pos + 1) % len(rebal)
            rebal[pos] += 1
        return Banks(rebal)


with open(sys.argv[1]) as f:
   banks=Banks(f.readline().split())

seen={} # bankconfig: move
move=0
while banks not in seen:
    seen[banks] = move
    move += 1
    print move, banks
    banks = banks.rebalance()

print move
print move - seen[banks]
