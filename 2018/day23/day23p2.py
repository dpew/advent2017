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


def nanodist(p1, nbot):
    '''
        >>> nanodist((0, 0, 0), (3, 3, 3, 2))
        (1, 1, 1)
        >>> nanodist((0, 0, 0), (-3, -3, -3, 2))
        (-1, -1, -1)
        >>> nanodist((10, 12, 12), (50, 50, 50, 200))
        (0, 0, 0)
        >>> nanodist((10, 12, 12), (50, 50, 50, 100))
        (0, 0, 0)
    '''
    d = subpos(nbot[:3], p1)
    return tuple(x - int(math.copysign(nbot[3], x)) for x in d)

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

def countintersect(minp, maxp):
    #pmin = addpos(bot[:3], [bot[3]] * 3)
    #pmax = addpos(bot[:3], [-bot[3]] * 3)
    #return sum(1 if cubeintersect(pmin, pmax, n[:3], n[3]) else 0 for n in nanobots)
    s = sum(1 if cubeintersect(minp, maxp, n[:3], n[3]) else 0 for n in nanobots)
    #print "Countintersect min=%s max=%s => %d" % (minp, maxp, s)
    return s

def findmaxwrong(pmin, pmax, split):
    #print "findmax %s %s %d" % (pmin, pmax, split)
    maxbots=[]
    maxcount=0
    splits = [ (pmax[0] - pmin[0]) / split, (pmax[1] - pmin[1]) / split, (pmax[2] - pmin[2]) / split]
    #print splits
    srange = lambda n, x, s: xrange(n, x + s, 1 if s == 0 else s)
    for x in srange(pmin[0], pmax[0], splits[0]):
       for y in srange(pmin[1], pmax[1], splits[1]):
          for z in srange(pmin[2], pmax[2], splits[2]):
              p1 = (x, y, z)
              p2 = addpos(p1, splits)
              c = countintersect(p1, p2)
              if (c > maxcount):
                  maxbots = [(p1, p2) ]
                  maxcount = c
              elif c == maxcount:
                  maxbots.append((p1, p2))
    return c, maxbots

def square(v):
    return v * v

def mulvector(mult, vector):
    return tuple(map(lambda x: mult * x, vector))

def findneighbor(position, scale):
    total = 0
    vectors = []
    for p in directions(3):
        neighbor = addpos(position, mulvector(scale, p))
        weight = square(countdist(neighbor)) # / mdistance(position, neighbor)
        # print weight, neighbor
        vectors.append(tuple(map(lambda x: x * weight, subpos(neighbor, position))))
        total += weight

    #print "VECTORS"
    #pprint.pprint( vectors)

    # sum the mean vectors, divide by total weight
    newvector = tuple(map(lambda x: x/total, reduce(addpos, vectors)))
    #print newvector
    return addpos(position, newvector)


def findmindist(position, scale):
    least = mindist(position)
    count = countdist(position)
    last = (0, 0, 0)
    while last != position:
        last = position
        for p in directions(3):
            neighbor = addpos(position, mulvector(scale, p))
            if mindist(neighbor) < least:
                c = countdist(neighbor)
                if c >= count:
                    position = neighbor
                    least = mindist(neighbor)
                    count = c
          #          print "FOPUND"
    return position


print sum(n[3] for n in nanobots)/len(nanobots)
print min(n[3] for n in nanobots)
print max(n[3] for n in nanobots)
print minmax(*nanobots)

minnano = max(nanobots, key=countdist)

maxcount=0
ndist = minnano[:3]
last=(0, 0, 0)
ndist=(16833872, 19978022, 16361388)
while ndist != last:
    c = countdist(ndist)
    if c != maxcount:
       print "P %s, Countdist %d, Max %d" % (ndist, c, maxcount)
    maxcount = max(c, maxcount)
    last = ndist
    ndist = findneighbor(ndist, 500000)


scale=500000
last=(0,0,0)
while scale > 0:
    last = ndist
    ndist = findmindist(ndist, scale)
    print "P %s, Countdist %d, Scale %d" % (ndist, countdist(ndist), scale)
    scale=scale/2
    
print "P %s, Countdist %d, Mindist %d" % (ndist, countdist(ndist), mindist(ndist))
sys.exit(1)
   


print "before"
nmin, nmax = minmax(*nanobots)

print sum(1 if mdistance(maxnano[:3], n[:3]) <= maxnano[3] else 0 for n in nanobots)

print "MIN", nmin, "MAX", nmax
pmin, pmax = nmin, nmax
ranges = [(pmin, pmax)]
print pmax, pmin
width = mdistance(pmax, pmin)
while width > 0:
    maxcount = 0
    newranges = []
    for pmin, pmax in ranges:
        c, maxes = findmax(pmin, pmax, 5)
        if c > maxcount:
            newranges = maxes
            maxcount = c
        elif c == maxcount:
            newranges.extend(maxes)
    ranges = newranges
    print "Count %d, Width %d: %s" % (maxcount, width, newranges)
    width = mdistance(*ranges[0])
    print "newwidth", width
    sys.stdout.flush()


maxcount=0
point=(10000000000, 1000000000, 1000000000000)
for p1 in itertools.chain(*ranges):
    c = countdist(p1)
    if c > maxcount:
        maxcount = c
        point = p1
    elif c == maxcount:
        if mindist(p1) < mindist(point):
            point = p1
    
print point, mindist(point)
