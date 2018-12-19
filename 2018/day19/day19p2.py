#!/usr/bin/env python

import sys
import math
import pprint
import re
import doctest
from collections import defaultdict


class Computer(object):

    def __init__(self):
        self.ip = 0
        self.ipref = 0
        self.registers = [0] * 6
        self.OPS = {
           "addr": lambda a, b: self.reg(a) + self.reg(b),
           "addi": lambda a, b: self.reg(a) + b,
           "mulr": lambda a, b: self.reg(a) * self.reg(b),
           "muli": lambda a, b: self.reg(a) * b,
           "banr": lambda a, b: self.reg(a) & self.reg(b),
           "bani": lambda a, b: self.reg(a) & b,
           "borr": lambda a, b: self.reg(a) | self.reg(b),
           "bori": lambda a, b: self.reg(a) | b,
           "setr": lambda a, b: self.reg(a),
           "seti": lambda a, b: a,
           "gtir": lambda a, b: 1 if a > self.reg(b) else 0,
           "gtri": lambda a, b: 1 if self.reg(a) > b else 0,
           "gtrr": lambda a, b: 1 if self.reg(a) > self.reg(b) else 0,
           "eqir": lambda a, b: 1 if a == self.reg(b) else 0,
           "eqri": lambda a, b: 1 if self.reg(a) == b else 0,
           "eqrr": lambda a, b: 1 if self.reg(a) == self.reg(b) else 0
        }

    def reg(self, g): 
        #print "register ", g, registers[g]
        return self.registers[g]

    def execute(self, memory):
        instr = memory[self.ip]
        self.registers[self.ipref] = self.ip
        self.setreg(instr[3], self.OPS[instr[0]](instr[1], instr[2]))    
        self.ip = self.registers[self.ipref]
        self.ip += 1
    

    def setreg(self, c, v):
        self.registers[c] = v

    def __repr__(self):
        return str(self.registers)


def parseline(line):
  '''
      >>> parseline('addi 1 16 1')
      ('addi', 1, 16, 1)
      >>> parseline('addi 1 16 1  # ignore')
      ('addi', 1, 16, 1)
      >>> parseline('#ip 1')
      ('#ip', 1, 0, 0)
  '''
  if line.startswith('#'):
      return ('#ip', int(line.split()[1]), 0, 0)
  else:
      comment = line.find("#")
      if comment > 0:
          line = line[:comment]
      return tuple(i if e == 0 else int(i) for e, i in enumerate(line.split()))

def printmem(memory, ip):
   try:
       return ' '.join(str(x) for x in memory[ip])
   except IndexError:
       return "X X X X"

count=0

if __name__ == '__main__':
  if len(sys.argv) == 1:
      import doctest
      doctest.testmod()
      sys.exit(0)


computer = Computer()
with open(sys.argv[1]) as f:
    memory = []
    for l in f.readlines():
        instr = parseline(l)
        if instr[0] == '#ip': 
            computer.ipref = instr[1]
        else:
            memory.append(instr)

computer.setreg(0, 1)
while computer.ip >= 0 and computer.ip < len(memory):
   before = repr(computer)
   ip = computer.ip
   computer.execute(memory)
   print "id=%3d %-33s %-15s %-33s" % (ip, before, printmem(memory, ip), computer)

print "id=%d %s %s %s" % (ip, before, printmem(memory, ip), computer)
