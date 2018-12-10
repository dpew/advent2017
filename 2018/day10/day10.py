#!/usr/bin/env python

import sys
import math
import pprint
import re
import doctest
from llist import dllist
from collections import defaultdict

class Graph(object):
    def __init__(self):
       self.minX = 100
       self.minY = 100
       self.maxX = -100
       self.maxY = -100
       self.points = set()

    def reset(self):
       self.minX = 100
       self.minY = 100
       self.maxX = -100
       self.maxY = -100
       self.points = set()

    def add(self, x, y):
       self.points.add((x, y))
       self.minX = min(self.minX, x)
       self.maxX = max(self.maxX, x)
       self.minY = min(self.minY, y)
       self.maxY = max(self.maxY, y)

    def minval(self):
       return (self.maxX - self.minX) * (self.maxY - self.minY)

    def __repr__(self):
       r = ""
       for y in xrange(self.minY, self.maxY+1):
          r += ''.join('#' if (x, y) in self.points else '.' for x in xrange(self.minX, self.maxX + 1))
          r += '\n'
       return r

class Point(object):
    def __init__(self, x, y, vx, vy):
       self.pos = (x, y)
       self.vel = (vx, vy)

    def pointat(self, t):
       '''
           >>> Point(3, 9, 1, -2).pointat(3)
           (6, 3)
        '''
       return (self.pos[0] + t*self.vel[0], self.pos[1] + t*self.vel[1])

if __name__ == '__main__':
    if len(sys.argv) == 1:
       import doctest
       doctest.testmod()
       sys.exit(0)
    
    points=[]
    with open(sys.argv[1]) as f:
        for line in (re.split('< *|> *|, ',x) for x in f.readlines()):
            points.append(Point(int(line[1]), int(line[2]), int(line[4]), int(line[5])))

    g = Graph()
    minp = ""
    minv = 1000000000000000
    mint = 0
    for t in xrange(100000):
        g.reset()
        for p in points:
            g.add(*p.pointat(t))
        minv2 = g.minval()
        print t, minv2
        if minv2 < minv:
            minv = minv2
            mint = t
        else:
            break
        
    g.reset()
    print mint
    for p in points:
        g.add(*p.pointat(mint))
    print g
        
