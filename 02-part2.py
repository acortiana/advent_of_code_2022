#!/usr/bin/python3


import fileinput


asd = {
        "A X": 3,
        "A Y": 4,
        "A Z": 8,
        "B X": 1,
        "B Y": 5,
        "B Z": 9,
        "C X": 2,
        "C Y": 6,
        "C Z": 7 
}

sum = 0
for line in fileinput.input():
    myline = line.rstrip()
    sum+= int(asd[myline])

print(sum)

