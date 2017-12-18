#!/usr/bin/env python

import sys
import re


class Cpu(object):
    def __init__(self, name):
        self.name = name
        self.rcv = None
        self.registers={}

    def getreg(self, name):
        if name is None:
            return None

        try:
            return int(name)
        except:
            pass
          
        try:
            return self.registers[name]
        except KeyError:
            self.registers[name] = 0
            return 0
        

    def oper(self, oper, val1, val2):
        v = self.getreg(val2)
        self.getreg(val1)

        if oper == 'add':
           self.registers[val1] += v
           return 1
        if oper == 'mul':
           self.registers[val1] *= v
           return 1
        if oper == 'snd':
           self.rcv = self.registers[val1]
           return 1
        if oper == 'set':
           self.registers[val1] = v
           return 1
        if oper == 'mod':
           self.registers[val1] = self.registers[val1] % v
           return 1
        if oper == 'rcv':
           if self.registers[val1] != 0:
               return None
           return 1
        if oper == 'jgz':
           if self.registers[val1] > 0:
               return v
           return 1
         
        raise ValueError("Bad oper %s" % (oper,))
        
    def __repr__(self):
        return "%s: %s %s" % (self.name, self.rcv, self.registers)


maxval=0
with open(sys.argv[1]) as f:
   lines = [ l.strip().split() for l in f.readlines() ]

found=False
idx = 0
c1 = Cpu("1")
while not found:
    print lines[idx]
    try:
        val = lines[idx][2]
    except IndexError:
        val = None
    nxt = c1.oper(lines[idx][0], lines[idx][1], val)
    print c1
    if nxt is None:
        found = True
    else:
        idx += nxt

print c1.rcv
