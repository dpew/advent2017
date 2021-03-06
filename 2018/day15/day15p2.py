#!/usr/bin/env python

import sys
import math
import pprint
import re
import doctest
from collections import defaultdict

#DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))
DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))
MAXDIST=100000
DEBUG=0

def shortest(nodes):
    if not nodes:
       return None
    #return sorted(nodes, key=lambda n: (n.dist, n.pos, invertpath(n.path)))[0]
    return sorted(nodes, key=lambda n: (n.dist, invertpath(n.path)))[0]

def left(pos):
    '''
       >>> left((0, 1))
       (1, 0)
       >>> left((0, -1))
       (-1, 0)
       >>> left((1, 0))
       (0, -1)
       >>> left((-1, 0))
       (0, 1)
    '''
    return (pos[1], -pos[0])

def right(pos):
    '''
       >>> right((0, 1))
       (-1, 0)
       >>> right((0, -1))
       (1, 0)
       >>> right((1, 0))
       (0, 1)
       >>> right((-1, 0))
       (0, -1)
    '''
    return (-pos[1], pos[0])

def addpos(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def invertpath(path):
    '''
        >>> invertpath(((4, 2), (3, 2), (2, 2)))
        ((2, 4), (2, 3), (2, 2))
    '''
    return tuple(tuple((t[::-1])) for t in path)

def readingorder(p1, width=1000):
    '''
        >>> readingorder((3, 2))
        2003
        >>> readingorder((5, 10))
        10005
        >>> p1 = (100, 100)
        >>> sorted((addpos(p1, d) for d in DIRECTIONS), key=lambda k: (readingorder(k) - readingorder(p1)) % (MAXDIST * MAXDIST))
        [(101, 100), (100, 101), (100, 99), (99, 100)]
    '''
    return p1[1] * width + p1[0]


def comppos(p1, p2):
    '''
        >>> p = (100, 100)
        >>> sorted((addpos(p, d) for d in DIRECTIONS), key=lambda k: comppos(p, k))
        [(101, 100), (100, 101), (100, 99), (99, 100)]
    '''
    return (readingorder(p2) - readingorder(p1)) % (MAXDIST * MAXDIST)

def sortpaths(*paths):
    '''
        >>> p1=((2,1),(2,2),(1,2),(1,3))
        >>> p2=((2,1),(1,1),(1,2),(1,3))
        >>> sortpaths(p1, p2)
        [((2, 1), (1, 1), (1, 2), (1, 3)), ((2, 1), (2, 2), (1, 2), (1, 3))]
        >>> sortpaths(p2, p1)
        [((2, 1), (1, 1), (1, 2), (1, 3)), ((2, 1), (2, 2), (1, 2), (1, 3))]
        >>> p1=((4, 2), (3, 2), (2, 2))
        >>> p2=((4, 2), (5, 1), (2, 2))
        >>> sortpaths(p1, p2)
        [((4, 2), (5, 1), (2, 2)), ((4, 2), (3, 2), (2, 2))]
        >>> sortpaths(p2, p1)
        [((4, 2), (5, 1), (2, 2)), ((4, 2), (3, 2), (2, 2))]
        >>> p1=((4, 2), (3, 2), (2, 2))
        >>> p2=((4, 2), (5, 1), (2, 2))
    '''
    return sorted(paths, key=lambda p: invertpath(p))


class Board(object):

    def __init__(self, grid, units):
        self.grid = grid
        self.units = units
        self.height = len(grid)
        self.width = max(len(g) for g in grid)
        self.update()

    def get(self, pos):
        '''
            Returns (E|G|.|#,Unit)
        '''
        try:
            return (self.unitdict[pos].type, self.unitdict[pos])
        except KeyError:
            try:
                return (self.grid[pos[1]][pos[0]], None)
            except IndexError:
                return ( '?', None)

    def update(self):
        self.unitdict = dict((u.pos, u) for u in self.units if u.points > 0)

    def listunits(self):
        '''
            Returns units in read order
        '''
        return sorted(self.unitdict.values(), key=lambda u: readingorder(u.pos))

    def move(self):
        '''
           Moves all units.  Returns number of units moved
        '''
        moves = 0
        for u in self.listunits():
            remain = set(u.type for u in self.unitdict.values())
            if len(remain) < 2:
               return False
            if u.points > 0:
               if DEBUG > 1:
                  print "TURN %s" % (u, )
               moves+=u.move(self)
               self.update()
               u.attack(self)
               self.update()
        return True

    def attack(self):
        return
        attacks = 0
        for u in self.listunits():
            if u.points > 0:
                attacks += u.attack(board)
                self.update()
        return attacks

    def visit2(self, pos, criteria):
        v = Visitors() 
        spanning=[]
        dist = MAXDIST

        at = self.get(pos)
        spanning.append(v.put(pos, 0, at[0], at[1], (pos,)))
        while True:
            n = shortest(spanning)
            if not n:
                return v
            spanning.remove(n)
            
            for d in DIRECTIONS:
               p = addpos(n.pos, d)
               #if not v.get(p):
               at = self.get(p)
                  #print "Found ", at
               if criteria(at):
                   #print "Adding ", p, at
                   s = v.put(p, n.dist + 1, at[0], at[1], n.path + (p,))
                   if s:
                       spanning.append(s)

    def visit(self, visitors, criteria, pos, path=(), direct=None, dist=0, maxdist=200): #MAXDIST):
        
        # print "HERE", pos, dist, direct
        if dist > maxdist or dist > visitors.mindist(pos):
           return
  
        # if dist == 0, ignore the current position
        if dist > 0:
            at = self.get(pos)
            if not criteria(at):
                return visitors

            if visitors.distance(pos) < dist:
               return visitors

            # print "Distance", visitors.distance(pos)
            visitors.put(pos, dist, at[0], at[1], path)

        for d in DIRECTIONS if not direct else (direct, left(direct), right(direct)):
            self.visit(visitors, criteria, addpos(pos, d), path=path + (pos,), direct=d, dist=dist+1, maxdist=maxdist-1)
        return visitors

    def row(self, y):
        return ''.join(self.get((x, y))[0] for x in xrange(self.width)) \
               + ' ' \
               + ','.join(self.get((x, y))[1].prt() for x in xrange(self.width) if self.get((x, y))[1])

    def __repr__(self):
        return '\n'.join(self.row(y) for y in xrange(self.height))

class Unit(object):

    def __init__(self, x, y, t, points=200, apower=3):
        '''
            x, y, type ('E' or 'G'))
        '''
        self.pos = (x, y)
        self.type = t
        self.seek = 'G' if t == 'E' else 'E'
        self.points = points
        self.apower = apower


    def move(self, board):
        '''
            Move the unit in the board.  Returns 0 = no moves, 1 a move possible
        '''
        visitors = board.visit2(self.pos, lambda c: c[0] in ('.', self.seek))
        if DEBUG > 2:
           print "VISITORS", visitors
        nearest = visitors.nearest()
        if DEBUG > 2:
           print "MOVE", self.prt(), self.pos, pprint.pformat(nearest)
        if nearest:
            if nearest[0].dist > 1:
                if DEBUG > 1:
                    print "MOVE %s -> %s", (self, nearest[0].path[1])
                self.pos = nearest[0].path[1]
            return 1
        
        return 0

    def attack(self, board):
        '''
            Attacks adjacent units in board
            Returns 0 = no combatants, 1 a combatant
        '''
        visitors = board.visit2(self.pos, lambda c: c[0] in ('.', self.seek))
        nearest = sorted((n for n in visitors.nearest() if n.dist == 1 and n.unit.points > 0), key=lambda nd: (nd.unit.points, readingorder(nd.pos))) #comppos(self.pos, nd.pos)))
#        nearest = sorted((n for n in visitors.nearest() if n.dist == 1), key=lambda nd: (nd.unit.points, self.pos))
        if DEBUG > 2:
            pprint.pprint(('ATTACK', self, nearest))
        if nearest:
            if DEBUG > 1:
               print "ATTACK %s -> %s" % (self, nearest[0].unit)
            nearest[0].unit.points -= self.apower
            return 1
        #visitors = board.visit(Visitors(), lambda c: c[0] in ('.', self.seek), self.pos, maxdist=1)
        #visitors.nearest()
        return 0

    def prt(self):
        return "%s(%d)" % (self.type, self.points)

    def __repr__(self):
        return "%s(%2d,%2d,pnt=%d,pwr=%d)" % (self.type, self.pos[0], self.pos[1], self.points, self.apower)

class VNode(object):
    def __init__(self, dist, pos, kind, unit, path): 
       self.dist = dist
       self.pos = pos
       self.kind = kind
       self.unit = unit
       self.path = path

    def __repr__(self):
       return "VNode(dist=%d, pos=%s, kind=%s, unit=%s, path=%s)" % (self.dist, self.pos, self.kind, self.unit, self.path)

class Visitors(object):

    def __init__(self):
       self.positions = {}

    def get(self, pos):
       return self.positions.get(pos, None)

    def mindist(self, pos):
       try:
           return self.positions[pos].dist
       except KeyError:
           return MAXDIST

    def put(self, pos, dist, kind, unit, path):
       newnode = VNode(dist, pos, kind, unit, path)
       try:
           node = self.positions[pos]
           node = sorted((node, newnode), key=lambda n: (n.dist, n.pos, invertpath(n.path)))[0]
           self.positions[pos] = node
           return None # newnode
           
       except KeyError:
           self.positions[pos] = newnode
           return newnode

    def distance(self, pos):
       try:
           return self.positions[pos].dist
       except KeyError:
           return MAXDIST

    def nearest(self):
       return sorted((n for n in self.positions.values() if n.kind != '.' and n.dist > 0),
              key=lambda node: (node.dist, invertpath(node.path)))

    def __repr__(self):
       return pprint.pformat(dict((p, v) for p, v in self.positions.items() if v.kind != '.'))
       

if __name__ == '__main__':
    if len(sys.argv) == 1:
      import doctest
      doctest.testmod()
      sys.exit(0)


def rungame(power):
  grid=[]
  units=[]
  width=0
  with open(sys.argv[1]) as f:
      y=0
      for l in f.readlines():
	  for x, c in enumerate(l):
	      if c in ('G', 'E'):
		  units.append(Unit(x, y, c, apower=(power if c=='E' else 3)))
	  nl = l.replace('G', '.')
	  nl = nl.replace('E', '.')
	  grid.append(nl.rstrip())
	  width = max(width, len(l))
	  y+=1
      board = Board(grid, units)
      elfcount=sum(1 for u in units if u.type == 'E')
      del units

      rnd = 0
      while True: 
	  if DEBUG > 0:
	    print "ROUND", rnd
	    print board
	  moves=board.move()
	  if not moves:
	      break
	
	  #atk = board.attack()
	  #if atk:
	  # pprint.pprint(board.units)
	  rnd += 1

      elflive = sum(1 for u in board.listunits() if u.type == 'E')
      points=sum(u.points for u in board.listunits())
      print "ROUND", rnd
      print board
      print power, elflive==elfcount, rnd, points, rnd * points
      return elflive == elfcount, rnd*points

lastScore=None
lastMid=None
l=3
r=35
while r >= l:
    mid = l + (r - l)/2
    s, score = rungame(mid)
    if s:
        lastMid,lastScore=mid, score
        r = mid - 1
    else:
        l = mid + 1

print "Mid=%d, Score=%d"% (lastMid, lastScore)

