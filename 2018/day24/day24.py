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
        self.unit = unit
        self.count = int(count)

    def __repr__(self):
       return "%d units each with %s" % (self.count, self.unit)

class Unit(object):

    def __init__(self, hitpoints, attackdamage, attacktype, initiative):
        self.hitpoints = int(hitpoints)
        self.attackdamage = int(attackdamage)
        self.attacktype = attacktype
        self.initiative = int(initiative)
        self.weakness = []
        self.immunities = []

    def add_immunity(self, immunity):
        self.immunities.append(immunity)

    def add_weakness(self, weakness):
        self.weakness.append(weakness)

    def __repr__(self):
        ims = []
        a = ", ".join(self.weakness)
        if a:
            ims.append("weak to " + a)
        a = ", ".join(self.immunities)
        if a:
            ims.append("immune to " + a)
        a = "; ".join(ims)
        if a:
           a = "(" + a + ") "
        
        return \
          "%d hit points %swith an attack that does %d %s damage at initiative %d" % \
         (self.hitpoints,
          a,
          self.attackdamage,
          self.attacktype,
          self.initiative)

def parseline(line):
    '''
        >>> parseline('1767 units each with 5757 hit points (weak to fire, radiation) with an attack that does 27 radiation damage at initiative 4')
        1767 units each with 5757 hit points (weak to fire, radiation) with an attack that does 27 radiation damage at initiative 4
        >>> parseline('442 units each with 1918 hit points with an attack that does 35 fire damage at initiative 8')
        442 units each with 1918 hit points with an attack that does 35 fire damage at initiative 8
        >>> parseline('4378 units each with 32200 hit points (weak to cold) with an attack that does 10 bludgeoning damage at initiative 2')
        4378 units each with 32200 hit points (weak to cold) with an attack that does 10 bludgeoning damage at initiative 2
        >>> parseline('4378 units each with 32200 hit points (weak to cold) with an attack that does 10 bludgeoning damage at initiative 2')
        4378 units each with 32200 hit points (weak to cold) with an attack that does 10 bludgeoning damage at initiative 2
        >>> parseline('1380 units each with 20450 hit points (weak to slashing, radiation; immune to bludgeoning, fire) with an attack that does 28 cold damage at initiative 12')
        1380 units each with 20450 hit points (weak to slashing, radiation; immune to bludgeoning, fire) with an attack that does 28 cold damage at initiative 12
    '''
    data = list(tokenize(line, "()"))
    weak = ""
    if len(data) > 1:
        weak = data[1]
        line = data[0] + data[2]
    data = line.split()
    u = Unit(data[4], data[12], data[13], data[17])
    g = Group(u, int(data[0]))

    for w in tokenize(weak, ';'):
        vals = list(tokenize(w, ' ,'))
        addfunc = u.add_immunity if vals[0] == 'immune' else u.add_weakness
        for v in vals[2:]: 
            addfunc(v)
    return g

if len(sys.argv) < 2:
    import doctest
    doctest.testmod()
    sys.exit(3)

immune = Army()
infection = Army()

with open(sys.argv[1]) as f:
    curarmy = immune
    for line in f.readlines():
       if line.startswith("Immune"):
          curarmy = immune
       elif line.startswith("Infection"):
          curarmy = infection
       elif not line.strip():
          curarmy.add(parseline(line))

