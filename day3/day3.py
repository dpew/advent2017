#!/usr/bin/python
import sys
import pprint

def spiral(maxval):
    '''
        >>> spiral(10)
        [[0, 0, 0, 0, 0],
         [0, 5, 4  3, 0] 
         [0, 6, 1, 2, 0]
         [0, 7, 8, 9, 10]
         [0, 0, 0, 0, 0]]
    '''
    m = Matrix(maxval)
    m.set(0, 0, 1)
    m.set(1, 0, 2)
    m.set(1, 1, 3)
    m.set(0, 1, 4)

    return m

    #dim=maxval/2
    #line=[0 for x in xrange(dim)]
    #matrix=[list(line) for x in xrange(dim)]
    #center=[dim/2, dim/2]
    #dx=1
    #dy=0 
    #return matrix

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
    
