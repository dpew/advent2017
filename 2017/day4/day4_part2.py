#!/usr/bin/python

def sort(s):
    x = list(s)
    x.sort()
    return ''.join(x)

count=0
with open('day4.txt') as f:
   for line in (x.strip().split(' ') for x in f.readlines()):
      line = [sort(x) for x in line]
      if len(line) == len(set(line)): count += 1
print count

