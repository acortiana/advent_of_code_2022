#!/usr/bin/python3
import fileinput
from functools import cmp_to_key

def compare_wrapper(input1,input2):
    return compare([input1,input2])

def compare(data):
    if (type(data[0]) == int) and (type(data[1]) == int):
        if data[0] < data[1]:
            return 1
        if data[0] > data[1]:
            return -1
        return 0
    elif (type(data[0]) == list) and (type(data[1]) == list):
        smaller = data[0]
        if len(data[0]) == len(data[1]):
            default_winner = 0
        elif len(data[0]) < len(data[1]):
            default_winner = 1
        else:
            default_winner = -1
            smaller = data[1]
        for i in range(0,len(smaller)):
            result = compare([data[0][i],data[1][i]])
            if result == 0:
                continue
            return result
        return default_winner
    else:
        if (type(data[0]) == int):
            return compare([[data[0]],data[1]])
        else:
            return compare([data[0],[data[1]]])

data = []
for line in fileinput.input():
    line = line.rstrip('\n')
    if line == "":
        continue
    data.append(eval(line))

toadd = [[[2]],[[6]]]
data.extend(toadd)
sorted_data = sorted(data, key=cmp_to_key(compare_wrapper),reverse=True)
results = []
for i in range(0,len(sorted_data)):
    if sorted_data[i] in toadd:
        results.append(i+1)

print(results[0] * results[1])