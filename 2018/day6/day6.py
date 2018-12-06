#!/usr/bin/python

import sys
import math
import pprint
import re
import doctest
from collections import defaultdict


class Grid(object):

    def __init__(self):
        self.minX = 100000
        self.maxX = -100000
        self.minY = 100000
        self.maxY = -100000
    
    def expand(self, x, y):
        self.minX = min(self.minX, x)
        self.minY = min(self.minX, y)
        self.maxX = max(self.maxX, x)
        self.maxY = max(self.maxY, y)

    def makegrid(self):
        width = self.maxX - self.minX + 1
        height = self.maxY - self.minY + 1
        self.grid = [None] * width
        for x in xrange(0, width):
            self.grid[x] = [ None ] * height
        self.width = width
        self.height = height
       
    def getmax(self, x, y):
        return self.grid[x - self.minX][y - self.minY] 

    def setmax(self, x, y, point, dist):
        last = self.getmax(x, y)
        edge = x == self.minX or x == self.maxX or y == self.minY or y == self.maxY
        if last and last[0]:
            last[0].reduce(edge)
        self.grid[x - self.minX][y - self.minY] = (point, dist)
        if point:
            point.increase(edge)

    def setval(self, x, y, point, dist):
        d = self.getmax(x, y)
        if not d or dist < d[1]:
        #    print "setval(%s): %d, %d: %d" %( point, x, y, dist)
        #    print "New Min"
            self.setmax(x, y, point, dist)
        elif d and d[1] == dist:
        #    print "setval(%s): %d, %d: %d" %( point, x, y, dist)
        #    print "Same Min"
            self.setmax(x, y, None, dist)

    def __repr__(self):
        return "grid<%d, %d, %d, %d>" % (self.minX, self.minY, self.maxX, self.maxY)
            


class Point(object):
    def __init__(self, name, x, y):
       self.name = name
       self.count = 0
       self.x = x
       self.y = y
       self.edgecount = 0

    def reduce(self, edge):
       self.count -= 1
       if edge:
           self.edgecount -= 1

    def increase(self, edge):
       self.count += 1
       if edge:
           self.edgecount += 1

    def __repr__(self):
        return "point<%s, %d, %d: %d, %d>" % (self.name, self.x, self.y, self.count, self.edgecount)

def distance(x, y, x1, y1):
    '''
        >>> distance(8, 9, 8, 9)
        0
        >>> distance(8, 9, 9, 9)
        1
        >>> distance(8, 9, 9, 10)
        2
        >>> distance(8, 9, 9, 7)
        3
    '''
    return abs(x1 - x) + abs(y1 - y)

def printsec(sec):
    if sec is None:
        return "E   "
    if sec[0]:
        return "%s:%2d" % (sec[0].name, sec[1])
    return '.   '

def printgrid(g):
   print "grid:"
   for y in xrange(g.minY, g.height):
       x = [ printsec(g.getmax(x, y)) for x in xrange(g.minX, g.width) ]
       print x

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        import doctest
        doctest.testmod()
    else:
        count=0
        grid = Grid()
        points = []
        with open(sys.argv[1]) as f:
            for cut in f.readlines():
                count += 1
                c=cut.split(',')
                p = Point(str(count), int(c[0]), int(c[1]))
                grid.expand(p.x, p.y)
                points.append(p)

        print grid
        grid.makegrid()
        for p in points:
            for y in xrange(grid.minY, grid.height):
                for x in xrange(grid.minX, grid.width):
                     grid.setval(x, y, p, distance(x, y, p.x, p.y))
       #     printgrid(grid)
       #     sys.exit(1)

        maxarea=0
        for p in points:
            print p
            if p.edgecount == 0:
                maxarea = max(maxarea, p.count)
        #printgrid(grid)
        print maxarea
