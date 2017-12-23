#!/usr/bin/env python
import sys
import pprint
import re

DIRECTIONS=[(0,1),(1,0),(-1,0),(0,-1)]
ALPHA="ABCDEFGHIJKLMNOPQRSTUVWxYZ"


class Node(object):

    def __init__(self, name, *args):
        self.name = name
        self.vert = set()
        for c in args:
            self.add(c)

    def add(self, node):
        print "Adding %s" % (node,)
        if node not in self.vert:
            self.vert.add(node)
            node.add(self)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name.eq(other.name)

    def __repr__(self):
        return "Node('%s, '%s)" % (self.name, ", ".join(x.name for x in self.vert))

def getnode(name):
    try:
        return nodes[name]
    except KeyError:
        n = Node(name)
        nodes[name] = n
        return n


def ingroup(node, visited):
    if node in visited:
        return visited
    print "visiting %s" % (node,)
    visited.add(node)
    for c in node.vert:
        ingroup(c, visited)
    return visited

nodes={} #/name: Node

with open(sys.argv[1]) as f:
    for l in f.readlines():
        x = re.split("[ ,]*", l.strip())
        print x
        parent = getnode(x[0])
        for c in x[2:]:
            parent.add(getnode(c))


pprint.pprint(nodes)
matching = ingroup(getnode('0'), set())
print [c.name for c in matching]
print len(matching)
