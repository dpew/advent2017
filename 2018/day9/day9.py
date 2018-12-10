#!/usr/bin/env python

import sys
import math
import pprint
import re
import doctest
from llist import dllist
from collections import defaultdict


class Marbles(object):
    def __init__(self):
       self.marbles = dllist([0])
       self.cur = 0
       self.node = self.marbles.nodeat(0) # None #self.marbles.nodeat(0)

    def add(self, marble):
       a = 2 #1 if len(self.marbles) < 1 else 2
       self.node = self.marbles.nodeat(0) if not self.node.next else self.node.next
       #self.cur = (self.cur + a) % len(self.marbles)
       #for x in range(1):
#       if self.cur >= len(self.marbles):
#          self.cur -= len(self.marbles)
       self.node = self.marbles.insert(marble, self.node.next)
       #self.node = self.marbles.nodeat(0) if not self.node.next else self.node.next

    def remove(self):
       for x in range(7):
           self.node = self.marbles.last if not self.node.prev else self.node.prev
       #self.cur = self.cur - 7
       #if self.cur < 0:
       #    self.cur += len(self.marbles)
       #node = self.marbles.nodeat(self.cur)
       node = self.node
       self.node = self.marbles.nodeat(0) if not self.node.next else self.node.next
       return self.marbles.remove(node)

    def __repr__(self):
       s = ""
       for e, m in enumerate(self.marbles):
           if m == self.node.value:
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
       # print "[%2d]: %s" % (cp+1, m)
       cp = (cp + 1) % players
    print max(p)
