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

class Particle(object):
    def __init__(self, name, x, y, z):
        self.name = name
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
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def identity(self):
        return (self.x.pos, self.y.pos, self.z.pos)

    # def __hash__(self):
    #     return hash(self.x.pos, self.y.pos, self.z.pos)

    # def __eq__(self, other):
    #     return self.x.pos == other.x.pos and self.y.pos == other.y.pos and self.z.pos = other.z.pos


def parse_line(name, line):
    x=re.split("[^-0-9]*", line.strip())
    y=[int(i) for i in filter(lambda s: s, x)]
    return Particle(name, Axis(y[0],y[3],y[6]),
                    Axis(y[1],y[4],y[7]),
                    Axis(y[2],y[5],y[8]))


class Cloud(object):

    def __init__(self):
        self.particles = set()

    def add(self, particle):
        self.particles.add(particle)

    def tick(self):
        for p in self.particles:
            p.tick()
        self.del_collisions()

    def del_collisions(self):
        collisions={}
        bad=set()
        for p in self.particles:
            i = p.identity()
            if i in collisions:
               bad.add(collisions[i])
               bad.add(p)
            else:
               collisions[i] = p
        if bad:
            print "Collisions", bad
            self.particles.difference_update(bad)


import doctest
doctest.testmod()


cloud = Cloud()
with open(sys.argv[1]) as f:
    n=0
    for l in f.readlines():
        cloud.add(parse_line(n, l))
        n += 1

#print cloud.particles[0]
#print cloud.particles[1]


for x in xrange(int(sys.argv[2]) if len(sys.argv) > 2 else 10):
    cloud.tick()


dist = [ (c[0], c[1].cum_distance()) for c in enumerate(cloud.particles) ]
mindist = [ (c[0], c[1].mindist) for c in enumerate(cloud.particles) ]

#winner= min(dist, key=lambda x: abs(x[1]))
#print winner, cloud.particles[winner[0]]
#minwinner= min(mindist, key=lambda x: abs(x[1]))
#print minwinner, cloud.particles[minwinner[0]]
print len(cloud.particles)
