#!/usr/bin/env python
import sys

class Dance(object):
    def __init__(self, iterable):
        self.programs = list(iterable)

    def spin(self, count):
        '''
            >>> Dance("abcde").spin(3)
            'cdeab'
            >>> Dance("abcde").spin(1)
            'eabcd'
        '''
        self.programs = self.programs[-count:] + self.programs[:-count]
        return self

    def exchange(self, x, y):
        '''
            >>> Dance("eabcd").exchange(3, 4)
            'eabdc'
            >>> Dance("abcde").exchange(0, 2)
            'cbade'
        '''
        t = self.programs[x]
        self.programs[x] = self.programs[y]
        self.programs[y] = t
        return self

    def partner(self, x, y):
        '''
            >>> Dance("eabdc").partner('e', 'b')
            'baedc'
        '''
        return self.exchange(self.programs.index(x), self.programs.index(y))

    def apply(self, move):
        '''
            >>> Dance('abcde').apply('s1')
            'eabcd'
            >>> Dance('eabcd').apply('x3/4')
            'eabdc'
            >>> Dance('eabdc').apply('pe/b')
            'baedc'
        '''
        if move[0] == 's':
            self.spin(int(move[1:]))
        elif move[0] == 'x':
            x, y = move[1:].split('/')
            self.exchange(int(x), int(y))
        elif move[0] == 'p':
            x, y = move[1:].split('/')
            self.partner(x.strip(), y.strip())
        return self

    def __repr__(self):
        return repr(''.join(self.programs))

    def __eq__(self, other):
        '''
            >>> Dance('ab') == Dance('ab')
            True
            >>> Dance('ab') == Dance('ba')
            False
            >>> Dance('abc') == Dance('bca').spin(1)
            True
        '''
        return self.programs == other.programs



if __name__ == '__main__':
    if len(sys.argv) < 2:
        import doctest
        doctest.testmod()
    else:
        first='abcdefghijklmnop'
        d = Dance(first)
        d2 = Dance(first)
        count=int(sys.argv[1])
        for x in xrange(count % 60):
            for m in sys.argv[2].split(','):
                d.apply(m.strip())
            if d == d2:
                print 'Match!', x, d, d2
            if (x+1) % 60 == 0:
                print 'Again!', x, d, d2
#            if x % 58 == 0:
#                print d
        
        print '------'
        print d
