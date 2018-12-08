#!/usr/bin/python
import sys
from collections import  defaultdict

def chkrow(vals, c):
    '''
        >>> chkrow('abcdef', 2)
        0
        >>> chkrow('bababc', 2)
        1
        >>> chkrow('bababc', 3)
        1
        >>> chkrow('abbcde', 2)
        1
        >>> chkrow('abcccd', 2)
        0
        >>> chkrow('abcccd', 3)
        1
    '''
    d = defaultdict(lambda: 0)
    for v in vals:
        d[v] += 1
    two = len(filter(lambda x: x == c, d.values())) 
    #three = len(filter(lambda x: x == 3, d.values())) 
    return (1 if two > 0 else 0) # + (1 if three > 0 else 0)
    #print d, sum(x[1] for x in d.items()), len(d.keys())

def chksum(*args):
    '''
        >>> chksum('abcdef', 'bababc', 'abbcde', 'abcccd', 'aabcdd', 'abcdee', 'ababab')
        5
    '''
    return sum(chkrow(row, 2) for row in args) * sum(chkrow(row, 3) for row in args)

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

#def sumsum(*args):
#   return sum(evendiv(*row) for row in args)

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        import doctest
        doctest.testmod()
    else:
        input=[]
        with open(sys.argv[1]) as f:
            #print chksum(*[[int(c) for c in r.split()] for r in f.readlines()])
            print chksum(*[[c for c in r] for r in f.readlines()])
    
