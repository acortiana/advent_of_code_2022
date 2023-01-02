#!/usr/bin/python3
import fileinput

def cubemin(cube1,cube2):
    if cube1[0] - cube2[0] > 0:
        return cube2
    if cube1[1] - cube2[1] > 0:
        return cube2
    if cube1[2] - cube2[2] > 0:
        return cube2
    return cube1

data = []
for line in fileinput.input():
    line = line.rstrip('\n')
    tmp = tuple([ int(x) for x in line.split(",") ])
    data.append(tmp)

adjacent = set()
for combination in ((0,1,2),(0,2,1),(1,2,0)):
    for cube1 in data:
        for cube2 in data:
            if cube1 == cube2:
                continue
            if cube1[combination[0]] == cube2[combination[0]] and cube1[combination[1]] == cube2[combination[1]]:
                if abs(cube1[combination[2]] - cube2[combination[2]]) == 1:
                    adjacent.add((cubemin(cube1,cube2),combination))

print((len(data) * 6) - (len(adjacent) * 2))