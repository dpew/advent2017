#!/usr/bin/env python

import pprint
match=0

def binary(val):
    return "{0:b}".format(val)

def charof(val):
   return "%3d" % (val,)

def chrs(val):
    return ','.join((charof((val >> 16) & 255),
                   charof((val >> 8) & 255),
                   charof((val >> 0) & 255)))


seen=set()
multiple={}
def runmatch(match, maxcount):
    count=0
    a = 65536
    b = 0
    c = 0
    while True:
        largea = a = b | 65536   # line 6
        b = 1250634     # line 7
        while a > 0:
            d = a & 255
            b = b + d
            b = b & 16777215
            b = b * 65899
            b = b & 16777215
            if a in seen:
                if a not in multiple:
                    multiple[a] = count
            if count == maxcount:
                print "FOUND ", a
                return count;
    #c = (d +1) + 256
    #a = d + 1
            # print [0, a, b, c, d]
            # print "%10d %24s %s" % (a, binary(a), chrs(a))
            a = a / 256
            # print [0, a, b, c, d]
            count = count + 1
            seen.add(largea)

print runmatch(47932164, 1000000)
pprint.pprint(sorted((y, x) for x, y in multiple.items()))
