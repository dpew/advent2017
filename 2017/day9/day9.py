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


garbage_chars=0
def parse(iterable):
    global garbage_chars
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
            else:
                garbage_chars += 1
            continue
        if c == '<':
           is_garbage = True
           continue
        yield c

def process(line):
    global garbage_chars
    line = line.strip()
    garbage_chars = 0
    top = g = None
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
    print line, top, top.total() if top else None, garbage_chars

with open(sys.argv[1]) as f:
    for line in f.readlines():
        process(line)
