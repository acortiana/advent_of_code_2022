#!/usr/bin/python3

def process_ranges(string):
    mylist = []
    for myrange in string.split(','):
        mylist.append(myrange.split('-'))
    myvalue = 0
    if (int(mylist[0][0]) == int(mylist[1][0])) or (int(mylist[0][1]) == int(mylist[1][1])):
        return True
    if int(mylist[0][0]) < int(mylist[1][0]):
        myvalue += 1
    if int(mylist[0][1]) > int(mylist[1][1]):
        myvalue += 1
    if (myvalue % 2) == 0:
        return True
    return False

import fileinput

result = 0
for line in fileinput.input():
    if process_ranges(line.rstrip()):
        result+= 1

print(result)