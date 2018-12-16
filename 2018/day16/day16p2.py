#!/usr/bin/env python

import sys
import math
import pprint
import re
import doctest
from collections import defaultdict

registers=defaultdict(int)
registers=[0] * 4

OPS = {
   "addr": lambda a, b: reg(a) + reg(b),
   "addi": lambda a, b: reg(a) + b,
   "mulr": lambda a, b: reg(a) * reg(b),
   "muli": lambda a, b: reg(a) * b,
   "banr": lambda a, b: reg(a) & reg(b),
   "bani": lambda a, b: reg(a) & b,
   "borr": lambda a, b: reg(a) | reg(b),
   "bori": lambda a, b: reg(a) | b,
   "setr": lambda a, b: reg(a),
   "seti": lambda a, b: a,
   "gtir": lambda a, b: 1 if a > reg(b) else 0,
   "gtri": lambda a, b: 1 if reg(a) > b else 0,
   "gtrr": lambda a, b: 1 if reg(a) > reg(b) else 0,
   "eqir": lambda a, b: 1 if a == reg(b) else 0,
   "eqri": lambda a, b: 1 if reg(a) == b else 0,
   "eqrr": lambda a, b: 1 if reg(a) == reg(b) else 0
}

def reg(g): 
    #print "register ", g, registers[g]
    return registers[g]

def setreg(c, v):
    registers[c] = v

OPCMAP=defaultdict(set)

count=0

def dotest(before, after, values):
    global registers
    global count
    matches=0
    for o, r in OPS.items():
        registers = list(before)
        op=values[0]
        setreg(values[3], r(values[1], values[2]))
        if registers == after: 
            print "Match %d=%s before=%s after=%s values=%s" %(op, o, before, after, values)
            matches += 1
            OPCMAP[o].add(op)
        else:
            OPCMAP[o].discard(op)

    if matches >= 3:
        count += 1
        
    # print before, after, values 
    

#@if __name__ == '__main__':
  #if len(sys.argv) == 1:
  #    import doctest
  #    doctest.testmod()
  #    sys.exit(0)


#with open(sys.argv[1]) as f:
before=[]
values=[]
with open("day16p1.txt") as f:
    y=0
    for l in f.readlines():
        l = l.strip()
        print l
        if l.find("Before") >= 0:
            before = eval(l[7:])
        elif l.find("After") >= 0:
            after = eval(l[7:])
            dotest(before, after, values)
        else:
            if l.strip():
               values=[int(i) for i in l.split()]

print count
pprint.pprint(dict(OPCMAP))
OPCMAP2={}

while sum(1 for x in OPCMAP.values() if len(x) > 0):
    for r, op in OPCMAP.items():
        if len(op) == 1:
           val=list(op)[0]
           OPCMAP2[val] = r
           for k in OPCMAP.keys():
               OPCMAP[k].discard(val)

pprint.pprint(dict(OPCMAP))
pprint.pprint(OPCMAP2)
#sys.exit(1)
global registers
registers = [0] * 4
with open("day16p2.txt") as f:
  for l in f.readlines():
    values=[int(i) for i in l.split()]
    r = OPS[OPCMAP2[values[0]]]
    setreg(values[3], r(values[1], values[2]))    
    
print registers
