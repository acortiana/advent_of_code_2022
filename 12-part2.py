#!/usr/bin/python3
import fileinput
import sys


def djkstra_build_initial_datastructure():
    global lines
    data = {}
    start_vertex = find_vertex_end()
    for y in range(0,len(lines)):
        for x in range(0,len(lines[0])):
                data[(y,x)] = {
                    'shortest_distance': 99999,
                    'previous_vertex': None,
                    'visited': False
                }
                if (y,x) == start_vertex:
                    data[(y,x)]['shortest_distance'] = 0
    return data

def djkstra_visit(data):
    tovisit = None
    shortest_distance = 99999
    for i in data:
        if data[i]['visited'] == True:
            continue
        if data[i]['shortest_distance'] < shortest_distance:
            tovisit = i
            shortest_distance = data[i]['shortest_distance']
    if tovisit == None:
        return None
    neighbors = get_vertex_neighbors(tovisit)
    for i in neighbors:
        current_best_distance = data[i]['shortest_distance']
        new_best_distance = data[tovisit]['shortest_distance'] + 1
        if new_best_distance < current_best_distance:
            data[i]['shortest_distance'] = new_best_distance
            data[i]['previous_vertex'] = tovisit
    data[tovisit]['visited'] = True
    return True

def get_vertex_neighbors(vertex):
    global max_x
    global max_y
    neighbors = []
    candidate_neighbors = (
        (vertex[0] - 1,vertex[1]), # UP
        (vertex[0] + 1,vertex[1]), # DOWN
        (vertex[0],vertex[1] - 1), # LEFT
        (vertex[0],vertex[1] + 1)  # RIGHT
    )
    for i in candidate_neighbors:
        if (0 <= i[0] <= max_y) and (0 <= i[1] <= max_x):
            if (get_vertex_elevation(vertex) - get_vertex_elevation(i)) < 2:
                neighbors.append(i)
    return neighbors


def get_vertex_elevation(vertex):
    global lines
    if vertex == find_vertex_start():
        return ord('a')
    if vertex == find_vertex_end():
        return ord('z')        
    return ord(lines[vertex[0]][vertex[1]])

def find_vertex_from_char(mychar):
    global lines
    for y in range(0,len(lines)):
        for x in range(0,len(lines[0])):
            if lines[y][x] == mychar:
                return (y,x)

def find_vertex_start():
    return find_vertex_from_char('S')

def find_vertex_end():
    return find_vertex_from_char('E')

# Main
lines = []
for line in fileinput.input():
    line = line.rstrip('\n')
    lines.append(line)

max_y = len(lines) - 1
max_x = len(lines[0]) -1

print("please wait, calculations can take a couple of minutes...", file=sys.stderr)
data = djkstra_build_initial_datastructure()
while True:
    result = djkstra_visit(data)
    if result == None:
        break

fewest_steps = 99999
lowest_elevation = get_vertex_elevation(find_vertex_start())
for i in data:
    if get_vertex_elevation(i) != lowest_elevation:
        continue
    if data[i]['shortest_distance'] < fewest_steps:
        fewest_steps = data[i]['shortest_distance']

print(fewest_steps)