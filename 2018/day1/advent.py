#!/usr/bin/python
import sys

def readvals(fname):
    with open(fname) as f:
       for i in f:
           yield int(i)

val=0
seen=set()
found=False
while not found:
    for i in readvals(sys.argv[1]):
        val += i
        if val in seen:
            found=True
            break
        seen.add(val)

print val
