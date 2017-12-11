#!/usr/bin/python
import sys
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
    m = Matrix(maxval)
    i = 0
    for p in spiralgen():
        i += 1
        if i > maxval:
            return m
        m.set(p[0], p[1], i)
    
    return m


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

    def __init__(self, size):
        dim=size/2
        line=[0 for x in xrange(dim)]
        self.matrix=[list(line) for x in xrange(dim)]
        self.center_x = self.center_y = dim/2

    def get(self, x, y):
        return self.matrix[self.center_y - y][x + self.center_x[1]]

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

    def __repr__(self):
        return pprint.pformat(self.matrix)



if __name__ == '__main__':
    if len(sys.argv) <= 1:
        import doctest
        doctest.testmod()
    else:
        input=[]
        with open(sys.argv[1]) as f:
            print sumsum(*[[int(c) for c in r.split()] for r in f.readlines()])
    
