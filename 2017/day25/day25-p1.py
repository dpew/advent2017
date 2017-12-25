#!/usr/bin/env python

import sys
import itertools
from collections import defaultdict


class Tape(object):
    def __init__(self):
        self.tape = defaultdict(lambda: 0)
        self.pos = 0
        self.minpos = 0
        self.maxpos = 0

    def getval(self):
        return self.tape[self.pos]

    def setval(self, newval):
        self.tape[self.pos] = newval

    def setpos(self, direction):
        self.pos += direction
        self.minpos = min(self.pos, self.minpos)
        self.maxpos = max(self.pos, self.maxpos)

    def chksum(self):
        return sum(self.tape[x] for x in xrange(self.minpos, self.maxpos + 1))

    def __repr__(self):
        return str([ self.tape[x] for x in xrange(self.minpos, self.maxpos + 1) ])
            

class State(object):

    def __init__(self, name):
        self.name = name
        self.next = [None] * 2

    def add(self, val, write, move, newstate):
        self.next[val] = (newstate, write, move)

    def execute(self, val):
        return self.next[val]

    def __repr__(self):
        return "State(%s)" % (self.name,)

def p(x):
    print "P", x
    return x

def getlast(strval):
    return strval.split()[-1][:-1]

def readfile(path):
    with open(path, 'r') as f:
        curstate=None
        curval=None
        write=None
        move=None
        cont=None
        for l in f.readlines(): 
            l = l.strip()
            if l.find("In state") >= 0:
                curstate=getlast(l)
            elif l.find("current value") >= 0:
                curval=int(p(getlast(l)))
            elif l.find("Write") >= 0:
                write=int(p(getlast(l)))
            elif l.find("Move") >= 0:
                move=1 if "right" == getlast(l) else -1
            elif l.find("Continue") >= 0:
                cont=getlast(l)
                yield curstate, curval, write, move, cont

turing={}
for vals in readfile(sys.argv[1]):
   try:
       state = turing[vals[0]]
   except KeyError:
       state = State(vals[0])
       turing[state.name] = state
   #print "Adding", state
   #print vals
   state.add(vals[1], vals[2], vals[3], vals[4])

print turing

tape = Tape()
statename='A' if len(sys.argv) <= 2 else sys.argv[2]
count=6 if len(sys.argv) <= 3 else int(sys.argv[3])

for x in xrange(count):
    statename, newval, move = turing[statename].execute(tape.getval())
    tape.setval(newval)
    tape.setpos(move)
    #print tape

print tape.chksum()
