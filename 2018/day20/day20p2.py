#!/usr/bin/env python

import sys
import math
import pprint
import re
import doctest
import itertools
from collections import defaultdict
from functools import reduce


UP=(0, -1)
DOWN=(0, 1)
LEFT=(-1, 0)
RIGHT=(1, 0)

DIRS={
   'N': UP,
   'S': DOWN,
   'W': LEFT,
   'E': RIGHT
}

class Maze(object):

    def __init__(self, path=[]):
        self.min = (100, 100)
        self.max = (-100, -100)
        self.connections = set()
        self.addpath(path)

    def addpath(self, path):
        pos=(0, 0)
        for p in path:
            newpos = addpos(pos, DIRS[p])
            self.adddoor(pos, newpos)
            pos = newpos

    def adddoor(self, p1, p2):
        self.min = (min(self.min[0], p1[0], p2[0]), min(self.min[1], p1[1], p2[1]))
        self.max = (max(self.max[0], p1[0], p2[0]), max(self.max[1], p1[1], p2[1]))
        self.connections.add(tuple(sorted([p1, p2])))

    def doorat(self, p1, p2):
        c = tuple(sorted([p1, p2]))
        return c in self.connections

    def __repr__(self):
        out = ''
        for y in range(self.min[1], self.max[1] + 1):
            out += '#' + '#'.join('-' if self.doorat((x, y), addpos((x, y), UP)) else '#'
                                  for x in range(self.min[0], self.max[0]+1)) + '#'
            out += '\n'
            row = '.'.join('|' if self.doorat((x, y), addpos((x, y), LEFT)) else '#'
                                    for x in range(self.min[0], self.max[0]+2))
            if y == 0:
                pos = (0 - self.min[0] + 1) * 2
                row = row[:pos-1] + 'X' + row[pos:]
            out += row
            out += '\n'
        y+=1
        out += '#' + '#'.join('-' if self.doorat((x, y), addpos((x, y), UP)) else '#'
                                  for x in range(self.min[0], self.max[0]+1)) + '#'
        out += '\n'
        return out

    def render(self, *paths):
        out = ''
        positions = {}
        for p in paths:
            positions.update(pathToDict(p))
        for y in range(self.min[1], self.max[1] + 1):
            out += '#' + '#'.join('-' if self.doorat((x, y), addpos((x, y), UP)) else '#'
                                  for x in range(self.min[0], self.max[0]+1)) + '#'
            out += '\n'
            row = ''.join('|' if self.doorat((x, y), addpos((x, y), LEFT)) else '#'
                                    for x in range(self.min[0], self.max[0]+2))
            paths = ''.join(positions[(x, y)] if (x, y) in positions else '.'
                                    for x in range(self.min[0], self.max[0]+2)) 
            row = ''.join(itertools.chain(*zip(row, paths)))
            if y == 0:
                pos = (0 - self.min[0] + 1) * 2
                row = row[:pos-1] + 'X' + row[pos:]
            out += row
            out += '\n'
        y+=1
        out += '#' + '#'.join('-' if self.doorat((x, y), addpos((x, y), UP)) else '#'
                                  for x in range(self.min[0], self.max[0]+1)) + '#'
        out += '\n'
        return out

def navigate(path):
   allpaths = []
   paths = [[]]
   i, ln = 0, len(path)
   while i < ln:
       p = path[i]
       # print p, i, paths
       if p in DIRS.keys():
           for mypath in paths:
              mypath.append(p)
           i += 1
       elif p == '(':
           newpaths = []
           children, seen = navigate(path[i+1:])
           # print seen
           i  = i + seen + 1
           mx = max(len(c) for c in children)
           for mypath in paths:
             for c in children:
               if len(c) > 0:
                  newpath = list(mypath)
                  newpath.extend(c)
                  newpaths.append(newpath)
           paths = newpaths
       elif p == '|':
           allpaths.extend(paths)
           paths = [[]]
           i += 1
       elif p == ')':
           break
       else:
           i += 1
   allpaths.extend(paths)
   return allpaths, i+1

def pathToDict(path):
   positions={}
   pos=(0,0)
   positions[pos] = path[0]
   for p in path:
      pos = addpos(pos, DIRS[p])
      positions[pos] = p
      #pos = newpos
   positions[pos] = 'x'
   return positions
   

def addpos(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def measure(path):
    return reduce(addpos, (DIRS[p] for p in path))

def distance(p1, p2):
    '''
        >>> distance((8, 9), (8, 9))
        0
        >>> distance((8, 9), (9, 9))
        1
        >>> distance((8, 9), (9, 10))
        2
        >>> distance((8, 9), (9, 7))
        3
    '''
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    

def shorten(path):
    '''
        >>> shorten('NSEW')
        ''
        >>> shorten('NSEWE')
        'E'
        >>> shorten('NNSEWE')
        'NE'
        >>> shorten('ENNWSWWNEWSSSSEENWNSEEESWENNNN')
        'ENNWSWWSSSEENEENNN'
    '''
    result=[]
    pos = (0, 0)
    seen=[pos]
    for p in path:
       newpos = addpos(pos, DIRS[p])
       #print "BEFORE %s->%s %s %s " % (pos, newpos, ''.join(result) + p, seen)
       try:
          index = seen.index(newpos)
       #   print "MATCH"
          newpos = seen[index]
          result = result[:index] 
          seen = seen[:index+1]
       except ValueError:
          result.append(p)
          seen.append(newpos)
       #print "AFTER  %s->%s %s %s " % (pos, newpos, ''.join(result), seen)
       pos = newpos
    return ''.join(result)
        
def splitpaths(path):
    '''
        >>> list(splitpaths('NSEW'))
        ['N', 'E']
        >>> list(splitpaths('NSEWE'))
        ['N', 'E', 'E']
        >>> list(splitpaths('NNSEWW'))
        ['NN', 'NE', 'NW']
        >>> list(splitpaths('ENNWSWWNEWSSSSEENWNSEEESWENNNN'))
        ['ENNWSWWNE', 'ENNWSWWSSSEENWN', 'ENNWSWWSSSEENEENNN']
    '''
    result=[]
    pos = (0, 0)
    seen=[pos]
    prevseen=set(pos)
    lastpos = pos
    for p in path:
       newpos = addpos(pos, DIRS[p])
       #print "BEFORE %s->%s %s %s " % (pos, newpos, ''.join(result) + p, seen)
       try:
          index = seen.index(newpos)
       #   print "MATCH"
          if pos not in prevseen:
              yield ''.join(result)
          newpos = seen[index]
          result = result[:index] 
          seen = seen[:index+1]
       except ValueError:
          result.append(p)
          seen.append(newpos)
       #print "AFTER  %s->%s %s %s " % (pos, newpos, ''.join(result), seen)
       prevseen.add(lastpos)
       lastpos = pos
       pos = newpos
    if result:
        yield ''.join(result)
        

if len(sys.argv) < 2:
    import doctest
    doctest.testmod()
    sys.exit(3)

with open(sys.argv[1]) as f:
    path = f.readline()

    m = Maze()
    paths, seen = navigate(path)
    for p in paths:
        m.addpath(p)

    shortpaths = list(itertools.chain(*(splitpaths(p) for p in paths)))
    # pprint.pprint(shortpaths)
    maxpath = max(shortpaths, key=len)
    print m
    print m.render(maxpath)
    print m.render(*shortpaths)
    limited = [ s for s in set(shortpaths) if len(s) >= 1000 ]
    print m.render(*limited)
    print 'RESULT', len(maxpath), ''.join(maxpath)
    count = sum(1 if len(x) >= 1000 else 0 for x in shortpaths)
    print "ROOMS above 1000", count, len(limited)
    sys.exit(0)
