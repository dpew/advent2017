#!/usr/bin/env python

import sys
import os
import math
import pprint
import re
import doctest
import itertools
from collections import defaultdict
from functools import reduce

# create absolute mydir
mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(mydir, '../lib'))

from advent import *


class Army(object):

    def __init__(self):
        self.groups = []

    def add(self, unit):
        self.groups.add(unit)

class Group(object):

    def __init__(self, unit, count):
        self.units = unit
        self.count = count

class Unit(object):

    def __init__(self, hitpoints, attackdamage, attacktype, initiative):
        self.hitpoints = int(hitpoints)
        self.attackdamage = int(attackdamage)
        self.attacktype = attacktype
        self.initiative = int(initiative)
        self.weakness = []
        self.immunities = []

    def add_immunity(self, immunity):
        self.immunities.add(immunity)

    def add_weakness(self, weakness):
        self.weakness.add(weakness)

    def __repr__(self):
        ims = []
        a = ", ".join(self.weakness)
        if a:
            ims.add("weak to " + a)
        a = ", ".join(self.immunities)
        if a:
            ims.add("immune to " + a)
        a = ";".join(ims)
        if a:
           a = "(" + a + ")"
        
        return \
          "$d hit points %s with an attack that does %d %s damage at initiative %d" % \
         (self.hitpoints,
          a,
          self.attackdamage,
          self.self.attacktype,
          self.initiative)

def parseline(line):
    '''
        >>> parseline('1767 units each with 5757 hit points (weak to fire, radiation) with an attack that does 27 radiation damage at initiative 4')
        '1767 units each with 5757 hit points (weak to fire, radiation) with an attack that does 27 radiation damage at initiative 4'
        >>> parseline('442 units each with 1918 hit points with an attack that does 35 fire damage at initiative 8')
        '442 units each with 1918 hit points with an attack that does 35 fire damage at initiative 8'
        >>> parseline('4378 units each with 32200 hit points (weak to cold) with an attack that does 10 bludgeoning damage at initiative 2')
        '4378 units each with 32200 hit points (weak to cold) with an attack that does 10 bludgeoning damage at initiative 2'
    '''
    data = tokeninze(line, "()")
    weak = ""
    if len(data) > 1:
        line = data[0] + data[2]
        weak = data[1]
    data = tokeninze(line, ' ')
    u = Unit(data[4], data[6], data[7], data[11])
    for 
    return line

if len(sys.argv) < 2:
    import doctest
    doctest.testmod()
    sys.exit(3)

immune = Army()
infection = Army()

with open(sys.argv[1]) as f:
    for line in f.readlines():
         
        
            
    
    line = ty
    nanobots = []
    for l in f.readlines():
        nanobots.append(tuple(int(t) for t in tokenize(l, 'pos=<>, r=')))

maxnano = max(nanobots, key=lambda k: k[3])
print sum(1 if mdistance(maxnano[:3], n[:3]) <= maxnano[3] else 0 for n in nanobots)
#pprint.pprint(nanobots)
