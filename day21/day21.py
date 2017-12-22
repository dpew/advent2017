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
    
def join(grids):
    '''
        >>> join(['12/56'])
        '12/56'
        >>> join(['12/56','34/78','ab/ef','cd/gh'])
        '1234/5678/abcd/efgh'
        >>> join(['12/56','34/78','ab/ef','cd/gh'])
        '1234/5678/abcd/efgh'
    '''
    if len(grids) == 1:
        return grids[0]

    size=grids[0].count('/')+1
    mlist = [np.matrix([list(elem) for elem in g.split('/')]) for g in grids]
    size=len(mlist)/2
    matrix = np.vstack([np.hstack(mlist[x*size:x*size+size]) for x in xrange(size)])
    return '/'.join(''.join(m) for m in matrix.tolist())
    

def split(gridstr):
    '''
        >>> [x for x in split('1234/5678/abcd/efgh')]
        ['12/56', '34/78', 'ab/ef', 'cd/gh']
        >>> [x for x in split('123/456/789')]
        ['123/456/789']
        >>> [x for x in split('123456/789ABC/DEFGHI/JKLMNO/PQRSTU/VWXYZa')]
        ['12/78', '34/9A', '56/BC', 'DE/JK', 'FG/LM', 'HI/NO', 'PQ/VW', 'RS/XY', 'TU/Za']
    '''
    gridstr2 = gridstr.replace('/','')


    matrix = s2m(gridstr)
    if len(matrix) % 2 == 0:
        divisor = 2
    else:
        divisor = 3
    size = int(len(matrix)/divisor)
    # print "MATRIX",  matrix
    # print size, divisor


    for col in xrange(size):
       for row in xrange(size):
    #       print col*divisor,divisor*col+divisor, divisor*row,divisor*row+divisor
           yield m2s(matrix[np.ix_(np.arange(col*divisor,col*divisor+divisor), np.arange(row*divisor,row*divisor+divisor))])
 #          yield '/'.join(''.join(m) for m in matrix[np.ix_(np.arange(col*divisor,col*divisor+col), np.arange(row*divisor,row*divisor*row))].tolist())

def m2s(m):
    return '/'.join(''.join(m2) for m2 in m.tolist())

def s2m(s):
    '''
        >>> m2s(s2m('12/34'))
        '12/34'
    '''
    return np.matrix([list(x) for x in s.split('/')])


mappings={}

def parse_line(line):
    x=re.split("[ =>]* ", line.strip())
    for perm in spinflip(x[0]):
        mappings[perm] = x[1]

import doctest
doctest.testmod()

with open(sys.argv[1]) as f:
    for l in f.readlines():
        parse_line(l)

print spinflip('.#./..#/###')
grids = [ ".#./..#/###" ]
for x in xrange(5):
    newgrids = []
    for g in grids:
        newgrids.append(mappings[g])
    print "newgrid", newgrids
    print "join", s2m(join(newgrids))
    grids=split(join(newgrids))

count=0
for g in grids:
    count+=g.count('#')
print count
