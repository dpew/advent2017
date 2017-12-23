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
    return sum(chkrow(*row) for row in args)

def evendiv(*args):
    '''
         >>> evendiv(5, 9, 2, 8)
         4
         >>> evendiv(9, 4, 7, 3)
         3
         >>> evendiv(3, 8, 6, 5)
         2
    '''
    for i in xrange(len(args)):
        d = float(args[i])
        remain=list(args)
        del remain[i]
        # print d, remain
        for x in remain:
           if x / d == int(x/d):
               return int(x/d)
    raise Exception("no divisor")

def sumsum(*args):
   return sum(evendiv(*row) for row in args)

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        import doctest
        doctest.testmod()
    else:
        input=[]
        with open(sys.argv[1]) as f:
            print sumsum(*[[int(c) for c in r.split()] for r in f.readlines()])
    
