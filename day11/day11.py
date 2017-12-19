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


def distance(moves):
    '''
        >>> distance('ne,ne,ne')
        3
        >>> distance('ne,ne,sw,sw')
        0
        >>> distance('ne,ne,s,s')
        2
        >>> distance('sw,sw,se,sw,sw')
        3
        >>> distance('sw,nw,sw,nw,sw')
        5
    '''
    pos = [0, 0]
    for cmd in moves.split(','):
        pos[0], pos[1] = pos[0] + MAPVAL[cmd][0], pos[1] + MAPVAL[cmd][1]

    print pos
    return int(floor(sqrt((pos[0]**2) + (pos[1]**2)))) 


if __name__ == '__main__':
    if len(sys.argv) == 1:
        import doctest
        doctest.testmod()
    else:
        with open(sys.argv[1]) as f:
            print distance(f.readline().strip())
