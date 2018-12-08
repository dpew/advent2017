#!/usr/bin/python

import sys
import math
import pprint
import re
import doctest
from collections import defaultdict


def sumit(vals, i):
    nodevals=defaultdict(lambda: 0)
    s=0
    p=0
    c = vals[i]
    m = vals[i+1]
    i+=2
    for c2 in xrange(c):
        s2,p = sumit(vals, i)
 #       print "Adding ", c2, s2
        nodevals[c2+1] = s2
        i = p
    if c == 0:
      mysum=0
      for m2 in xrange(m):
    #    print "sum", vals[i]
        mysum += vals[i]
        i += 1 
      s += mysum
    elif c != 0:
      for m2 in xrange(m):
        print "Adding child ", vals[i], nodevals[vals[i]], s
        s += nodevals[vals[i]]
        i += 1 
    #print "return", s, i
    #print "mynode", nodevals
    return s, i

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        import doctest
        doctest.testmod()
    else:
        x=[]
        with open(sys.argv[1]) as f:
          vals = [ int(x) for x in f.readline().strip().split()]
          #print vals
          print sumit(vals, 0)[0]
