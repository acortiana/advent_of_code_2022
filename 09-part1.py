#!/usr/bin/python3
import fileinput
import re

def move_head(direction):
    global head
    for i in range(0,len(head)):
        head[i] += direction_dict[direction][i]
    move_tail()

def move_tail():
    global head
    global tail
    global tail_positions
    mindiff_y = 2
    mindiff_x = 2
    if (abs(head[0] - tail[0]) + abs(head[1] - tail[1])) == 3:
        if abs(head[0] - tail[0]) == 2:
            mindiff_x = 1
        else:
            mindiff_y = 1

    if ( head[0] - tail[0] ) == mindiff_y:
        tail[0] += 1
    if ( head[0] - tail[0] ) == -mindiff_y:
        tail[0] -= 1
    if ( head[1] - tail[1] ) == mindiff_x:
        tail[1] += 1
    if ( head[1] - tail[1] ) == -mindiff_x:
        tail[1] -= 1
    tail_positions.add(tuple(tail))

direction_dict = {
    'U': (1,0),
    'D': (-1,0),
    'L': (0,-1),
    'R': (0,1)
}

# y,x
head = [0,0]
tail = [0,0]
tail_positions = set()

regex = re.compile("^([UDLR]) ([0-9]+)")
for line in fileinput.input():
    line = line.rstrip('\n')
    regex_result = regex.match(line)
    if regex_result:
        direction = regex_result[1]
        quantity = int(regex_result[2])
        for i in range(0,quantity):
            move_head(direction)
    else:
        raise Exception("error")

print(len(tail_positions))