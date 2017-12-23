#!/bin/bash

echo up
up=$(cat "$1" | sed 's/./\0\n/g' | grep \( |wc -l)
echo down
down=$(cat "$1" | sed 's/./\0\n/g' | grep \) |wc -l)
echo $up $down $((up - down))
