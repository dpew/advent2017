#!/usr/bin/env python
import sys

class CircBuf(object):

    def __init__(self, spin):
        self.buffer = [ 0 ]
        self.spin = spin
        self.pos = 0

    def add(self, num):
        self.pos = (self.pos + self.spin) % len(self.buffer)
        self.buffer.insert(self.pos+1, num)
        self.pos += 1

    def get(self, pos):
        return self.buffer[pos % len(self.buffer)]

    def __repr__(self):
        return "{%s}" % (','.join(str(c) for c in self.buffer),)


c = CircBuf(377)
for x in xrange(1, int(5e5)+1):
    c.add(x)

idx = c.buffer.index(0)
print c.get(idx), c.get(idx + 1)
