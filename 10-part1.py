#!/usr/bin/python3
import fileinput


def evaluate():
    global cycle
    global X
    global total
    if ((cycle - 20) % 40) == 0:
        total += cycle * X


total = 0
X = 1
cycle = 0
for line in fileinput.input():
    line = line.rstrip('\n')
    cycle += 1
    evaluate()
    if line[0:4] == "addx":
        number = int(line[5:])
        cycle += 1
        evaluate()
        X += number

print(total)