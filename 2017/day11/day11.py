#!/usr/bin/env python
import sys
from math import radians, cos, sin, sqrt, ceil, floor

C = cos(radians(30))

MAPVAL = {
    'ne': ( C,  .5),
    'n':  ( 0,   1),
    'nw': (-C,  .5),
    'se': ( C, -.5),
    's':  ( 0,  -1),
    'sw': (-C, -.5)
}


class GridPos(object):
    def __init__(self, x=0, y=0):
        self.pos = [x, y]

    def move(self, cmd):
        return GridPos(self.pos[0] + MAPVAL[cmd][0],  self.pos[1] + MAPVAL[cmd][1])

    def distance(self, pos):
       return sqrt(((pos[0]-self.pos[0])**2) + ((pos[1]-self.pos[1])**2)) 

    def __getitem__(self, idx):
        return self.pos[idx]

    def __repr__(self):
        return repr(self.pos)

def distance(moves):
    '''
        >>> distance('ne,ne,ne')
        (3, 3)
        >>> distance('ne,ne,sw,sw')
        (0, 2)
        >>> distance('ne,ne,s,s')
        (2, 2)
        >>> distance('se,sw,se,sw,sw')
        (3, 3)
        >>> distance('sw,sw,se,sw,sw')
        (4, 4)
        >>> distance('sw,nw,sw,nw,sw')
        (5, 5)
    '''
    start = pos = GridPos()
    maxdist = 0
    for cmd in moves.split(','):
        pos = pos.move(cmd)
        maxdist = max(maxdist, move_distance(pos, start))

    return move_distance(pos, start), maxdist


def move_distance(pos, start):
    '''
        Returns the number of moves it takes to return to start
    '''
    # now use greedy algorith to get back
    count = 0
    while pos.distance(start) > .01:
        moves = [(x[0], pos.move(x[0]).distance(start)) for x in  MAPVAL.items()]
        cmd = min(moves, key=lambda x: x[1])

        pos = pos.move(cmd[0])
        count += 1

    return count

if __name__ == '__main__':
    if len(sys.argv) == 1:
        import doctest
        doctest.testmod()
    else:
        with open(sys.argv[1]) as f:
            print distance(f.readline().strip())
