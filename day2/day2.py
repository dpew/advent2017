#!/usr/bin/python
import sys

def chkrow(*vals):
    '''
        >>> chkrow(5, 1, 9, 5)
        8
        >>> chkrow(7, 5, 3)
        4
        >>> chkrow(2, 4, 6, 8)
        6
    '''
    return max(vals) - min(vals)

def chksum(*args):
    '''
        >>> chksum([5, 1, 9, 5], [7, 5, 3] , [2, 4, 6, 8])
        18
    '''
    print args
    return sum(chkrow(*row) for row in args)

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        import doctest
        doctest.testmod()
    else:
        input=[]
        with open(sys.argv[1]) as f:
            print chksum(*[[int(c) for c in r.split()] for r in f.readlines()])
    
