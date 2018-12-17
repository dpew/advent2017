#!/usr/bin/env python

import sys
import math
import pprint
import re
import doctest
from collections import defaultdict

DOWN=(0, 1)
LEFT=(-1, 0)
RIGHT=(1, 0)

def addpos(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

class Water(object):
    def __init__(self):
        self.water = defaultdict(lambda: '.')
        self.min = (2000, 0)
        self.max = (0, 0)
        self.seen  = defaultdict(lambda: False)

    def addclay(self, x, y):
        self.water[(x, y)] = '#'
        self.min = (min(x, self.min[0]), min(y, self.min[1]))
        self.max = (max(x, self.max[0]), max(y, self.max[1]))

    def fill(self, pos, direction='D'):
        #print self
        if self.seen[pos]:
            raise "BULLSHIT"
        #print pos, direction, self.seen[pos]
        self.seen[pos] = True
        hit = self[pos]
        if not hit:
           return False

        if hit == '~':
           return True

        if hit == '.':
           self.water[pos] = '|'
         
           down = addpos(DOWN, pos)
           if self.seen[down] or self.fill(down):
              left, right = addpos(LEFT, pos), addpos(RIGHT, pos)
              full = True
              if not self.seen[left]:
                 full = self.fill(left, 'L') and full
              if not self.seen[right]:
                 full = self.fill(right, 'R') and full
              if full:
                 self.water[pos] = '~'
              return full

        if hit == '#':
           return True

        #print "HERE", hit, self.water[pos]
        return False

    def __getitem__(self, pos):
        if pos[0] < self.min[0] or pos[0] > self.max[0]:
           return None
        if pos[1] < self.min[1] or pos[1] > self.max[1]:
           return None
          
        return self.water[pos]

    def __repr__(self):
        str = ''
        for y in xrange(self.min[1], self.max[1]+1):
           str += ''.join(self.water[(x, y)] for x in xrange(self.min[0], self.max[0]+1))
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


sys.setrecursionlimit(3000)
ground=Water()
with open(sys.argv[1]) as f:
    y=0
    for l in f.readlines():
        inputs = split(l)
        if inputs[0] == 'x':
            for y in xrange(inputs[3], inputs[4]+1):
                ground.addclay(inputs[1], y)
        else:
            for x in xrange(inputs[3], inputs[4]+1):
                ground.addclay(x, inputs[1])
        
#print ground.water
print ground.min, ground.max
ground.fill((500, 1))
print ground
print sum(1 if g in ('~', '|') else 0 for g in ground.water.values())
