#!/usr/bin/python

import sys
import math
import pprint
import re
import doctest
from collections import defaultdict


def readlines(fname):
   with open(fname) as f:
       return [x.strip() for x in f.readlines()]

def collapse(s):
   '''
      >>> collapse('aAfoobar')
      'foobar'
      >>> collapse('aafoobar')
      'aafoobar'
      >>> collapse('aafoOBbar')
      'aafar'
   '''
   #p = re.compile(r'aA|bB|cC|dD|eE|fF') 
   #p = re.compile(r'(?=(\p{L}))(?=.*(?!\1))')
   #return s.replace(s, '')
   r = r'aA|bB|cC|dD|eE|fF|gG|hH|iI|jJ|kK|lL|mM|nN|oO|pP|qQ|rR|sS|tT|uU|vV|wW|xX|yY|zZ'
   r2 = ''.join([x.lower() if x.isupper() else x.upper() for x in r])
   p = re.compile(r + '|' + r2)
   return p.sub('', s, 10)

def reduce(polymer):
   '''
       >>> reduce('dabAcCaCBAcCcaDA')
       'dabCBAcaDA'
   '''
   l = len(polymer)
   while True:
      polymer = collapse(polymer)
      l2 = len(polymer) 
      if l2 == l:
          return polymer
      l = l2

def remove(polymer, unit):
   '''
       >>> remove('aaaBcCAdef', 'a')
       'BcCdef'
       >>> remove('dabAcCaCBAcCcaDA', 'c')
       'dabAaBAaDA'
   '''
   p = re.compile("(%s|%s)" % (unit.lower(), unit.upper())) 
   return p.sub('', polymer)


if len(sys.argv) > 1:
    input = readlines(sys.argv[1])[0]
    print len(input)
    print len(reduce(input))

    smallest=len(input)
    sunit=''
    for unit in xrange(ord('a'), ord('z')+1):
        unit = chr(unit)
        small = len(reduce(remove(input, unit)))
        if small < smallest:
            smallest = small
            sunit = unit
    print smallest, sunit
else:
    doctest.testmod()
