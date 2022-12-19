#!/usr/bin/python3
import fileinput
import re
import sys

def find_manhattan_distance(point1,point2):
    distance1 = abs(point1[0] - point2[0])
    distance2 = abs(point1[1] - point2[1])
    return distance1 + distance2

def find_result_point(x,y):
    multiplier = 4000000
    global data
    global excluded
    match_found = False
    for sensor, beacon, radius in data:
        if find_manhattan_distance(sensor,(x,y)) < radius:
            match_found = True
            break
    if match_found == False:
        myset = set()
        myset.add(((x,y)))
        result = myset.difference(excluded)
        if result:
            return (x*multiplier)+y

def find_manhattan_perimeter(point,radius):
    x_min = 0
    x_max = 4000000
    y_min = 0
    y_max = 4000000
    points = []
    counter1 = radius + 1
    counter2 = 0
    while counter1 >= 0:
        if x_min <= (point[0]+counter1) <= x_max:
            if y_min <= (point[1]+counter2) <= y_max:
                points.append((point[0]+counter1,point[1]+counter2))
            if y_min <= (point[1]-counter2) <= y_max:
                points.append((point[0]+counter1,point[1]-counter2))
        if x_min <= (point[0]-counter1) <= x_max:
            if y_min <= (point[1]+counter2) <= y_max:
                points.append((point[0]-counter1,point[1]+counter2))
            if y_min <= (point[1]-counter2) <= y_max:
                points.append((point[0]-counter1,point[1]-counter2))
        counter1 -= 1
        counter2 += 1
    return points

print("please wait, calculations can take a couple of minutes...", file=sys.stderr)
regex = re.compile("^Sensor at x=([\-0-9]+), y=([\-0-9]+): closest beacon is at x=([\-0-9]+), y=([\-0-9]+)$")
data = []
excluded = set()
for line in fileinput.input():
    line = line.rstrip('\n')
    result = regex.match(line)
    sensor = (int(result[1]), int(result[2]))
    beacon = (int(result[3]), int(result[4]))
    radius = find_manhattan_distance(sensor,beacon)
    data.append((sensor,beacon,radius))
    excluded.add(beacon)

for sensor, beacon, radius in data:
    points = find_manhattan_perimeter(sensor,radius)
    for i in points:
        result = find_result_point(i[0],i[1])
        if result:
            print(result)
            sys.exit(0)