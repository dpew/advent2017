#!/usr/bin/env python

import sys
import re
from Queue import Queue
from collections import defaultdict

watch = set(['b', 'c', 'h'])


class Cpu(object):
    def __init__(self, name, cpu=None):
        self.name = name
        self.registers={}
        self.sndcount = 0
        self.sndcpu = cpu
        self.queue = Queue()
        self.mulcnt = 0
        self.seen = defaultdict(lambda: False)

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
        

    def snd(self, val):
        self.queue.put(val)
  

    def oper(self, oper, val1, val2, line=None):
        v = self.getreg(val2)
        v1 = self.getreg(val1)
#        print "%s: %s[%7s], %s[%7s]" %( oper, val1, v1, val2, v)
#        print oper, v1, v

        if oper == 'sub':
           self.registers[val1] -= v
           if val1 in watch:
              print "SUB  %s[%3s]: %s[%7s], %2s[%7s] %s" %( oper, line, val1, v1, val2, v, self.registers)
           return 1
        if oper == 'mul':
           self.mulcnt += 1
           self.registers[val1] *= v
           if val1 in watch:
              print "MUL  %s[%3s]: %s[%7s], %2s[%7s] %s" %( oper, line, val1, v1, val2, v, self.registers)
           return 1
        if oper == 'snd':
           self.sndcpu.snd(self.getreg(val1))
           self.sndcount += 1
           return 1
        if oper == 'set':
           self.registers[val1] = v
#           print "SET  %s[%3s]: %s[%7s], %2s[%7s] %s" %( oper, line, val1, v1, val2, v, self.registers)
           return 1
        if oper == 'mod':
           self.registers[val1] = self.registers[val1] % v
           return 1
        if oper == 'rcv':
           if self.queue.empty():
               return 0
           self.registers[val1] = self.queue.get()
           return 1
        if oper == 'jgz':
           if self.getreg(val1) > 0:
               return v
           return 1
        if oper == 'jnz':
           #if self.getreg(val1) == -8:
           #    print "OPTIMIZE1 %s: %s[%7s], %s[%7s] %s" %( oper, val1, v1, val2, v, self.registers)
           #    self.getreg('d')
               #self.registers['d'] += 1
           #    print "OPTIMIZE2 %s: %s[%7s], %2s[%7s] %s" %( oper, val1, v1, val2, v, self.registers)
           #    return 1
           if self.getreg(val1) != 0:
               if not self.seen[line]:
#                   print "FAIL %s[%3s]: %s[%7s], %2s[%7s] %s" %( oper, line, val1, v1, val2, v, self.registers)
                   self.seen[line] = True
               return v
           self.seen[line] = False
#           print "GOOD %s[%3s]: %s[%7s], %2s[%7s] %s" %( oper, line, val1, v1, val2, v, self.registers)
           return 1
         
        raise ValueError("Bad oper %s" % (oper,))

        
    def __repr__(self):
        return "%s: %s %s" % (self.name, self.sndcount, self.registers)


maxval=0
with open(sys.argv[1]) as f:
   lines = [ l.strip().split() for l in f.readlines() ]

found=False
idx0 = 0
c0 = Cpu("0")
c0.oper('set', 'a', '1')

def getl(line, idx):
    try:
        return line[idx]
    except IndexError:
        return None
    
while idx0 < len(lines):
    nxt0 = c0.oper(lines[idx0][0], lines[idx0][1], getl(lines[idx0], 2), idx0)
#    nxt1 = c1.oper(lines[idx1][0], lines[idx1][1], getl(lines[idx1], 2))
#    if nxt0 == 0 and nxt1 == 0:
#        break
    # print c0, c1
#    print 'h', c0.getreg('h')
    idx0 += nxt0
#    idx1 += nxt1

print c0.registers, "MULCNT", c0.mulcnt
#print "C0", c0.sndcount, "C1", c1.sndcount
