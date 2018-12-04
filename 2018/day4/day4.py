#!/usr/bin/python

import sys
import math
import pprint
import re
import doctest
from collections import defaultdict

class Guard(object):
  def __init__(self):
      self.days={}

  def day(self, d):
      try:
          minutes = self.days[d]
      except KeyError:
          minutes = [0] * 60
          self.days[d] = minutes
      return minutes

  def doasleep(self, d, start, end):
      print d, start, end
      minutes = self.day(d)
      for x in xrange(start, end):
          minutes[x] = 1

  def maxsleep(self):
      sleep=0
      for d in self.days.keys():
         sleep += sum(self.day(d))
      return sleep
          
  def maxhour(self):
      count=[0] * 60
      for d in self.days.keys():
         minutes = self.day(d)
         for m in xrange(0, 60):
            count[m] += minutes[m]
      return count.index(max(count))

  def maxhour2(self):
      count=[0] * 60
      for d in self.days.keys():
         minutes = self.day(d)
         for m in xrange(0, 60):
            count[m] += minutes[m]
      m = max(count)
      return m, count.index(m)

  def __repr__(self):
      data=""
      for d in self.days.keys():
          minutes = self.day(d)
          data += d + ''.join(['#' if x else '.' for x in minutes]) 
          data += '\n'
      return data

guards=defaultdict(lambda: Guard())

count=0
with open(sys.argv[1]) as f:
   guard=-1
   awake=0
   asleep=60
   for line in (re.split(':| \#|\] | ',x) for x in f.readlines()):
      #print line
      time=int(line[2])
      day=line[0]
      if line[3] == 'Guard':
          if guard > -1 and asleep > -1:
              guards[guard].doasleep(day, asleep, 60)
          guard=int(line[4])
          awake=0
          asleep=-1
      elif line[3] == 'falls':
          asleep=time
      elif line[3] == 'wakes':
          awake=time
          #print guard, day, asleep, awake
          guards[guard].doasleep(day, asleep, awake)
          asleep=-1

pprint.pprint(guards)
gmax=0
gnum=-1
gguard=None
for g, gu in guards.items():
    s = gu.maxsleep()
    if s > gmax:
        gmax = s
        gnum = g
        gguard = gu

print gguard.maxhour()
print gnum
print "Answer", gnum * gguard.maxhour()

sleepmax=0
gnum=-1
ghour=-1
for g, gu in guards.items():
    s, h = gu.maxhour2()
    if s > sleepmax:
        sleepmax = s
        ghour = h
        gnum = g

print gnum
print ghour
print "Answer", gnum * ghour

