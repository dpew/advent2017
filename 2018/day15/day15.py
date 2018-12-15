#!/usr/bin/env python

import sys
import math
import pprint
import re
import doctest
from collections import defaultdict

DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))
MAXDIST=100000

def addpos(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def sortpaths(paths):
    return sorted(paths, key=lambda p: (p[0][1], p[0][0]))

class Board(object):

    def __init__(self, grid, units):
        self.grid = grid
        self.units = units
        self.height = len(grid)
        self.width = max(len(g) for g in grid)
        self.reset()

    def get(self, pos):
        '''
            Returns (E|G|.|#,Unit)
        '''
        try:
            return (self.unitdict[pos].type, self.unitdict[pos])
        except KeyError:
            return (self.grid[pos[1]][pos[0]], None)

    def reset(self):
        self.unitdict = dict((u.pos, u) for u in self.units)

    def visit(self, visitors, criteria, pos, path=(), dist=0, maxdist=MAXDIST):
        if dist > maxdist:
           return visitors
  
        # if dist == 0, ignore the current position
        if dist > 0:
            at = self.get(pos)
            if not criteria(at):
                return visitors

            if visitors.distance(pos) < dist:
               return visitors

            # print "Distance", visitors.distance(pos)
            visitors.put(pos, dist, at, path)

        for d in DIRECTIONS:
            self.visit(visitors, criteria, addpos(pos, d), path=path + (pos,), dist=dist+1, maxdist=maxdist-1)
        return visitors

    def row(self, y):
        return ''.join(self.get((x, y))[0] for x in xrange(self.width))

    def __repr__(self):
        return '\n'.join(board.row(y) for y in xrange(self.height))

class Unit(object):

    def __init__(self, x, y, t, points=200, apower=3):
        '''
            x, y, type ('E' or 'G'))
        '''
        self.pos = (x, y)
        self.type = t
        self.seek = 'G' if t == 'E' else 'E'
        self.points = points
        self.apower = apower


    def move(self, board):
        '''
            Move the unit in the board.  Returns 0 = no moves, 1 a move possible
        '''
        visitors = board.visit(Visitors(), lambda c: c[0] in ('.', self.seek), self.pos)
        #pprint.pprint(visitors.positions)
        print visitors
        return 0

    def attack(self, board):
        '''
            Attacks adjacent units in board
        '''
        #visitors = board.visit(Visitors(), lambda c: c[0] in ('.', self.seek), self.pos, maxdist=1)
        #visitors.nearest()
        pass

    def __repr__(self):
        return "%s(%2d,%2d,pnt=%d,pwr=%d)" % (self.type, self.pos[0], self.pos[1], self.points, self.apower)

class Visitors(object):

    def __init__(self):
       self.positions = {}

    def put(self, pos, dist, at, path):
       try:
           self.positions[pos] = (dist, at, sortpaths((path, self.positions[pos][2]))[0])
       except KeyError:
           self.positions[pos] = (dist, at, path)

    def distance(self, pos):
       try:
           return self.positions[pos][0]
       except KeyError:
           return MAXDIST

    def __repr__(self):
       return pprint.pformat(dict((p, v) for p, v in self.positions.items() if v[1][0] != '.'))
       

if __name__ == '__main__':
    if len(sys.argv) == 1:
      import doctest
      doctest.testmod()
      sys.exit(0)


grid=[]
units=[]
width=0
with open(sys.argv[1]) as f:
    y=0
    for l in f.readlines():
        for x, c in enumerate(l):
            if c in ('G', 'E'):
                units.append(Unit(x, y, c))
        nl = l.replace('G', '.')
        nl = nl.replace('E', '.')
        grid.append(nl.rstrip())
        width = max(width, len(l))
        y+=1
    board = Board(grid, units)
    del units

    rnd = 0
    while True: 
        moves=0
        print rnd
        print board
        for u in sorted(board.units, key=lambda u: (u.pos[1], u.pos[0])):
            print u.type, u.pos
            moves+=u.move(board)
        if not moves:
            break
        rnd += 1

    points=sum(u.points for u in board.units)
    print rnd, points, rnd * points 
