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
        self.groups.append(unit)

    def choose_targets(self, army):
        targets = list(army.groups) 
        chosen = []
        for g in sorted(self.groups, key=lambda s: s.effective_power, reverse=True):
            if targets:
                target = g.choose_attack(targets)
                chosen.append((g, target))
                targets.remove(target)
        return chosen

    def size(self):
         return sum(1 if g.alive else 0 for g in self.groups)

    def __repr__(self):
        r = ""
        r = []
        return '\n'.join("Group %d: %d units %d damage, %d effective_power" % (e, g.effective_units, g.damage, g.effective_power)
                         for e, g in enumerate(self.groups))

class Group(object):

    def __init__(self, unit, count):
        self.name = "Group"
        self.unit = unit
        self.count = int(count)
        self.damage = 0
        self.alive = True

    @property
    def effective_power(self):
        return self.unit.attackdamage * self.effective_units

    @property
    def effective_units(self):
        return max(0, self.count - self.damage/self.unit.hitpoints)

    def choose_attack(self, groups):
        if groups:
            return max(groups, key=lambda g: self.vulnerable_key(g))
        raise ValueError("No groups")

    def vulnerable_key(self, group):
        return (group.effectiveness(self.unit.attacktype, self.unit.attackdamage), group.effective_power, group.unit.initiative)

    def effectiveness(self, attacktype, points): 
        '''
            Returns the amount of damage done to this group for the given attack type and points
        '''
        vi = 1
        if attacktype in self.unit.weakness:
           vi = 2
        elif self.unit.attacktype in self.unit.immunities:
           vi = 0
        return points * vi

    def attack(self, damage):
        self.damage += damage
        self.alive = self.damage < (self.unit.hitpoints * self.count)

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
       elif line.strip():
          curarmy.add(parseline(line))

for e, g in enumerate(immune.groups):
   g.name = "Immune group %d" %(e+1,)
for e, g in enumerate(infection.groups):
   g.name = "Infect group %d" %(e+1,)

   
while immune.size() > 0 and infection.size() > 0:
    print immune.size(), infection.size()
    chosen = immune.choose_targets(infection)
    chosen.extend(infection.choose_targets(immune))
   
    for attacker, defender in sorted(chosen, key=lambda g: g[0].unit.initiative, reverse=True):
        units = defender.effective_units
        defender.attack(defender.effectiveness(attacker.unit.attacktype, attacker.effective_power))
        units = units - defender.effective_units 
        print "%s attacks %s killing %d units" % (attacker.name, defender.name, units)

print "Immune\n", immune
print "Infection\n", infection
