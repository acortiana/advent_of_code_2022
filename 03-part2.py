#!/usr/bin/python3

def get_priority(mychar):
    asc_value = ord(mychar)
    if  97 <= asc_value <= 122:
        return asc_value - 96
    else:
        return asc_value - 38

def process_strings(stringlist):
    (string1, string2, string3) = stringlist
    set1 = set([*string1])
    set2 = set([*string2])
    set3 = set([*string3])
    setresult = set1.intersection(set2,set3)
    numeric_result = 0
    for i in setresult:
        numeric_result += get_priority(i)
    return numeric_result


import fileinput

sum = 0
stringlist = []
for line in fileinput.input():
    stringlist.append(line.rstrip())
    if len(stringlist) == 3:
        sum += process_strings(stringlist)
        stringlist = []

print(sum)
