#!/usr/bin/env python

import sys
import re

registers={}

sound=None

class Register(object):
    def __init__(self, name):
        self.name = name
        self.val = 0
        self.rcv = None

    def oper(self, oper, val):
        global sound
        if val is not None:
            try:
                v = registers[val].val
            except KeyError:
                v = int(val)
        else:
           v = None

        if oper == 'add':
           self.val += int(v)
           return 1
        if oper == 'mul':
           self.val = self.val * v
           return 1
        if oper == 'snd':
           self.rcv = self.val
           sound = self.val
           return 1
        if oper == 'set':
           self.val = v
           return 1
        if oper == 'mod':
           self.val = self.val % v
           return 1
        if oper == 'rcv':
           if self.val != 0:
               return None
           return 1
        if oper == 'jgz':
           if self.val > 0:
               return v
           return 1
         
        raise ValueError("Bad oper %s" % (oper,))
        
    def __repr__(self):
        return "%s: %d %s" % (self.name, self.val, self.rcv)


def getreg(name):
    try:
        return registers[name]
    except KeyError:
        pass
    reg = Register(name)
    registers[name] = reg
    return reg
    
maxval=0
with open(sys.argv[1]) as f:
   lines = [ l.strip().split() for l in f.readlines() ]

found=False
idx = 0
while not found:
    print lines[idx]
    try:
        val = lines[idx][2]
    except IndexError:
        val = None
    r = getreg(lines[idx][1])
    nxt = r.oper(lines[idx][0], val)
    print r
    if nxt is None:
        found = True
    else:
        idx += nxt

print r.rcv, sound
