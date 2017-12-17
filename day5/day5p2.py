#!/usr/bin/env python

import sys
maze=[int(x) for x in sys.stdin.readlines()]

pos=0
count=0
while pos < len(maze):
    offset = maze[pos]
    maze[pos] += 1 if offset < 3 else -1
    pos += offset
    count += 1
print count
