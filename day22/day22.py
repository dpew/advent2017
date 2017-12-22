#!/usr/bin/env python

import sys
import pprint
import re
from collections import defaultdict


grid=defaultdict(lambda: '.')

def parse_line(row, line):
    c = 0
    for e, x in enumerate(line.strip()):
        print "INPUT", line, row, e
        grid[(e, row)] = x
        c = max(c, e)
    return c


with open(sys.argv[1]) as f:
    rows = 0
    cols = 0
    for row, l in enumerate(f.readlines()):
        cols = parse_line(row, l.strip())
        rows=max(row, rows)

LEFT = {
   (0, -1): (-1, 0),
   (-1, 0): (0, 1),
   (0, 1): (1, 0),
   (1, 0): (0, -1)}

RIGHT = {
   (0, -1): (1, 0),
   (-1, 0): (0, -1),
   (0, 1): (-1, 0),
   (1, 0): (0, 1)}

REVERSE = {
   (0, -1): (0, 1),
   (-1, 0): (1, 0),
   (0, 1): (0, -1),
   (1, 0): (-1, 0)}

def left(pos):
    return LEFT[pos]

def right(pos):
    return RIGHT[pos]

def reverse(pos):
    return REVERSE[pos]

def print_grid(pos):
    for y in xrange(-5, 5):
       print ''.join(('O' if pos[0] == x and pos[1] == y else grid[(x,y)]) for x in xrange(-5, 5))
    print '----------------------'

direction=(0, -1)
print_grid((1,1))
print rows, cols
count=0
pos=(int(rows/2),int(cols/2))
for x in xrange(10000000):
    #print 'interation', x
    #print_grid(pos)
    s = grid[pos]
    if s == '#':
        grid[pos] = 'F'
        direction=right(direction)
    elif s == '.':
        grid[pos] = 'W'
        direction=left(direction)
    elif s == 'W':
        count+=1
        grid[pos] = '#'
    elif s == 'F':
        grid[pos] = '.'
        direction=reverse(direction)
    #print "Before",  pos
    pos = (pos[0] + direction[0], pos[1] + direction[1])
    #print "after", pos
    #print_grid(pos)
print count


