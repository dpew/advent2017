#!/usr/bin/env python


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



if __name__ == '__main__':
    import doctest
    doctest.testmod()
