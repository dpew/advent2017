#!/usr/bin/env python

import sys
import math
import pprint
import re
import doctest
from collections import defaultdict


UP=(0, -1)
DOWN=(0, 1)
LEFT=(-1, 0)
RIGHT=(1, 0)


def addpos(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

ALL=(addpos(UP, LEFT), UP, addpos(UP, RIGHT),
     LEFT, RIGHT,
     addpos(DOWN, LEFT), DOWN, addpos(DOWN, RIGHT))


def newunit(current, counts):
   if current == '.':
       return '|' if counts['|'] >= 3 else current
   if current == '|':
      return '#' if counts['#'] >= 3 else current
   if current == '#':
      if counts['#'] > 0 and counts['|'] > 0:
         return '#'
      else:
         return '.'
   raise "BAD"
 
class Lumberyard(object):
    def __init__(self, lumber):
        self.lumber = lumber
        self.width = len(lumber[0])
        self.height = len(lumber)

    def count(self, pos):
        c = defaultdict(int)
        for p in ALL:
           c[self[addpos(p, pos)]] += 1
        return c

    def iterate(self):
        l = []
        for y in xrange(self.height):
            l.append([newunit(self[(x, y)], self.count((x, y))) for x in xrange(self.width)])
        return Lumberyard(l)

    def counttype(self, t):
        return sum(1 if i == t else 0 for i in repr(self))

    def __getitem__(self, pos):
        if pos[0] < 0 or pos[1] < 0:
           return 'X'
        try:
           return self.lumber[pos[1]][pos[0]]
        except IndexError:
           return 'X'

    def __repr__(self):
        str = ''
        for y in xrange(self.height):
           str += ''.join(self[(x, y)] for x in xrange(self.width))
           str += '\n'
        return str
            
        
def split(inp):
   '''
       >>> split('x=5, y=10..200')
       ('x', 5, 'y', 10, 200)
   '''
   s = re.split(r', |=|\.\.', inp)
   return (s[0], int(s[1]), s[2], int(s[3]), int(s[4]))

if __name__ == '__main__':
  if len(sys.argv) == 1:
      import doctest
      doctest.testmod()
      sys.exit(0)


with open(sys.argv[1]) as f:
    y=0
    inputs = []
    for l in f.readlines():
        inputs.append(l.rstrip())
    lumber = Lumberyard(inputs)
    print lumber[(6, 0)], lumber.count((6, 0))
    #sys.exit(1)


    repeat=defaultdict(list)
    curt = 0 
    for t in xrange(608):
        # print lumber
        tstr = repr(lumber)
        repeat[tstr].append(t)
        lumber = lumber.iterate()

    pprint.pprint([x for x in repeat.values() if len(x) > 1])
    #print lumber
    #print repeat[repr(lumber)] 

    t = lumber.counttype('|')
    y = lumber.counttype('#')
    print t, y, t*y

    lumber = lumber.iterate()
    t = lumber.counttype('|')
    y = lumber.counttype('#')
    print t, y, t*y

