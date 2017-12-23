#!/usr/bin/python

count=0
with open('day4.txt') as f:
   for line in (x.strip().split(' ') for x in f.readlines()):
      if len(line) == len(set(line)): count += 1
print count
      
