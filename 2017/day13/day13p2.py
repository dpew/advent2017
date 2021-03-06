#!/usr/bin/env python

import sys
import pprint
import re


class Layer(object):

    def __init__(self, name, depth):
        self.name = name
        self.depth = int(depth)
        self.position = 0
        self.rawpos = 0

    def iterate(self, by=1):
        '''
           >>> l = Layer(0, 3)
           >>> l.iterate().position
           1
           >>> l.iterate().position
           2
           >>> l.iterate().position
           1
           >>> l.iterate().position
           0
           >>> l.iterate().position
           1
           >>> l.iterate(5).position
           2
        '''
        self.rawpos = (self.rawpos + by) % ((self.depth-1)*2)
        self.position = self.rawpos if self.rawpos < self.depth else self.depth - self.rawpos + 1
        return self

    def hit(self, depth):
        #print self.name, self.position == depth
        return self.position == depth

    def reset(self):
        self.position = 0
        self.rawpos = 0

class EmptyLayer(object):
    def __init__(self, name):
        self.name = name

    def hit(self, depth):
        # print self.name, False
        return False
        
    def iterate(self, by=1):
        pass

    def reset(self):
        pass

class Firewall(object):

    def __init__(self):
        self.layers = []

    def add_layer(self, num, depth):
        l = Layer(num, depth)
        while len(self.layers) <= num:
             self.layers.append(EmptyLayer(len(self.layers)))
        self.layers[num] = l

    def iterate(self, by=1):
        for l in self.layers:
            l.iterate(by=by)

    def reset(self):
        for l in self.layers:
            l.reset()

    def hit(self, layer, depth):
        return self.layers[layer].hit(depth)

    def severity(self, layer, depth):
        return (layer * self.layers[layer].depth) if self.hit(layer, depth) else 0

    def __len__(self):
        return len(self.layers)
    
import doctest
doctest.testmod()

firewall = Firewall()
with open(sys.argv[1]) as f:
    for l in f.readlines():
        x = re.split("[: ]*", l.strip())
        firewall.add_layer(int(x[0]), int(x[1])) 


severity=0
depth=0
delay=0
bad=False
while True:
    firewall.reset()
    if not delay % 1000:
        print "delaying", delay
    firewall.iterate(by=delay)

    for layer in xrange(len(firewall)):
        if firewall.hit(layer, depth):
            bad = True
            break
        firewall.iterate()
    if not bad:
        print "delay", delay
        sys.exit(0)
    bad = False
    delay += 1
