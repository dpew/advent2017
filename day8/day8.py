#!/usr/bin/env python

import sys
import re

class Register(object):
    def __init__(self, name):
        self.name = name
        self.val = 0

    def oper(self, oper, val):
        if oper == 'inc':
           self.val += int(val)
           return
        if oper == 'dec':
           self.val -= int(val)
           return
        raise ValueError("Bad oper %s" % (oper,))
        
    def cond(self, cond, val):
        val = int(val)
        if cond == '>':
            return self.val > val
        if cond == '<':
            return self.val < val
        if cond == '>=':
            return self.val >= val
        if cond == '<=':
            return self.val <= val
        if cond == '!=':
            return self.val != val
        if cond == '==':
            return self.val == val

        raise ValueError("Bad cond %s" % (cond,))

    def __repr__(self):
        return "%s: %d" % (self.name, self.val)

registers={}

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
   for line in (l.strip().split() for l in f.readlines()):
      if getreg(line[4]).cond(line[5], line[6]):
          getreg(line[0]).oper(line[1], line[2])
      maxval=max(maxval,max(registers.values(), key=lambda x: x.val).val) 

print "Max register", max(registers.values(), key=lambda x: x.val)
print "max value ever", maxval
