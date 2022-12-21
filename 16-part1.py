#!/usr/bin/python3
import fileinput
import re
import sys
import copy

def djkstra_rebuild_initial_datastructure(data,startpoint):
    for i in data:
        data[i]['tmp'] = {
            'shortest_distance': 99999,
            'previous_vertex': None,
            'visited': False
        }
        if i == startpoint:
            data[i]['tmp']['shortest_distance'] = 0

def djkstra_visit(data):
    tovisit = None
    shortest_distance = 99999
    for i in data:
        if data[i]['tmp']['visited'] == True:
            continue
        if data[i]['tmp']['shortest_distance'] < shortest_distance:
            tovisit = i
            shortest_distance = data[i]['tmp']['shortest_distance']
    if tovisit == None:
        return None
    neighbors = data[tovisit]['neighbors']
    for i in neighbors:
        current_best_distance = data[i]['tmp']['shortest_distance']
        new_best_distance = data[tovisit]['tmp']['shortest_distance'] + 1
        if new_best_distance < current_best_distance:
            data[i]['tmp']['shortest_distance'] = new_best_distance
            data[i]['tmp']['previous_vertex'] = tovisit
    data[tovisit]['tmp']['visited'] = True
    return True

def compute_and_load_distances(data,startpoint):
    djkstra_rebuild_initial_datastructure(data,startpoint)
    while True:
        result = djkstra_visit(data)
        if result == None:
            break
    data[startpoint]['bestpaths'] = {}
    for i in data:
        data[startpoint]['bestpaths'][i] = data[i]['tmp']['shortest_distance']

def cleanup(data):
    todelete = []
    for i in data:
        if i == "AA":
            continue
        if data[i]['flow_rate'] != 0:
            continue
        todelete.append(i)
        for ii in data:
            del data[ii]['bestpaths'][i]
    for i in todelete:
        del data[i]
    for i in data:
        del data[i]['neighbors']
        del data[i]['tmp']
        del data[i]['bestpaths'][i]

def compute(data,metadata):
    global bestvalue
    startpoint = metadata['startpoint']
    for i in data[startpoint]['bestpaths']:
        if i in metadata['openedvalves']:
            continue
        if metadata['minutes'] - data[startpoint]['bestpaths'][i] >= 2:
            mymetadata = copy.deepcopy(metadata)
            mymetadata['minutes'] -= data[startpoint]['bestpaths'][i]
            mymetadata['startpoint'] = i
            for ii in mymetadata['openedvalves']:
                mymetadata['flowed'] += data[ii]['flow_rate'] * (data[startpoint]['bestpaths'][i] + 1)
            mymetadata['openedvalves'].append(i)
            mymetadata['minutes'] -= 1
            compute(data,mymetadata)
    for _ in range(metadata['minutes'],0,-1):
        for i in metadata['openedvalves']:
            metadata['flowed'] += data[i]['flow_rate']
    if metadata['flowed'] > bestvalue:
        bestvalue = metadata['flowed']


print("please wait, calculations can take a couple of minutes...", file=sys.stderr)
data = {}
regex = re.compile("^Valve ([A-Z]+) has flow rate=([0-9]+); tunnel(?:s)? lead(?:s)? to valve(?:s)? ([A-Z, ]*)$")
for line in fileinput.input():
    line = line.rstrip('\n')
    result = regex.match(line)
    if not result:
        print("error")
        sys.exit(1)
    (valve_id, flow_rate, valves) = result[1], result[2], result[3].split(', ')
    data[valve_id] = {
        'flow_rate': int(flow_rate),
        'neighbors': valves
    }

for i in data:
    compute_and_load_distances(data,i)

cleanup(data)

bestvalue = 0
start_metadata = {
    'openedvalves': [],
    'flowed': 0,
    'minutes': 30,
    'startpoint': 'AA',
}
compute(data,start_metadata)
print(bestvalue)