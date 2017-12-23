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
        >>> join([['12/56']])
        '12/56'
        >>> join([['12/56','34/78'], ['ab/ef','cd/gh']])
        '1234/5678/abcd/efgh'
        >>> join([['12/56'], ['34/78'], ['ab/ef'], ['cd/gh']])
        '12/56/34/78/ab/ef/cd/gh'
        >>> join([['12/56','34/78'], ['ab/ef','cd/gh']])
        '1234/5678/abcd/efgh'
    '''
    try:
        matrix = np.vstack(np.hstack(s2m(c) for c in col) for col in grids)
        return m2s(matrix)
    except Exception, e:
        print e

def p(m):
    print "val", m
    return m
    

def split(gridstr):
    '''
        >>> split('1234/5678/abcd/efgh')
        [['12/56', '34/78'], ['ab/ef', 'cd/gh']]
        >>> split('123/456/789')
        [['123/456/789']]
        >>> split('123456/789ABC/DEFGHI/JKLMNO/PQRSTU/VWXYZa')
        [['12/78', '34/9A', '56/BC'], ['DE/JK', 'FG/LM', 'HI/NO'], ['PQ/VW', 'RS/XY', 'TU/Za']]
        >>> split('1234/5678')
        [['12/56', '34/78']]
        >>> split('12/34/56/78')
        [['12/34'], ['56/78']]
    '''
    matrix = s2m(gridstr)
    dim = np.shape(matrix)

    rdiv = 3 if dim[0] % 2 else 2
    cdiv = 3 if dim[1] % 2 else 2
    #print "rdiv", rdiv, "cdiv", cdiv

    rmatrix = []
    for row in xrange(dim[0]/rdiv):
       cmatrix = []
       for col in xrange(dim[1]/cdiv):
 #        print rdiv*row,rdiv*row+rdiv, col*cdiv,cdiv*col+cdiv
           cmatrix.append(m2s(matrix[np.ix_(np.arange(row*rdiv,row*rdiv+rdiv), np.arange(col*cdiv,col*cdiv+cdiv))]))
 #          yield '/'.join(''.join(m) for m in matrix[np.ix_(np.arange(col*divisor,col*divisor+col), np.arange(row*divisor,row*divisor*row))].tolist())
       rmatrix.append(cmatrix)
    return rmatrix

def m2s(m):
    return '/'.join(''.join(m2) for m2 in m.tolist())

def s2m(s):
    '''
        >>> m2s(s2m('12/34'))
        '12/34'
    '''
    return np.matrix([list(x) for x in s.split('/')])


mappings={}
def map(grid):
    try:
        return mappings[grid]
    except KeyError:
        return grid

def parse_line(line):
    x=re.split("[ =>]* ", line.strip())
    for perm in spinflip(x[0]):
        mappings[perm] = x[1]

import doctest
doctest.testmod()

with open(sys.argv[1]) as f:
    for l in f.readlines():
        parse_line(l)

iterations = int(sys.argv[2]) if len(sys.argv) > 2 else 5

grids = [[ ".#./..#/###" ]]
for x in xrange(iterations):
    print "iteration", x
    newgrids = [ [ mappings[row] for row in col] for col in grids ]
    grids=split(join(newgrids))

count=0
for g in join(grids):
    count+=g.count('#')
print count
