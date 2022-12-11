#!/usr/bin/python3
import fileinput

def evaluate():
    global cycle
    global X
    global display
    myvalues = (X-1, X, X+1)
    pixel_position = len(display) % 40
    if pixel_position in myvalues:
        display.append("#")
    else:
        display.append(".")

X = 1
cycle = 0
display = []
for line in fileinput.input():
    line = line.rstrip('\n')
    cycle += 1
    evaluate()
    if line[0:4] == "addx":
        number = int(line[5:])
        cycle += 1
        evaluate()
        X += number

for i in (0,40,80,120,160,200):
    for ii in range(i,i+40):
        print(display[ii],end='')
    print("")