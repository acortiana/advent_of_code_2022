#!/usr/bin/python3

def get_priority(mychar):
    asc_value = ord(mychar)
    if  97 <= asc_value <= 122:
        return asc_value - 96
    else:
        return asc_value - 38

def process_string(mystring):
    mylen = len(mystring)
    index1 = int(mylen / 2)
    index2 = -index1
    (string1, string2) = mystring[:index1], mystring[index2:]
    set1 = set([*string1])
    set2 = set([*string2])
    setresult = set1.intersection(set2)
    numeric_result = 0
    for i in setresult:
        numeric_result += get_priority(i)
    return numeric_result


import fileinput

sum = 0
for line in fileinput.input():
    sum += process_string(line.rstrip())

print(sum)
