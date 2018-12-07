#!/usr/bin/python

import sys
import math
import pprint
import re
import doctest
from collections import defaultdict


class Puzzle(object):

   def __init__(self):
       self.things={} #defaultdict(lambda: list())
       self.steps = set()

   def add(self, x, y):
      self.steps.add(x)
      self.steps.add(y)
      try:
          self.things[y].append(x)
      except KeyError:
          self.things[y] = [x]

   def next(self):
      remain=[]
      for s in self.steps:
          if s not in self.things.keys():
              remain.append(s)
      try:
          return sorted(remain)[0]
      except IndexError:
          return None

   def complete(self, x):
      self.steps.remove(x)
      for s in self.steps:
          if s in self.things and x in self.things[s]:
              self.things[s].remove(x)
              if len(self.things[s]) == 0:
                  del self.things[s]
      #self.things[x].remove(y)
      #if len(self.things[x]) == 0:
      #   del self.things[x]

   def finished(self, x):
      return x in self.things.keys()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        import doctest
        doctest.testmod()
    else:
        puzzle = Puzzle()
        with open(sys.argv[1]) as f:
          for cut in f.readlines():
             x = cut.split()
             puzzle.add(x[1], x[7])
        answer=[]
        print puzzle.steps
        while len(puzzle.steps):
            pprint.pprint(puzzle.steps)
            pprint.pprint(puzzle.things)
            x = puzzle.next()
            answer.append(x)
            puzzle.complete(x)
            print x

        print ''.join(answer)
       
            
#        print puzzle.start, puzzle.next()

      
