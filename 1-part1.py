#!/usr/bin/python3


import fileinput

sum = 0
mylist = []
for line in fileinput.input():
    if line.rstrip() == "":
        mylist.append(sum)
        sum = 0
        continue
    else:
        sum += int(line.rstrip())

print(max(mylist))
