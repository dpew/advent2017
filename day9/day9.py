#!/usr/bin/env python
import sys

class Group(object):

    def __init__(self, *args):
        self.children = []
        self.parent = None
        for c in args:
            self.add(c)

    def set_parent(self, parent):
        self.parent = parent
        if self not in parent.children:
            parent.children.append(self)
        return self

    def add(self, child):
        child.set_parent(self)

    def score(self):
        return self.parent and self.parent.score() + 1 or 1

    def total(self):
        return self.score() + sum(c.total() for c in self.children)

    def __repr__(self):
        return "{%s}" % (','.join(repr(c) for c in self.children),)


def parse(iterable):
    is_garbage = False
    is_bang = False
    for c in iterable:
        if is_bang:
            is_bang = False
            continue
        if c == '!':
           is_bang = True
           continue
        if is_garbage:
            if c == '>':
                is_garbage = False
            continue
        if c == '<':
           is_garbage = True
           continue
        yield c

def process(line):
    line = line.strip()
    top = g = None
    print 'LINE', ''.join(parse(line))
    for c in parse(line):
        if c == '{':
            if not top:
                top = g = Group()
            else:
                child = Group()
                g.add(child)
                g = child
        elif c == '}':
            g = g.parent
    print line, top, top.total()

with open(sys.argv[1]) as f:
    for line in f.readlines():
        process(line)
