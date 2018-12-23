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
    def __init__(self, width, height, depth, target=None):
        self.width = width
        self.height = height
        self.depth = depth
        self.target = target if target else (width, height)

        self.geoindex = {}
        for y in range(height+1):
           for x in range(width + 1):
              self.geoindex[(x, y)] = self.at(x, y)

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
        if x == self.target[0] and y == self.target[1]:
            return self.erode(0)
        if x == 0:
            return self.erode(y * 48271)
        if y == 0:
            return self.erode(x * 16807)
        try:
            return self.geoindex[(x, y)]
        except KeyError, e:
        #    print "KEY ERROR", x, y
        #    raise e
            
            return self.erode(self.at(x, y-1) * self.at(x-1, y))

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
        for y in range(self.target[1]+1):
            risk += sum(self.at(x, y) % 3 for x in range(self.target[0]+1))
        return risk

    def choices(self, node, cost):
        '''
             returns generator of (cost, node(pos, tool))
             a node is a tuple of (pos, tool)
        '''
        pos, tool = node
        mytype = self.type(*pos)
        
        for d in DIRS.values():
            p = addpos(pos, d)
            if p[0] < 0 or p[1] < 0:
                continue
            if p == self.target:
                yield (cost + (1 if ('T' == tool) else 8), (p, 'T'))
                return
            newtype = self.type(*p)
            for newtool in TOOLS:
                if newtool in ALLOWED[newtype] and newtool in ALLOWED[mytype]:
                    nc = (cost + (1 if (newtool == tool) else 8), (p, newtool))
                    # print nc
                    yield nc

    def mindist(self, source=(0, 0), target=None):
        if not target:
            target = self.target

        totaldist = distance(source, target)
        #print totaldist

        node=(source, 'T')
        SEEN = defaultdict(list)
        #SEEN[node] = 0
        paths=[]
        heappush(paths, (0, totaldist, node, None))
        # heappush(paths, (0, node))
        maxdist = totaldist

        while True:
            cost, dist, node, parent = heappop(paths)
            if node in SEEN:
               continue
            #print node
            SEEN[node] = True # SEEN[parent] + [node]
            #if dist < 2:
                #print cost, dist, node, len(paths)
                #p2 = list(paths)
                #print [ heappop(p2) for i in range(min(len(p2), 10)) ]
            #    maxdist = dist
            #print cost, node, len(paths)

            if node[0] == target:
                return cost, node, SEEN[node]

           # returns list of (cost, node(pos, newtool))
            for newcost, newnode in self.choices(node, cost):
                if newnode not in SEEN:
#                     if newnode[0] != target or newnode[1] == 'T':
                         heappush(paths, (newcost, distance(target, newnode[0]), newnode, node))
#                     else:
#                         print "SKIPPING", newnode
        #              heappush(paths, (newcost, newnode))

    def __repr__(self):
        out = ''
        for y in range(self.height + 1):
            out = out + ''.join(TERRAIN[self.type(x, y)] for x in range(self.width+1))
            out = out + '\n'
        return out

    def render(self, path):
        el = dict(path)
        out = ''
        for y in range(self.height + 1):
            out = out + ''.join(el[(x, y)] if (x, y) in el else TERRAIN[self.type(x, y)] for x in range(self.width+1))
            out = out + '\n'
        return out

def pathcost(path):
    p1 = path[0] 
    changetool=0
    move=0
    for p2 in path[1:]:
        move+=1
        if p2[1] != p1[1]:
            changetool +=1
        p1 = p2
        
    return move, changetool, move + 7 * changetool


if len(sys.argv) > 1:
    import doctest


if len(sys.argv) > 1:
    import doctest
    doctest.testmod()
    sys.exit(3)

depth=4845
target=(6,770)
#depth=510
#target=(10,10)
g = GeoIndex(2000, 2000, depth, target)
#g = GeoIndex(20, 20, depth, target)
print g.risk()
print g
print "computing"
cost, node, path = g.mindist()
#print g.render(path)
#print pathcost(path)
print cost, node

