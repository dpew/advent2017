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
    #every=list(args)
    #every.append(args[0])
    if len(args) < 1:
        return 0

    print args
    last=int(args[-1])
    for d in args:
        d = int(d)
        if d == last:
            sum += d
        last = d   
    return sum



if __name__ == '__main__':
    import doctest
    doctest.testmod()

    #print sumdigits(*sys.argv[1:])
    print sumdigits(*sys.argv[1])
    
