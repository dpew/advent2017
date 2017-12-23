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

def densify(iterable, density=16):
    '''
        >>> list(densify(xrange(6), density=3))
        [3, 2]
        >>> list(densify(xrange(7), density=3))
        [3, 2, 6]
        >>> list(densify([65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22]))
        [64]
    '''
    val = 0
    i = 0 
    for x in iterable:
        i += 1
        val = val ^ x
        if not i % density:
           yield val
           val = 0
    if i % density:
        yield val

def hexify(iterable):
    '''
        >>> hexify([64, 7, 255])
        '4007ff'
        >>> hexify([0, 15, 16, 255])
        '000f10ff'
    '''
    return "".join(('0' + hex(x)[2:])[-2:] for x in iterable)

def countbits(val):
    '''
        >>> countbits(0)
        0
        >>> countbits(1)
        1
        >>> countbits(2)
        1
        >>> countbits(15)
        4
    '''
    count=0
    while val:
       count += val & 1
       val = val >> 1
    return count


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

    def hashoper(self, iterable, skip=0):
        '''
            Runs a single knothash function
            returns self, skip

            >>> CircularList(range(5)).hashoper([3, 4, 1, 5])[0]
            [3, 4, 2, 1, [0]]
            >>> l = CircularList(range(5)).hashoper([3, 4, 1, 5])[0]
            >>> l[0] * l[1]
            12
        '''
        for i in iterable:
            self.reverse(i)
            self.skip(skip + i)
            skip += 1
        return self, skip

    def __iter__(self):
        return iter(self.items)

    def __getitem__(self, x):
        return self.items[x]

    def __repr__(self):
        return repr([x[1] if x[0] != self.position else [x[1]] for x in enumerate(self.items)])

def knothash(iterable, repeat=64):
    '''
        >>> knothash('')
        'a2582a3a0e66e6e86e3812dcb672a272'
        >>> knothash('AoC 2017')
        '33efeb34ea91902bb2f59c9920caa6cd'
        >>> knothash('1,2,3')
        '3efbe78a8d82f29979031a4aa0b16a9d'
        >>> knothash('1,2,4')
        '63960835bcdc130f0b66d7ff4f6a5a8e'
    '''
    return hexify(knothashraw(iterable, repeat=repeat))

def knothashraw(iterable, repeat=64):
    counts = [ ord(x) for x in iterable ] + [17, 31, 73, 47, 23]
    c = CircularList(range(256))
    skip = 0
    for x in xrange(repeat):
        skip = c.hashoper(counts, skip)[1]
    return densify(c)


def hashmatrix(key):
    return [ knothashraw("%s-%d" % (key, x)) for x in xrange(128)]
       
if __name__ == '__main__':

    if len(sys.argv) <= 1:
        import doctest
        doctest.testmod(verbose=False)
    else:
        print sum((sum((countbits(b) for b in x)) for x in hashmatrix(sys.argv[1])))
