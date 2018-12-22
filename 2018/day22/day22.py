#!/usr/bin/env python

import sys
import math
import pprint
import re
import doctest
import itertools
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

class GeoIndex(object):
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth

        self.geoindex = []
        for y in range(height+1):
           self.geoindex.append([0] * (width + 1))

        for y in range(height+1):
           for x in range(width + 1):
              self.geoindex[y][x] = self.at(x, y)

    def at(self, x, y):
        '''
            >>> g = GeoIndex(10, 10, 510)
            >>> g.at(0, 0)
            510
            >>> g.at(1, 0)
            17317
            >>> g.at(0, 1)
            8415
            >>> g.at(1, 1)
            1805
            >>> g.at(10, 10)
            510
        '''
        if x == self.width and y == self.height:
            return self.erode(0)
        if x == 0:
            return self.erode(y * 48271)
        if y == 0:
            return self.erode(x * 16807)
        return self.erode(self.geoindex[y-1][x] * self.geoindex[y][x-1])

    def erode(self, val):
        return (self.depth + val) % 20183

    def risk(self):
        '''
            >>> g = GeoIndex(10, 10, 510)
            >>> g.risk()
            114
        '''
        risk=0
        for y in range(self.height+1):
            risk += sum(self.at(x, y) % 3 for x in range(self.width+1))
        return risk
    




if len(sys.argv) > 1:
    import doctest
    doctest.testmod()
    sys.exit(3)

depth=4845
target=(6,770)
g = GeoIndex(target[0], target[1], depth)

print g.risk()
