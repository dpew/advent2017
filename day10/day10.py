#!/usr/bin/env python

import sys

def rotate(lst, count):
    '''
        >>> rotate([0, 1, 2, 3, 4], 3)
        [3, 4, 0, 1, 2]
        >>> rotate([0, 1, 2, 3, 4], 0)
        [0, 1, 2, 3, 4]
        >>> rotate([0, 1, 2, 3, 4], -3)
        [2, 3, 4, 0, 1]
        >>> rotate([0, 1, 2, 3, 4], 5)
        [0, 1, 2, 3, 4]
        >>> rotate([0, 1, 2, 3, 4], -5)
        [0, 1, 2, 3, 4]
        >>> rotate([0, 1, 2, 3, 4], 7)
        [2, 3, 4, 0, 1]
        >>> rotate([0, 1, 2, 3, 4], -7)
        [3, 4, 0, 1, 2]
        >>> rotate([0, 1, 2, 3, 4], -12)
        [3, 4, 0, 1, 2]
    '''
    count = ((count % len(lst)) + len(lst)) % len(lst)
    return lst[count:] + lst[:count]


class CircularList(object):
    def __init__(self, iterable):
       self.position = 0
       self.items = [ x for x in iterable]

    def reverse(self, count):
        '''
            >>> CircularList(range(10)).reverse(5)
            [[4], 3, 2, 1, 0, 5, 6, 7, 8, 9]
            >>> CircularList(range(10)).reverse(1)
            [[0], 1, 2, 3, 4, 5, 6, 7, 8, 9]
            >>> CircularList(range(10)).reverse(0)
            [[0], 1, 2, 3, 4, 5, 6, 7, 8, 9]
            >>> CircularList(range(10)).reverse(10)
            [[9], 8, 7, 6, 5, 4, 3, 2, 1, 0]
        '''
        if count == 0:
            return self

        assert count >= 0
        assert count <= len(self.items)

        tmplist = rotate(self.items, self.position)
        reversed = tmplist[count-1::-1] + tmplist[count:]
        self.items = rotate(reversed, -self.position)
        return self

    def skip(self, count):
        '''
            >>> CircularList(range(10)).skip(2)
            [0, 1, [2], 3, 4, 5, 6, 7, 8, 9]
            >>> CircularList(range(10)).skip(12)
            [0, 1, [2], 3, 4, 5, 6, 7, 8, 9]
            >>> CircularList(range(10)).skip(0)
            [[0], 1, 2, 3, 4, 5, 6, 7, 8, 9]
            >>> CircularList(range(10)).skip(10)
            [[0], 1, 2, 3, 4, 5, 6, 7, 8, 9]
        '''
        self.position = (self.position + count) % len(self.items)
        return self

    def __repr__(self):
        return repr([x[1] if x[0] != self.position else [x[1]] for x in enumerate(self.items)])

    #def __str__(self):
    #    return str(self.items)


def puzzle(count, moves):
    '''
        >>> puzzle(5, [3, 4, 1, 5])
        [3, 4, 2, 1, [0]]
        12
    '''
    c = CircularList(range(count))
    skip=0
    for x in moves:
        c.reverse(x)
        #print 'reverse', x, c
        c.skip(skip + x)
        #print 'skip', skip + x, c
        skip+=1
    print c
    print c.items[0] * c.items[1]

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        import doctest
        doctest.testmod()
    else:
        input=[int(x) for x in sys.argv[1].split(',')]
        print "input", input
        puzzle(256, input)
