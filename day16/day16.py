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



if __name__ == '__main__':
    if len(sys.argv) < 2:
        import doctest
        doctest.testmod()
    else:
        d = Dance('abcdefghijklmnop')
        #d = Dance('abcde')
        for x in xrange(1000000000):
            for m in sys.argv[1].split(','):
                d.apply(m.strip())
            if x % 1000 == 0:
                sys.stdout.write('.')
                sys.stdout.flush()
        
        print '------'
        print d
