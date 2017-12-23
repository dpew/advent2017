#!/usr/bin/python
import sys

def sumdigits(*args):
    '''
        >>> sumdigits(1,1,2,2)
        3
        >>> sumdigits(1,1,1,1)
        4
        >>> sumdigits(1,2,3,4)
        0
        >>> sumdigits(9,1,2,1,2,1,2,9)
        9
        >>> sumdigits(1,2,3,4,1,1,1)
        3
    '''
    sum=0
    if len(args) < 1:
        return 0

    last=int(args[-1])
    for d in args:
        d = int(d)
        if d == last:
            sum += d
        last = d   
    return sum


def sumdigits2(*args):
    '''
        >>> sumdigits2(1,2,1,2)
        6
        >>> sumdigits2(1,2,2,1)
        0
        >>> sumdigits2(1,2,3,4,2,5)
        4
        >>> sumdigits2(1,2,3,1,2,3)
        12
        >>> sumdigits2(1,2,1,3,1,4,1,5)
        4
    '''

    sum=0
    if len(args) < 1:
        return 0

    offset=len(args)/2
    for i in xrange(offset):
        sum += 2 * int(args[i]) if args[i] == args[i+offset] else 0
    return sum

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        import doctest
        doctest.testmod()
    else:
        print sumdigits2(*sys.argv[1])
    
