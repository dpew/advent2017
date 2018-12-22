#!/usr/bin/env python

import sys
import math
import pprint
import re
import doctest
import itertools
from collections import defaultdict
from functools import reduce
from heapq import heappush, heappop


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

TERRAIN= {
   0: '.',
   1: '=',
   2: '|'
}

TOOLS = ('T', 'C', 'N')

# permitted tools in given terrian
ALLOWED = {
   0: ('T', 'C'),
   1: ('C', 'N'),
   2: ('T', 'N')
}

def addpos(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def distance(p1, p2):
    '''
        >>> distance((8, 9), (8, 9))
        0
        >>> distance((8, 9), (9, 9))
        1
        >>> distance((8, 9), (9, 10))
        2
        >>> distance((8, 9), (9, 7))
        3
    '''
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


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

    def type(self, x, y):
        return self.at(x, y) % 3

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

    def choices(self, node, cost):
        '''
             returns generator of (cost, node(pos, tool))
             a node is a tuple of (pos, tool)
        '''
        pos, tool = node
        
        for d in DIRS.values():
            p = addpos(pos, d)
            if p[0] < 0 or p[0] > self.width or p[1] < 0 or p[1] > self.height:
                continue
            newtype = self.type(*pos)
            for newtool in TOOLS:
                if newtool in ALLOWED[newtype]:
                    nc = (cost + (1 if (newtool == tool) else 8), (p, newtool))
                    # print nc
                    yield nc

    def mindist(self, source=(0, 0), target=None):
        '''
            >>> g = GeoIndex(10, 10, 510)
            >>> cost, node = g.mindist()
            >>> cost
            45
        '''
        if not target:
            target = (self.width, self.height)

        totaldist = distance(source, target)

        node=(source, 'T')
        SEEN = defaultdict(lambda: 100000000000)
        SEEN[node] = 0
        paths=[]
        heappush(paths, (0, totaldist, node))
        # heappush(paths, (0, node))

        while True:
            #p2 = list(paths)
            #print [ heappop(p2) for i in range(len(p2)) ]
            cost, dist, node = heappop(paths)
            SEEN[node] = cost
            #print cost, dist, node, len(paths)
            #print cost, node, len(paths)

            if node[0] == target:
                return cost, node

           # returns list of (cost, node(pos, newtool))
            for newcost, newnode in self.choices(node, cost):
                if newnode not in SEEN:
                #if SEEN[newnode] > newcost:
                     heappush(paths, (newcost, totaldist - distance(target, newnode[0]), newnode))
        #              heappush(paths, (newcost, newnode))
                #     SEEN[newnode] = newcost

    def __repr__(self):
        out = ''
        for y in range(self.height + 1):
            out = out + ''.join(TERRAIN[self.type(x, y)] for x in range(self.width+1))
            out = out + '\n'
        return out


if len(sys.argv) > 1:
    import doctest
    doctest.testmod()
    sys.exit(3)

#depth=4845
#target=(6,770)
depth=510
target=(10,10)
print g.risk()
g = GeoIndex(target[0], target[1], depth)
print g.mindist()

