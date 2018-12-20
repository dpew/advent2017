#!/usr/bin/env python

import sys
import math
import pprint
import re
import doctest
from collections import defaultdict
from functools import reduce


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

def navigate(path):
   allpaths = []
   paths = [[]]
   i, ln = 0, len(path)
   while i < ln:
       p = path[i]
       print p, i, paths
       if p in DIRS.keys():
           for mypath in paths:
              mypath.append(p)
           i += 1
       elif p == '(':
           newpaths = []
           children, seen = navigate(path[i+1:])
           print seen
           i  = i + seen + 1
           mx = max(len(c) for c in children)
           for mypath in paths:
             for c in children:
               if len(c) >= mx:
                  newpath = list(mypath)
                  newpath.extend(c)
                  newpaths.append(newpath)
           paths = newpaths
       elif p == '|':
           allpaths.extend(paths)
           paths = [[]]
           i += 1
       elif p == ')':
           break
       else:
           i += 1
   allpaths.extend(paths)
   return allpaths, i+1
   

def addpos(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def measure(path):
    return reduce(addpos, (DIRS[p] for p in path))

with open(sys.argv[1]) as f:
    path = f.readline()

    paths, seen = navigate(path)
    p2 = [ ''.join(p) for p in paths ]
    pprint.pprint(p2)
    minpath = min(paths, key=lambda p: measure(p)) 
    #print paths
    #print max(measure(p) for p in paths) 
    print len(minpath), ''.join(minpath)

