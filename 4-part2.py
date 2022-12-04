#!/usr/bin/python3

def process_ranges(string):
    mylist = []
    for myrange in string.split(','):
        mylist.append(myrange.split('-'))
    myvalue = 0
    range1 = set()
    range2 = set()
    for i in range(int(mylist[0][0]),int(mylist[0][1])+1):
        range1.add(i)
    for i in range(int(mylist[1][0]),int(mylist[1][1])+1):
        range2.add(i)
    if range1.intersection(range2):
        return True
    else:
        return False
    

import fileinput

result = 0
for line in fileinput.input():
    if process_ranges(line.rstrip()):
        result+= 1

print(result)