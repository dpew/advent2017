#!/usr/bin/env python

import sys
import pprint
import re
import numpy as np


class Grid(object):

    def __init__(self, gridstr):
      
        #print [list(x) for x in gridstr.split('/')]
        if isinstance(gridstr, basestring):
            self.matrix = np.matrix([list(x) for x in gridstr.split('/')])
        else:
            self.matrix = gridstr
        #self.grid = np.array(list(iterable))
        #print "grid", self.grid
        #print len(self.grid)
        #self.grid = self.grid.reshape(len(self.grid)>>2, len(self.grid)>>2)
        #self.grid = np.matrix(*args)

    def __repr__(self):
        return "Grid(%s)" % (repr(self.matrix),)

    def matches(self, grid):
        '''
            >>> g = Grid('../.#')
            >>> g.matches(Grid('../.#'))
            True
            >>> g.matches(Grid('.#/..'))
            True
            >>> g.matches(Grid('../#.'))
            True
            >>> g.matches(Grid('../.#'))
            True
            >>> g.matches(Grid('../..'))
            False
            >>> Grid(".#./..#/###").matches(Grid(".#./..#/###"))
            True
            >>> Grid(".#./..#/###").matches(Grid(".#./#../###"))
            True
            >>> Grid(".#./..#/###").matches(Grid("#../#.#/##."))
            True
            >>> Grid(".#./..#/###").matches(Grid("###/..#/.#."))
            True
            >>> Grid(".#./..#/###").matches(Grid("#.#/..#/.#."))
            False
            >>> Grid(".#./..#/###").matches(Grid("#./.."))
            False
        '''
        g = grid.matrix
        if len(self.matrix) != len(grid.matrix):
            return False
        for x in xrange(4):
            if (g == self.matrix).all():
                return True
            if (np.flip(g, 0) == self.matrix).all():
                return True
            g = np.rot90(g)
        return False

    def split(self):
        if len(self.matrix) == 3:
            yield Grid(self.matrix)
        else:
            yield Grid(self.matrix[np.ix_(np.arange(0, 2), np.arange(0, 2))])
            yield Grid(self.matrix[np.ix_(np.arange(0, 2), np.arange(2, 4))])
            yield Grid(self.matrix[np.ix_(np.arange(2, 4), np.arange(0, 2))])
            yield Grid(self.matrix[np.ix_(np.arange(2, 4), np.arange(2, 4))])
            
def parse_line(line):
    x=re.split("[ =>]* ", line.strip())
    return Grid(x[0]), [g for g in Grid(x[1]).split()]

def matchgrid(g):
    for lk in lookup:
        if lk[0].matches(g):
            return lk[1]
    raise ValueError("No match for %s" % (g,))

import doctest
doctest.testmod()


lookup=[]
with open(sys.argv[1]) as f:
    for l in f.readlines():
        lookup.append(parse_line(l))

grids = [ Grid(".#./..#/###") ]
for x in xrange(5):
    newgrids=[]
    for g in grids:
        print "G is ", g
        newgrids.extend(matchgrid(g))
    grids = newgrids

print grids
