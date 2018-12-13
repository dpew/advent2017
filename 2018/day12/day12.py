#!/usr/bin/env python

import sys
import math
import pprint
import re
import doctest
from llist import dllist
from collections import defaultdict

def getp(x, pots):
    s = []
    for y in xrange(x-2, x+3):
        s.append('.' if (y < 0 or y >= len(pots)) else pots[y])
    #print ''.join(s), x, pots
    return ''.join(s)

def grow(pots, defs):
    return ''.join(defs[getp(x, pots)] for x in xrange(-2, len(pots) + 3))

def trim(pots):
    '''
       >>> trim('...#...##..')
       (3, '#...##')
       >>> trim('#####')
       (0, '#####')
    '''
    last=pots.rfind('#')
    first=pots.find('#')
    #return first, last
    return first, pots[first:last+1]

class Plants(object):
    def __init__(self, pots, defs):
        self.pots = pots
        self.defs = defs
        self.start = 0

    def grow(self):
        self.pots = grow(self.pots, self.defs)
        self.start = self.start - 2
        d, self.pots = trim(self.pots)
        self.start += d

    def count(self):
        return sum(e + self.start if x == '#' else 0 for e, x in enumerate(self.pots))

    def sum(self):
        return sum(1 if x == '#' else 0 for x in self.pots)

if __name__ == '__main__':
    if len(sys.argv) == 1:
      import doctest
      doctest.testmod()
      sys.exit(0)

    x=[]
    potdefs = defaultdict(lambda: '.') #{}
    with open(sys.argv[1]) as f:
       for x in f.readlines():
          pdef = x.strip().split()
          potdefs[pdef[0]] = pdef[2]

      # initial='#..#.#..##......###...###'
       initial='##..#..##....#..#..#..##.#.###.######..#..###.#.#..##.###.#.##..###..#.#..#.##.##..###.#.#...#.##..'
       pots=initial

       p = Plants(pots, potdefs)

       #print pots, potdefs
       print pots
       #s = sum(1 if x == '#' else 0 for x in pots)
       s = p.sum()
       for x in xrange(20):
          p.grow()
          print p.count(), p.pots
          #c = p.sum()
          #print p.count()
          #print x, c, s, pots

       print s

