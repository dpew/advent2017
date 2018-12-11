#!/usr/bin/env python

import sys
import math
import pprint
import re
import doctest
from llist import dllist
from collections import defaultdict

def hundred(val):
    '''
       >>> hundred(935)
       9
       >>> hundred(1486)
       4
       >>> hundred(86)
       0
       >>> hundred(342586)
       5
    '''
    h = int(val / 100)
    h2 = int(h / 10) * 10
    return h - h2
 

def power(serial, x, y):
    '''
       >>> power(8, 3, 5)
       4
    '''
    rack = x + 10
    power = rack * y
    power = power + serial
    power = power * rack
    return hundred(power) - 5

def gridpower(serial, x, y):
    '''
       >>> gridpower(18, 33, 45)
       29
    '''
    a = []
    for x2 in xrange(x, x+3):
        for y2 in xrange(y, y+3):
            a.append(power(serial, x2, y2))
    return sum(a)
    
    
if __name__ == '__main__':
    if len(sys.argv) == 1:
      import doctest
      doctest.testmod()
      sys.exit(0)


    serial = int(sys.argv[1])
    mp = 0
    mx = -1
    my = -1
    for x in xrange(0, 297):
        for y in xrange(0, 297):
            mp2 = gridpower(serial, x, y)
            if mp2 > mp:
               mp, mx, my = mp2, x, y
   
    print mp, mx, my 
