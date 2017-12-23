#!/usr/bin/env python

import sys
import pprint
import re


class Axis(object):

    def __init__(self, pos, vel, acc):
        self.pos = pos
        self.vel = vel
        self.acc = acc

    def tick(self):
        self.vel += self.acc
        self.pos += self.vel
       
    def __repr__(self):
        return "<%d,%d,%d>" % (self.pos, self.vel, self.acc)

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other):
        return self.pos == other.pos

class Particle(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.cum_dist = 0
        self.mindist = self.distance()

    def tick(self):
        self.x.tick()
        self.y.tick()
        self.z.tick()
        self.mindist = min(self.mindist, self.distance) 
        self.cum_dist += self.distance()

    def distance(self):
        return abs(self.x.pos) + abs(self.y.pos) + abs(self.z.pos)

    def cum_distance(self):
        return self.cum_dist

    def __repr__(self):
        return "%s %s %s" % (self.x, self.y, self.z)

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other):
        return self.pos == other.pos


def parse_line(line):
    x=re.split("[^-0-9]*", line.strip())
    y=[int(i) for i in filter(lambda s: s, x)]
    return Particle(Axis(y[0],y[3],y[6]),
                    Axis(y[1],y[4],y[7]),
                    Axis(y[2],y[5],y[8]))


class Cloud(object):

    def __init__(self):
        self.particles = []

    def add(self, particle):
        self.particles.append(particle)

    def tick(self):
        for p in self.particles:
            p.tick()

import doctest
doctest.testmod()


cloud = Cloud()
with open(sys.argv[1]) as f:
    for l in f.readlines():
        cloud.add(parse_line(l))

print cloud.particles[0]
print cloud.particles[1]


for x in xrange(int(sys.argv[2]) if len(sys.argv) > 2 else 10):
    cloud.tick()


dist = [ (c[0], c[1].cum_distance()) for c in enumerate(cloud.particles) ]
mindist = [ (c[0], c[1].mindist) for c in enumerate(cloud.particles) ]

winner= min(dist, key=lambda x: abs(x[1]))
print winner, cloud.particles[winner[0]]
minwinner= min(mindist, key=lambda x: abs(x[1]))
print minwinner, cloud.particles[minwinner[0]]
