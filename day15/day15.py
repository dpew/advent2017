#!/usr/bin/env python
import sys

divisor=2147483647
twobytes=255 + 255 * 256

def generate(start, factor, multiple):
    val=start
    while True:
        val=int((val * factor) % divisor)
        if val % multiple == 0:
            yield val

def judge(count, iterable1, iterable2):
    matches=0
    i1 = iter(iterable1)
    i2 = iter(iterable2)
    for x in xrange(count):
        if i1.next() & twobytes == i2.next() & twobytes:
            matches+=1        
    return matches

if __name__ == '__main__':
    if len(sys.argv) < 2:
        import doctest
        doctest.testmod()
    else:
        input1=int(sys.argv[2]) if len(sys.argv) > 3 else 1092455
        input2=int(sys.argv[3]) if len(sys.argv) > 3 else 430625591
        print judge(int(sys.argv[1]), generate(input1, 16807, 4), generate(input2, 48271, 8))
