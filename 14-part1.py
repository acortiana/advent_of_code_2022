#!/usr/bin/python3
import fileinput

def process_rocks(line):
    global data
    coordinates = line.split(" -> ")
    worst_y = 0
    for i in range(1,len(coordinates)):
        (x1,y1) = [ int(x) for x in coordinates[i-1].split(",") ]
        (x2,y2) = [ int(x) for x in coordinates[i].split(",") ]
        if x1 > x2:
            (x1, x2) = (x2, x1)
        if y1 > y2:
            (y1, y2) = (y2, y1)
        if x1 == x2:
            for ii in range(y1,y2+1):
                data[(x1,ii)] = True
        if y1 == y2:
            for ii in range(x1,x2+1):
                data[(ii,y1)] = True
        if y2 > worst_y:
            worst_y = y2
    return worst_y

def deposit_sand_grain():
    global data
    global worst_y
    position = [500,0]
    while True:
        new_position = (position[0],position[1] + 1)
        if new_position[1] > worst_y:
            return False
        if not (new_position in data):
            position = new_position
            continue
        new_position = (new_position[0] - 1,new_position[1])
        if not (new_position in data):
            position = new_position
            continue
        new_position = (new_position[0] + 2,new_position[1])
        if not (new_position in data):
            position = new_position
            continue
        data[position] = True
        return True
        
data = {}
worst_y = 0
for line in fileinput.input():
    line = line.rstrip('\n')
    bad_y = process_rocks(line)
    if bad_y > worst_y:
        worst_y = bad_y

counter = 0
while deposit_sand_grain() == True:
    counter += 1

print(counter)