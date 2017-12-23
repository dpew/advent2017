#!/usr/bin/env python

import sys
maze=[int(x) for x in sys.stdin.readlines()]

pos=0
count=0
while pos < len(maze):
    maze[pos] += 1
    pos = pos + maze[pos] -1
    count += 1
print count
