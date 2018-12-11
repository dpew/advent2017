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

pastval={}
def power2(serial, x, y):
    try:
        return pastval[(x, y)]
    except KeyError:
        p = power(serial, x, y)
        pastval[(x, y)] = p
        return p

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

gridp={}
def gridpower2(serial, x, y, size):
    '''
       >>> gridpower2(18, 33, 45, 3)
       29
    '''
    if size == 1:
        s = power2(serial, x, y)
        gridp[(x, y, 1)] = s
        return s
    else:
        try:
             s = gridp[(x, y, size-1)]
        except KeyError:
             s = gridpower2(serial, x, y, size-1)

    for x2 in xrange(x, x+size):
        s += power2(serial, x2, y+size-1)
    for y2 in xrange(y, y+size-1):
        s += power2(serial, x+size-1, y2)
    gridp[(x, y, size)] = s
    return s
    
if __name__ == '__main__':
    if len(sys.argv) == 1:
      import doctest
      doctest.testmod()
      sys.exit(0)


    serial = int(sys.argv[1])
    mp = 0
    mx = -1
    my = -1
    ms = 0
    for s in xrange(3, 297):
      print s
      for x in xrange(0, 300-s):
        for y in xrange(0, 300-s):
            mp2 = gridpower2(serial, x, y, s)
            if mp2 > mp:
               mp, mx, my, ms = mp2, x, y, s
   
      print mp, mx, my, ms
