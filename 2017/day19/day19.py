#!/usr/bin/env python
import sys
import pprint

DIRECTIONS=[(0,1),(1,0),(-1,0),(0,-1)]
ALPHA="ABCDEFGHIJKLMNOPQRSTUVWxYZ"

letters=[]

class Tron(object):

    def __init__(self, x, y, grid, width, height):
        self.pos = [x, y]
        self.direction = (0, 1)
        self.grid = grid
        self.width = width
        self.height = height
        self.seen = set()
        self.steps = 0

    def getgrid(self, pos):
        try: 
            return self.grid[pos[1]][pos[0]]
        except IndexError:
            return ' '

    def addpos(self, direction):
        return (self.pos[0] + direction[0], self.pos[1] + direction[1])

    def next(self):
        self.steps += 1
        self.pos = self.addpos(self.direction)
        if (self.pos[0] > self.width or self.pos[0] < 0):
            return False
        if (self.pos[1] > self.height or self.pos[1] < 0):
            return False
        c = self.getgrid(self.pos)
        print c, self.pos, self.steps
        if c == '+':
            if self.pos in self.seen:
                raise ValueError("Seen %s %s" % (self.pos,self.direction))
            self.seen.add(self.pos)
            self.direction = self.newdirection(self.direction)
        elif c in ALPHA: 
            print 'GOT', c
        elif c == ' ':
            return False
        return True
         
    def newdirection(self, curdirection):
        if curdirection[0] == 0:
            if self.getgrid(self.addpos((-1,0))) != ' ':
                return (-1, 0)
            elif self.getgrid(self.addpos((1,0))) != ' ':
                return (1, 0)
            else:
                raise ValueError("No direction %s" % (self.pos,))
        else:
            if self.getgrid(self.addpos((0,-1))) != ' ':
                return (0, -1)
            elif self.getgrid(self.addpos((0,1))) != ' ':
                return (0, 1)
            else:
                raise ValueError("No direction %s" % (self.pos,))

    def get(self, pos):
        return self.buffer[pos % len(self.buffer)]

    def __repr__(self):
        return "{%s}" % (','.join(str(c) for c in self.buffer),)


grid=[]
width=0
with open(sys.argv[1]) as f:
    for l in f.readlines():
        grid.append(l) #.rstrip())
        width = max(width, len(l))

start=grid[0].index('|')
print grid[0]
print grid[0][start]
t = Tron(start, 0, grid, width, len(grid))
while t.next():
    pass
