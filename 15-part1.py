#!/usr/bin/python3
import fileinput
import re

def find_manhattan_distance(point1,point2):
    distance1 = abs(point1[0] - point2[0])
    distance2 = abs(point1[1] - point2[1])
    return distance1 + distance2

def cannot_contain_beacon(sensor,radius,y):
    x = set()
    for i in range(0,(radius - abs(sensor[1] - y))+1):
        x.add(sensor[0] + i)
        x.add(sensor[0] - i)
    return x

regex = re.compile("^Sensor at x=([\-0-9]+), y=([\-0-9]+): closest beacon is at x=([\-0-9]+), y=([\-0-9]+)$")
excluded = set()
points = set()
target_y = 2000000
for line in fileinput.input():
    line = line.rstrip('\n')
    result = regex.match(line)
    (sensor_x, sensor_y, beacon_x, beacon_y) = (int(result[1]), int(result[2]), int(result[3]), int(result[4]))
    if sensor_y == target_y:
        excluded.add(sensor_x)
    if beacon_y == target_y:
        excluded.add(beacon_x)
    radius = find_manhattan_distance((sensor_x, sensor_y),(beacon_x, beacon_y))
    points = points.union(cannot_contain_beacon((sensor_x, sensor_y),radius,target_y))

result = points.difference(excluded)
print(len(result))