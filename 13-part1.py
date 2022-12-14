#!/usr/bin/python3
import fileinput

def compare(data):
    if (type(data[0]) == int) and (type(data[1]) == int):
        if data[0] < data[1]:
            return True
        if data[0] > data[1]:
            return False
        return None
    elif (type(data[0]) == list) and (type(data[1]) == list):
        smaller = data[0]
        if len(data[0]) == len(data[1]):
            default_winner = None
        elif len(data[0]) < len(data[1]):
            default_winner = True
        else:
            default_winner = False
            smaller = data[1]
        for i in range(0,len(smaller)):
            result = compare([data[0][i],data[1][i]])
            if result == None:
                continue
            return result
        return default_winner
    else:
        if (type(data[0]) == int):
            return compare([[data[0]],data[1]])
        else:
            return compare([data[0],[data[1]]])

data = []
counter = 0
finalresult = 0
for line in fileinput.input():
    line = line.rstrip('\n')
    if line == "":
        data = []
        continue
    data.append(eval(line))
    if len(data) == 2:
        counter += 1
        if compare(data):
            finalresult += counter

print(finalresult)