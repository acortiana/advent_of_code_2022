#!/usr/bin/python3
import fileinput
import sys

for line in fileinput.input():
    counter = 0
    for i in range(0,len(line)):
        text_part = line[counter:counter+14]
        if len(set([*text_part])) == 14:
            print(counter+14)
            sys.exit(0)
        counter += 1