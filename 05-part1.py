#!/usr/bin/python3
import re
import fileinput

def exec_move(command):
    global crane
    regex = re.compile('^move ([0-9]+) from ([0-9]+) to ([0-9]+)$')
    result = regex.match(command)
    if result:
        quantity = int(result[1])
        src = int(result[2]) - 1
        dst = int(result[3]) - 1
        for i in range(0,quantity):
            tmp = crane[src].pop()
            crane[dst].append(tmp)
    else:
        raise Exception("error")


loading = True
crane = [ [], [], [], [], [], [], [], [], [] ]
for line in fileinput.input():
    line = line.rstrip('\n')
    if line == "":
        continue
    if loading == True:
        if line == " 1   2   3   4   5   6   7   8   9 ":
            loading = False
            continue
        for i in range(1,34,4):
            index = int((i - 1) / 4)
            if line[i].rstrip() != "":
                crane[index].insert(0,line[i])
    else:
        exec_move(line)

for i in crane:
    print(i[-1],end='')
print('')