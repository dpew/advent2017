#!/usr/bin/env python

import sys
import math
import pprint
import re

def to_cut(s):
   '''
       >>> to_cut('#1 @ 1,3: 4x4')
       (1, 1, 3, 4, 4)
       >>> to_cut('#2 @ 3,1: 4x4')
       (2, 3, 1, 4, 4)
       >>> to_cut('#3 @ 5,5: 2x2')
       (3, 5, 5, 2, 2)
   '''
   return tuple(int(x) for x in filter(lambda x: x, re.split('[^0-9]',s)))

class Matrix(object):

    def __init__(self, size):
      line=[0 for x in xrange(size)]
      self.matrix=[list(line) for x in xrange(size)]
      self.width = size
      self.height = size

    def set(self, x, y, val):
        self.matrix[y][x] = val

    def get(self, x, y):
        '''
        '''
        try:
            return self.matrix[y][x]
        except IndexError:
            return 0

    def add_cut(self, cut):
       if not cut:
          return
       print cut
       for x in range(cut[1], cut[1] + cut[3]):
           for y in range(cut[2], cut[2] + cut[4]):
               val = self.get(x, y)
               self.set(x, y, cut[0] if val == 0 else -1 )

    def __repr__(self):
        return pprint.pformat(self.matrix)
        


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        import doctest
        doctest.testmod()
    else:
    	m = Matrix(1000)
        with open(sys.argv[1]) as f:
            for cut in f.readlines():
                m.add_cut(to_cut(cut))
        print "here"
        count=0
        print repr(m)
        for y in xrange(m.height):
           for x in xrange(m.width):
               if m.get(x, y) == -1:
                   count+=1
            
        print count
