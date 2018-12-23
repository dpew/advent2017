#!/usr/bin/env python

import itertools


def mdistance(p1, p2):
    '''
        Manhattan Distance

        Gives an absolute value of the manhattan distance of two nodes. Each node may have N dimensions. 

        >>> mdistance((8, 9), (8, 9))
        0
        >>> mdistance((8, 9), (9, 9))
        1
        >>> mdistance((8, 9), (9, 10))
        2
        >>> mdistance((8, 9), (9, 7))
        3
        >>> mdistance((8, 9, 10), (9, 7, 5))
        8
        >>> mdistance(xrange(5), xrange(1, 6))
        5
        >>> mdistance((10, 10, 10), (12, 12, 12))
        6
    '''
    return sum(abs(p[0] - p[1]) for p in zip(p1, p2))


def tokenize(s, chars=' '):
    '''
        >>> list(tokenize('pos=<-22356506,24819383,19709017>, r=53389427', 'pos=<,>r= '))
        ['-22356506', '24819383', '19709017', '53389427']
        >>> list(tokenize(' 1234  1 abc3 '))
        ['1234', '1', 'abc3']
        >>> list(tokenize(' 1234  1 abc3 ', 'abc '))
        ['1234', '1', '3']
    '''
    found = []
    for c in s: 
        if c not in chars:
            found.append(c)
        else:
            if found:
                yield ''.join(found)
                found = []
    if found:
       yield ''.join(found)

def addpos(*positions):
    '''
       >>> addpos((1, 2), (1, 2))
       (2, 4)
       >>> addpos((1, 2, 3), (1, 2, 4))
       (2, 4, 7)
       >>> addpos((1, 2, 3), (1, 2, 4), (-2, -4, -7))
       (0, 0, 0)
    '''
    return tuple((sum(p[x] for p in positions) for x in range(len(positions[0]))))

def mintuple(t1, t2):
    '''
        >>> mintuple((-4, 10, 8), (-100, 12, 19))
        (-100, 10, 8)
        >>> mintuple((-4, 10), (-100, 12))
        (-100, 10)
    '''
    return tuple(min(x) for x in zip(t1, t2))
    

def minmax(positions):
    '''
        Returns the minimum and maximum positions.
        The minimum position is a tuple containing the minimum of all positions.
        The maximym position is a tuple containing the maximym of all positions.
        >>> minmax(((-4, 10), (4, -5)))
        ((-4, -5), (4, 10))
        >>> minmax(((-4, 10, 8), (4, -5, 5), (3, 1, 1), (-100, 10, 8)))
        ((-100, -5, 1), (4, 10, 8))
        >>> minmax(((-4, 10, 8),))
        ((-4, 10, 8), (-4, 10, 8))
        >>> minmax(zip(xrange(10), xrange(10)))
        ((0, 0), (9, 9))
    '''
    p2 = iter(itertools.tee(positions, 2))
    return (tuple(min(x) for x in zip(*p2.next())),
            tuple(max(x) for x in zip(*p2.next())))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
