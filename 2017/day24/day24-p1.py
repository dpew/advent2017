#!/usr/bin/env python

import sys
import itertools
from collections import defaultdict

def readfile(path):
    with open(path, 'r') as f:
        for l in f.readlines(): 
            yield tuple(int(x) for x in l.strip().split('/'))
   


portmap={}
ports=sorted([p for p in readfile(sys.argv[1])])
for p in ports:
    try:
        portmap[p[0]].append(p)
    except KeyError:
        portmap[p[0]] = [p]

def newset(iterable, v):
   s = set(iterable)
   s.add(v)
   return s

class Component(object):
    def __init__(self, iterable):
        self.links = list(iterable)
        self.weight = sum(map(lambda x: x[0] + x[1], self.links))

    def link(self, component):
        return Component(itertools.chain(self.links, component.links))

    def __contains__(self, element):
        return self.links.contains(element)
    
    def __repr__(self):
        return "--".join(str(x) for x in self.links)

#    @property
#    def weight(self):
#        return sum(map(lambda x: x[0] + x[1], self.links))

#print ports

def assemble(size, seen):
    components = []
    try:
        for p in filter(lambda x: size in x and x not in seen, ports):
            c = Component([p])
            components.append(c)
            otherpin = p[1] if p[0] == size else p[0]
            for a in assemble(otherpin, newset(seen, p)):
                components.append(c.link(a))
    except KeyError:
        pass
    #print "RETURN", components
    return components

chains=assemble(0, set())
#for c in chains:
#    print "%4d: %s" % (c.weight, c)

maxchain=max(chains, key=lambda c: c.weight)
print '---------------'
print "MAX", maxchain.weight, maxchain
