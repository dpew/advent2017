#!/usr/bin/env python
import sys

class Node:
  def __init__(self, cargo=None, next=None): 
    self.cargo = cargo 
    self.next = next    

  def __str__(self): 
    return str(self.cargo)

class CircBuf(object):

    def __init__(self, spin):
        self.spin = spin
        self.nodes = Node(0)
        self.nodes.next = self.nodes
        self.pos = self.nodes
        self.size = 1

    def add(self, num):
        jump = self.spin % self.size
        p = self.pos
        for x in xrange(jump):
            p = p.next
        node = Node(num, p.next)
        p.next = node
        self.pos = node 
        self.size += 1

    def get(self, pos):
        p = self.nodes
        for x in xrange(pos): 
            p = p.next
        return p

    def find(self, val):
        p = self.nodes
        while p.cargo != val:
            p = p.next
        return p

    def __repr__(self):
        return "{%s}" % (','.join(str(c) for c in iter(self)),)

    def __iter__(self):
        p = self.nodes
        for x in xrange(self.size):
            yield p.cargo
            p = p.next


c = CircBuf(377)
for x in xrange(1, 50000001):
    c.add(x)

p = c.find(0)
print p, p.next
