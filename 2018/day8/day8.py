#!/usr/bin/python

import sys
import math
import pprint
import re
import doctest
from collections import defaultdict


def sumit(vals, i):
    #print i, vals[i::]
    s=0
    p=0
    c = vals[i]
    m = vals[i+1]
    i+=2
    for c2 in xrange(c):
        s2,p = sumit(vals, i)
        s += s2
        i = p
    for m2 in xrange(m):
    #    print "sum", vals[i]
        s += vals[i]
        i += 1 
    #print "return", s, i
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
