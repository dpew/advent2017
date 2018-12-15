#!/usr/bin/env python

import sys
import math
import pprint
import re
import doctest
from collections import defaultdict

class Board(object):

    def __init__(self, grid, units):
        self.grid = grid
        self.units = units
        self.height = len(grid)
        self.width = max(len(g) for g in grid)
        self.reset()

    def get(self, pos):
        try:
            return self.unitdict[pos].type
        except KeyError:
            return self.grid[pos[1]][pos[0]]

    def reset(self):
        self.unitdict = dict((u.pos, u) for u in self.units)

    def row(self, y):
        return ''.join(self.get((x, y)) for x in xrange(self.width))

    def __repr__(self):
        return '\n'.join(board.row(y) for y in xrange(self.height))

class Unit(object):

    def __init__(self, x, y, t, points=200, apower=3):
        '''
            x, y, type ('E' or 'G'))
        '''
        self.pos = (x, y)
        self.type = t
        self.points = points
        self.apower = apower


    def move(self, board):
        '''
            Move the unit in the board.  Returns 0 = no moves, 1 a move possible
        '''
        return 0

    def attack(self, board):
        '''
            Attacks adjacent units in board
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
