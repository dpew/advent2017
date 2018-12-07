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
       self.busy = set()

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
          if s not in self.things.keys() and s not in self.busy:
              remain.append(s)
      try:
          return sorted(remain)[0]
      except IndexError:
          return None

   def setbusy(self, x):
       self.busy.add(x)

   def complete(self, x):
      self.busy.remove(x)
      self.steps.remove(x)
      for s in self.steps:
          if s in self.things and x in self.things[s]:
              self.things[s].remove(x)
              if len(self.things[s]) == 0:
                  del self.things[s]
      #self.things[x].remove(y)
      #if len(self.things[x]) == 0:
      #   del self.things[x]

   def available(self):
      remain = []
      for s in self.steps:
          if s not in self.things.keys() and s not in self.busy:
              remain.append(s)
      return remain

   def waiting(self):
      s2 = set(self.steps)
      return s2.difference(self.available()).difference(self.busy)

   def finished(self, x):
      return x in self.things.keys()

   def __repr__(self):
      return "Available %s Waiting %s" % (self.available(), self.waiting())

class Worker(object):
     def __init__(self, puzzle):
         self.task = None
         self.duration = 0
         self.puzzle = puzzle

     def work(self, t):
         self.task = t
         self.duration = 60 + (ord(t) - ord('A')) + 1

     def dowork(self):
         if self.duration:
             self.duration -= 1
             if not self.duration:
                self.puzzle.complete(self.task)
                self.task = None

     def __repr__(self):
         return self.task if self.task else '.'


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
        workcount = int(sys.argv[2])
        answer=[]
        workers = [ Worker(puzzle) for x in xrange(workcount) ]
        time=0
        print puzzle.steps
        while sum(w.duration for w in workers) or len(puzzle.steps):
            # pprint.pprint(puzzle.steps)
            # pprint.pprint(puzzle.things)
            if puzzle.available():
                print puzzle
            for w in workers:
                if not w.task:
                   x = puzzle.next()
                   if x:
                      puzzle.setbusy(x)
                      w.work(x)
            time += 1
            print "%2d: %s" % (time, workers)
            for w in workers:
                x = w.task
                w.dowork()
                if x and not w.duration:
                   answer.append(x)

        print time
        print ''.join(answer)
       
      
