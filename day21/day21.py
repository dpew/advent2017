#!/usr/bin/env python 
import sys
import pprint
import re
import numpy as np


def addslash(gridstr):
    if len(gridstr) == 4:
       return gridstr[0:2] + '/' + gridstr[2:4]
    elif len(gridstr) == 9:
       return gridstr[0:3] + '/' + gridstr[3:6] + '/' + gridstr[6:9]
    else:
       return gridstr

def spin(gridstr):
    gridstr = gridstr.replace('/', '')
    if len(gridstr) == 9:
        return addslash(''.join(gridstr[x] for x in [2, 5, 8, 1, 4, 7, 0, 3, 6]))
    else:
        return addslash(''.join(gridstr[x] for x in [1, 3, 0, 2]))
        

def flip(gridstr):
    gridstr = gridstr.replace('/', '')
    if len(gridstr) == 9:
        return addslash(''.join(gridstr[x] for x in [2, 1, 0, 5, 4, 3, 8, 7, 6]))
    else:
        return addslash(''.join(gridstr[x] for x in [1, 0, 3, 2]))

def spinflip(gridstr):
    '''
        >>> sorted(spinflip('../.#'))
        ['#./..', '.#/..', '../#.', '../.#']
        >>> sorted(spinflip('.#./..#/###'))
        ['###/#../.#.', '###/..#/.#.', '##./#.#/#..', '#../#.#/##.', '.##/#.#/..#', '.#./#../###', '.#./..#/###', '..#/#.#/.##']
    '''
    d=[]
    for x in xrange(4):
       d.append(gridstr)
       d.append(flip(gridstr))
       gridstr=spin(gridstr)
       
    return list(set(d))
    
def split(gridstr):
    '''
        >>> split('1234/5678/abcd/efgh')
        ['12/56', '34/78', 'ab/ef', 'cd/gh']
        >>> split('123/456/789')
        ['123/456/789']
    '''
    gridstr2 = gridstr.replace('/','')
    if len(gridstr2) >= 16:
        return [ "/".join((gridstr2[0:2], gridstr2[4:6])),
                 "/".join((gridstr2[2:4], gridstr2[6:8])),
                 "/".join((gridstr2[8:10], gridstr2[12:14])),
                 "/".join((gridstr2[10:12], gridstr2[14:16]))]
    else:
        return [ gridstr ]

mappings={}

def parse_line(line):
    x=re.split("[ =>]* ", line.strip())
    for perm in spinflip(x[0]):
        mappings[perm] = x[1]

with open(sys.argv[1]) as f:
    for l in f.readlines():
        parse_line(l)

print spinflip('.#./..#/###')
grids = [ ".#./..#/###" ]
for x in xrange(5):
    newgrids = []
    for g in grids:
        newgrids.extend(split(mappings[g]))
    grids=newgrids

count=0
for g in grids:
    count+=g.count('#')
print count
