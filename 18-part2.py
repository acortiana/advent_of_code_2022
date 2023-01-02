#!/usr/bin/python3
import fileinput

def load_data():
    global data
    for line in fileinput.input():
        line = line.rstrip('\n')
        tmp = tuple([ int(x) for x in line.split(",") ])
        data.append(tmp)

def find_max_min():
    global data
    global data_max
    global data_min
    data_max = [0,0,0]
    data_min = [0,0,0]
    for cube in data:
        for i in range(0,3):
            if cube[i] > data_max[i]:
                data_max[i] = cube[i]
            if cube[i] < data_min[i]:
                data_min[i] = cube[i]

def cube_escaped(cube):
    global data_max
    global data_min
    for i in range(0,3):
        if cube[i] > data_max[i]:
            return True
        if cube[i] < data_min[i]:
            return True
    return False

def find_straight_exit(cube):
    for axis in range(0,3):
        for direction in (-1,1):
            mycube = list(cube)
            while True:
                mycube[axis] += direction
                if tuple(mycube) in data:
                    break
                if cube_escaped(mycube):
                    return True
    return False

def find_exit(cube,processed_cubes):
    global excluded_cubes
    global data
    if cube in processed_cubes:
        return find_straight_exit(cube)
    processed_cubes.add(cube)
    if cube in excluded_cubes:
        return False
    if cube in data:
        return False
    if find_straight_exit(cube):
        return True
    neighbors = [
        (cube[0],cube[1],cube[2]+1),
        (cube[0],cube[1],cube[2]-1),
        (cube[0],cube[1]+1,cube[2]),
        (cube[0],cube[1]-1,cube[2]),
        (cube[0]+1,cube[1],cube[2]),
        (cube[0]-1,cube[1],cube[2])
    ]
    for i in neighbors:
        if find_exit(i,processed_cubes) == True:
            return True
    excluded_cubes.add(cube)
    return False

excluded_cubes = set()
data_max = []
data_min = []
data = []
load_data()
find_max_min()
result = 0

for cube in data:
    mysum = 0
    neighbors = [
        (cube[0],cube[1],cube[2]+1),
        (cube[0],cube[1],cube[2]-1),
        (cube[0],cube[1]+1,cube[2]),
        (cube[0],cube[1]-1,cube[2]),
        (cube[0]+1,cube[1],cube[2]),
        (cube[0]-1,cube[1],cube[2])
    ]
    for i in neighbors:
        processed_cubes = set()
        if find_exit(i,processed_cubes):
            mysum += 1
    result += mysum

print(result)