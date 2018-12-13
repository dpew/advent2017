#!/usr/bin/env python
import sys
import pprint
DIRLOOKUP=['>', 'v', '<', '^']
DIRECTIONS=[(1,0),(0,1),(-1,0),(0,-1)]
# turns left, straight, right 
TURNCHAR=('L', 'S', 'R')
TURNS={}
TURNS[('<', '\\')] = '^'
TURNS[('>', '\\')] = 'v'
TURNS[('v', '\\')] = '>'
TURNS[('^', '\\')] = '<'
TURNS[('<', '/')] = 'v'
TURNS[('>', '/')] = '^'
TURNS[('^', '/')] = '>'
TURNS[('v', '/')] = '<'

class Tron(object):

    def __init__(self, grid, width, height):
        self.grid = grid
        self.width = width
        self.height = height

    def get(self, pos):
        return self.grid[pos[1]][pos[0]]

    def __repr__(self):
        return ''.join(self.grid)


def move(pos, d):
    return (pos[0] + d[0], pos[1] + d[1])

def turnjunct(t, d): 
    '''
       >>> turnjunct('L', 0)
       ('S', 3)
       >>> turnjunct('L', 1)
       ('S', 0)
       >>> turnjunct('R', 0)
       ('L', 1)
       >>> turnjunct('R', 3)
       ('L', 0)
       >>> turnjunct('S', 3)
       ('R', 3)
    '''
    if t == 'L':
       return 'S', (d - 1) % len(DIRLOOKUP)
    if t == 'R':
       return 'L', (d + 1) % len(DIRLOOKUP)
    if t == 'S':
       return 'R', d

def turn(edge, d):
    '''
        >>> turn('\\\\', 0)
        1
        >>> turn('\\\\', 2)
        3
        >>> turn('|', 2)
        2
    '''
    nd = TURNS.get((DIRLOOKUP[d], edge), DIRLOOKUP[d])
    return DIRLOOKUP.index(nd)


class Cart(object):

    def __init__(self, x, y, d):
        self.pos = (x, y)
        self.d = d
        self.turn = 'L'

    def move(self, tron):
        self.pos = move(self.pos, DIRECTIONS[self.d])
        c = tron.get(self.pos)
        if c == '+':
            self.turn, self.d = turnjunct(self.turn, self.d)
        else:
            self.d = turn(c, self.d)

    def __repr__(self):
        return "Cart(%d, %d, %s)" % (self.pos[0], self.pos[1], DIRLOOKUP[self.d])


def crash(carts):
    p=set()
    for c in carts:
        if c.pos in p:
            return c.pos
        p.add(c.pos)
    return None

if len(sys.argv) == 1:
   import doctest
   doctest.testmod()
   sys.exit(1)

grid=[]
carts=[]
width=0
with open(sys.argv[1]) as f:
    y=0
    for l in f.readlines():
        for x, c in enumerate(l):
            if c in DIRLOOKUP:
                carts.append(Cart(x, y, DIRLOOKUP.index(c)))
                print carts
        nl = l.replace('>', '-')
        nl = nl.replace('<', '-')
        nl = nl.replace('^', '|')
        nl = nl.replace('v', '|')
        grid.append(nl) #.rstrip())
        width = max(width, len(l))
        y+=1

#start=grid[0].index('|')
t = Tron(grid, width, len(grid))
while not crash(carts):
    for c in carts:
        c.move(t)
    
print crash(carts)
