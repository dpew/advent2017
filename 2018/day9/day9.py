#!/usr/bin/python

import sys
import math
import pprint
import re
import doctest
from collections import defaultdict


class Marbles(object):
    def __init__(self):
       self.marbles = [0]
       self.cur = 0

    def add(self, marble):
       a = 1 if len(self.marbles) < 1 else 2
       self.cur = (self.cur + a)
       if self.cur > len(self.marbles):
          self.cur -= len(self.marbles)
       self.marbles.insert(self.cur, marble)

    def remove(self):
       self.cur = self.cur - 7
       if self.cur < 0:
           self.cur += len(self.marbles)
       return self.marbles.pop(self.cur)

    def __repr__(self):
       s = ""
       for e, m in enumerate(self.marbles):
           if e == self.cur:
              s += " (%2d)" % (m, )
           else:
              s += "  %2d " % (m, )
       return s


if __name__ == '__main__':
    if len(sys.argv) == 1:
       import doctest
       doctest.testmod()
       sys.exit(0)
    
    players=int(sys.argv[1])
    count=int(sys.argv[2])

    m = Marbles()
    p = [0] * players
    cp = 0
    #print cp, m
    for x in xrange(1, count+1):
       if x > 0 and x % 23 == 0:
          p[cp] += x + m.remove()
       else:
          m.add(x)
       #print "[%2d]: %s" % (cp+1, m)
       cp = (cp + 1) % players
    print max(p)
