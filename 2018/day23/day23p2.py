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
    nanobots = []
    for l in f.readlines():
        nanobots.append(tuple(int(t) for t in tokenize(l, 'pos=<>, r=')))



def countdist(bot):
    return sum(1 if mdistance(bot[:3], n[:3]) <= n[3] else 0 for n in nanobots)
     
def mindist(bot):
    return mdistance((0, 0, 0), bot[:3])

def intersect(bot1, bot2):
    return mdistance(bot1[:3], bot2[:3]) < (bot1[3] + bot2[3])

def countintersect(bot):
    return sum(1 if intersect(bot, n) else 0 for n in nanobots)

def findmax(pmin, pmax, width):
    maxbots=[]
    maxcount=0
    for x in xrange(pmin[0]-(width/2), pmax[0]+(width/2), width):
       for y in xrange(pmin[1]-(width/2), pmax[1]+(width/2), width):
          for z in xrange(pmin[2]-(width/2), pmax[2]+(width/2), width):
              bot = (x, y, z, width)
              c = countintersect(bot)
              if (c > maxcount):
                  maxbots = [bot]
                  maxcount = c
              elif c == maxcount:
                  maxbots.append(bot)
    return maxbots
    
maxnano = max(nanobots, key=lambda k: k[3])
print "before"
nmin, nmax = minmax(nanobots)

print sum(1 if mdistance(maxnano[:3], n[:3]) <= maxnano[3] else 0 for n in nanobots)

print "MIN", nmin, "MAX", nmax
pmin, pmax = nmin, nmax
width = (nmax[0] - nmin[0]) / 5
while width > 0:
    maxes = findmax(pmin, pmax, width)
    print maxes 
    maxv = min(maxes, key=lambda x: mindist(x[:3]))
    print maxv, mindist(maxv), countintersect(maxv)
    width = width / 2
    pmin = addpos(maxv[:3], (-width, -width, -width))
    pmax = addpos(maxv[:3], (width, width, width))
