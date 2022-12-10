#!/usr/bin/python3
import fileinput
import re

def move_head(direction):
    global chain
    for i in range(0,len(chain[0])):
        chain[0][i] += direction_dict[direction][i]
    for i in range(1,10):
        move_tail(i)

def move_tail(myid):
    global chain
    mindiff_y = 2
    mindiff_x = 2
    if (abs(chain[myid-1][0] - chain[myid][0]) + abs(chain[myid-1][1] - chain[myid][1])) == 3:
        if abs(chain[myid-1][0] - chain[myid][0]) == 2:
            mindiff_x = 1
        else:
            mindiff_y = 1

    if ( chain[myid-1][0] - chain[myid][0] ) == mindiff_y:
        chain[myid][0] += 1
    if ( chain[myid-1][0] - chain[myid][0] ) == -mindiff_y:
        chain[myid][0] -= 1
    if ( chain[myid-1][1] - chain[myid][1] ) == mindiff_x:
        chain[myid][1] += 1
    if ( chain[myid-1][1] - chain[myid][1] ) == -mindiff_x:
        chain[myid][1] -= 1
    if myid == 9:
        tail9_positions.add(tuple(chain[myid]))

direction_dict = {
    'U': (1,0),
    'D': (-1,0),
    'L': (0,-1),
    'R': (0,1)
}

# y,x
chain = []
for i in range(0,10):
    chain.append([0,0])
tail9_positions = set()

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

print(len(tail9_positions))