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
        self.generation = 0
        self.seen = {}
        self.counts = {}

    def grow(self):
        self.pots = grow(self.pots, self.defs)
        self.start = self.start - 2
        d, self.pots = trim(self.pots)
        self.start += d
        self.counts[self.generation] = self.count()
        self.generation += 1

    def isseen(self):
        try:
           return self.seen[self.pots]
        except KeyError:
           self.seen[self.pots] = (self.generation, self.start, self.count())
           return None

    def count(self, start=None):
        s = start or self.start
        return sum(e + s if x == '#' else 0 for e, x in enumerate(self.pots))

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

       gen = 50000000000
       #gen = 200
       #gen = 31913
       #print pots, potdefs
       print pots
       #s = sum(1 if x == '#' else 0 for x in pots)
       s = p.sum()
       while True:
          p.grow()
          #print p.generation, p.count(), p.pots, p.start
          seen = p.isseen()
          if seen:
              print "FOUND", seen
              g = gen % seen[0]
              print p.generation, p.pots, g, p.counts[g]
              print gen, p.count(gen - (p.generation - seen[1])+1)
              break
              
          #print p.count(), p.pots
          #c = p.sum()
          #print p.count()
          #print x, c, s, pots

       print p.count()

