#!/usr/bin/env python

import sys
import math
import pprint
import re
import doctest
from collections import defaultdict

class Grid(object):

    def __init__(self, grid, width, height):
        self.grid = grid
        self.width = width
        self.height = height

    def get(self, pos):
        return self.grid[pos[1]][pos[0]]

    def __repr__(self):
        return ''.join(self.grid)

class Unit(object):

    def __init__(self, x, y, t, points=200, apower=3):
        '''
            x, y, type ('E' or 'G'))
        '''
        self.pos = (x, y)
        self.type = t
        self.points = points
        self.apower = apower


    def move(self, grid):
        '''
            Move the unit in the grid.  Returns 0 = no moves, 1 a move possible
        '''
        return 0

    def attack(self, grid):
        '''
            Attacks adjacent units in grid
        '''
        pass


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
    thegrid = Grid(grid, width, y)

    rnd = 0
    while True: 
        moves=0
        for u in units:
            moves+=u.move(thegrid)
        if not moves:
            break
        rnd += 1

    points=sum(u.points for u in units)
    print rnd, points, rnd * points 
