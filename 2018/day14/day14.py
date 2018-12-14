#!/usr/bin/env python

import sys
import math
import pprint
import re
import doctest
from llist import dllist
from collections import defaultdict

def combine(recipies, e1, e2):
    i1 = int(recipies[e1])
    i2 = int(recipies[e2])
    r = recipies + str(i1 + i2)
    #print i1, i2, e1, e2, r
    e1 = (e1 + i1 + 1) % len(r) 
    e2 = (e2 + i2 + 1) % len(r) 
    if e2 == e1:
       e2 = (e2 + 1) % len(r)
    return (r, e1, e2)

    
def printr(recipies, pos):
    print pos, recipies[pos:pos+10], recipies[pos-5:pos]
    

if __name__ == '__main__':
    if len(sys.argv) == 1:
      import doctest
      doctest.testmod()
      sys.exit(0)


    recipies='37'
    e1=0
    e2=1
    for x in xrange(2028):
        recipies, e1, e2 = combine(recipies, e1, e2)

    #print recipies[9: 19]
    #print recipies[5: 15]
    #print recipies[18: 28]
    #print recipies[2018: 2028]

    recipies='330121'
    #c=330121
    c=2018
    recipies='37'
    find='303121'
    #find='59414'
    e1=0
    e2=1
    while True: 
        recipies, e1, e2 = combine(recipies, e1, e2)
        if recipies[:-10].find(find) >= 0:
            p = recipies.find(find) 
            printr(recipies, p)
            break
        

    #printr(recipies, 9)
    #printr(recipies, 5)
    #printr(recipies, 18)
    #printr(recipies, 2018)
    #printr(recipies, c)
    #print recipies[9: 19]
    #print recipies[18: 28]
    #print recipies[2018: 2028]
