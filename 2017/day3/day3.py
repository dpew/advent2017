#!/usr/bin/python
import sys
import math
import pprint

def spiral(maxval):
    '''
        >>> spiral(10)
        [[0, 0, 0, 0, 0],
         [0, 5, 4, 3, 0],
         [0, 6, 1, 2, 0],
         [0, 7, 8, 9, 10],
         [0, 0, 0, 0, 0]]
    '''
    m = Matrix(int(math.sqrt(maxval))+2)
    i = 0
    for p in spiralgen():
        i += 1
        if i > maxval:
            return m
        m.set(p[0], p[1], i)
    
    return m

def sumspiral(width, maxval):
    '''
        >>> sumspiral(5, 747)[0]
        [[147, 142, 133, 122, 59],
         [304, 5, 4, 2, 57],
         [330, 10, 1, 1, 54],
         [351, 11, 23, 25, 26],
         [362, 747, 806, 0, 0]]
    '''
    m = Matrix(width)
    m.set(0, 0, 1)
    for p in spiralgen(): 
        v = m.sumadj(p[0], p[1])
        m.set(p[0], p[1], v)
        if v > maxval:
            return m, v
        

def spiralgen():
    x = 0
    y = 0
    yield 0, 0
    delta = 1
    direction = 1
    while True:
        for i in xrange(delta):
           x += direction
           yield x, y
        for i in xrange(delta):
           y += direction
           yield x, y
        delta += 1
        direction = -direction

class Matrix(object):

    def __init__(self, dim):
        line=[0 for x in xrange(dim)]
        self.matrix=[list(line) for x in xrange(dim)]
        self.center_x = self.center_y = dim/2

    def get(self, x, y):
        '''
            >>> spiral(10).get(0, 0)
            1
            >>> spiral(10).get(1, 1)
            3
            >>> spiral(10).get(1, -1)
            9
            >>> spiral(10).get(10, -12)
            0
            >>> spiral(12).get(-3, 1)
            0
        '''
        try:
            x1 = self.center_x + x
            y1 = self.center_y - y
            if x1 < 0 or y1 < 0:
                 return 0
            return self.matrix[y1][x1]
        except IndexError:
            return 0

    def set(self, x, y, val):
        self.matrix[self.center_y - y][x + self.center_x] = val

    def find(self, val):
        '''
            >>> spiral(10).find(1)
            (0, 0)
            >>> spiral(10).find(4)
            (0, 1)
            >>> spiral(10).find(3)
            (1, 1)
            >>> spiral(10).find(11)
            Traceback (most recent call last):
            ...
            KeyError: 11
        '''
        for r, row in enumerate(self.matrix):
            for c, col in enumerate(row):
                if col == val:
                    return c - self.center_x, self.center_y - r

        raise KeyError(val) 

    def sumadj(self, x, y):
        return sum([self.get(x + x1, y + y1) for x1 in xrange(-1, 2) for y1 in xrange(-1, 2)])

    def __repr__(self):
        return pprint.pformat(self.matrix)



if __name__ == '__main__':
    if len(sys.argv) <= 1:
        import doctest
        doctest.testmod()
    else:
        val=int(sys.argv[1])
        s=spiral(val)
        # print s
        p = s.find(val)
        print p
        print abs(p[0]) + abs(p[1])

        s2, maxval = sumspiral(15, val) 
        print s2
        print maxval
