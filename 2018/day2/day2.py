#!/usr/bin/python
import sys
from collections import  defaultdict

def diffit(a, b):
    '''
        >>> diffit('abcde', 'axcye')
        2
        >>> diffit('fghij', 'fguij')
        1
    '''
    return len(filter(lambda x: x[0] != x[1], zip(a, b)))

def match(item, boxes):
   mv=len(item)
   m=None
   for b in boxes:
      d = diffit(item, b)
      if d > 0 and d < mv:
          mv = d
          m = b
   return mv, m

def correct(boxes):
    c = []
    fewest=100
    for b in boxes:
       mv, m = match(b, boxes)
       if mv < fewest:
           fewest = mv
       c.append((mv, m))

    return filter(lambda x: x[0] == fewest, c)

def common(a, b):
    '''
        >>> common('abcde', 'axcye')
        'ace'
        >>> common('fghij', 'fguij')
        'fgij'
    '''
    return ''.join(([x[0] for x in filter(lambda x: x[0] == x[1], zip(a, b))]))
    


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        import doctest
        doctest.testmod()
    else:
        input=[]
        with open(sys.argv[1]) as f:
            #print chksum(*[[int(c) for c in r.split()] for r in f.readlines()])
            input = f.readlines()
        x1, x2 =  correct(input)
        print common(x1[1], x2[1])
            #print correct(*[[c for c in r] for r in f.readlines()])
    
