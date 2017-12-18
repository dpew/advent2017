#!/usr/bin/env python

import sys
import re
import functools

class Node(object):
    def __init__(self, name):
        self.name = name
        self.children = []

    def setval(self, val):
        self.val = int(val)
        return self

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return "%s(%d)" % (self.name, self.val)

    def __eq__(self, other):
        return self.name == self.name

    def depth(self):
        if self.children:
            return 1 + max(n.depth() for n in self.children)
        else:
            return 1

    def add(self, node):
        self.children.append(node)

nodes={}

def getnode(name):
    try:
        return nodes[name]
    except KeyError:
        pass
    node = Node(name)
    nodes[name] = node
    return node
    
with open(sys.argv[1]) as f:
   for line in (re.split('[,() ]+', l.strip()) for l in f.readlines()):
      print line
      node = getnode(line[0]).setval(line[1])
      for child in line[3:]:
          node.add(getnode(child))

mapped = map(lambda x: (x.depth(), x), nodes.values())
m = max(x[0] for x in mapped)
max_node = filter(lambda x: x[0] == m, mapped)
print max_node
