#!/usr/bin/python3
import fileinput
import re
import sys
import copy
import itertools

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


def fork(data,metadata):
    available_fork_players = 0
    for playerid in range(0,2):
        if metadata['players_minutes_to_destination'][playerid] == 0:
            available_fork_players += 1
            metadata['players_source'][playerid] = metadata['players_destination'][playerid]
    if available_fork_players == 0:
        return 0

    not_available_valves = metadata['touchedvalves']
    available_valves = set(data).difference(metadata['touchedvalves'])
    available_valves_count = len(available_valves)
    
    if available_valves_count == 0:
        return 0

    fork_count = 0
    if available_valves_count == 1 or available_fork_players == 1:
        for playerid in range(0,2):
            if metadata['players_minutes_to_destination'][playerid] != 0:
                continue
            new_source = metadata['players_destination'][playerid]
            computed = 0
            for new_destination in data[new_source]['bestpaths']:
                if new_destination in metadata['touchedvalves']:
                    continue
                computed += 1
                players_minutes_to_destination = data[new_source]['bestpaths'][new_destination]
                mymetadata = copy.deepcopy(metadata)
                mymetadata['players_destination'][playerid] = new_destination
                mymetadata['touchedvalves'].add(new_destination)
                mymetadata['players_minutes_to_destination'][playerid] = players_minutes_to_destination
                compute(data,mymetadata)
                fork_count += 1
        return fork_count
    else:
        new_sources = metadata['players_destination']
        new_destination_pool0 = data[new_sources[0]]['bestpaths']
        new_destination_pool1 = data[new_sources[1]]['bestpaths']
        cartesian_product_destination = itertools.product(new_destination_pool0,new_destination_pool1)
        for i in cartesian_product_destination:
            if i[0] in metadata['touchedvalves'] or i[1] in metadata['touchedvalves']:
                continue
            if i[0] == i[1]:
                continue
            mymetadata = copy.deepcopy(metadata)
            mymetadata['players_destination'][0] = i[0]
            mymetadata['players_destination'][1] = i[1]
            mymetadata['touchedvalves'].add(i[0])
            mymetadata['touchedvalves'].add(i[1])
            mymetadata['players_minutes_to_destination'][0] = data[new_sources[0]]['bestpaths'][i[0]]
            mymetadata['players_minutes_to_destination'][1] = data[new_sources[1]]['bestpaths'][i[1]]
            compute(data,mymetadata)
            fork_count += 1
        return fork_count


def compute(data,metadata):
    global bestvalue
    global maxrate
    while True:
        if fork(data,metadata) != 0:
            return
        all_valves_open = len(metadata['openedvalves']) == len(data)

        mybestvalue = metadata['flowed']
        mybestvalue += (maxrate * metadata['minutes'])
        if all_valves_open:
            if mybestvalue > bestvalue:
                bestvalue = mybestvalue
            return
        else:
            if mybestvalue < bestvalue:
                return
        
    
        for i in metadata['openedvalves']:
            metadata['flowed'] += data[i]['flow_rate']
        if metadata['flowed'] > bestvalue:
            bestvalue = metadata['flowed']
        for playerid in range(0,2):
            source = metadata['players_source'][playerid]
            if source not in metadata['openedvalves']:
                metadata['openedvalves'].append(source)
                continue
            if metadata['players_minutes_to_destination'][playerid] > 0:
                metadata['players_minutes_to_destination'][playerid] -= 1
        if metadata['minutes'] == 1:
            return
        metadata['minutes'] -= 1


print("please wait, calculations can take a couple of hours...", file=sys.stderr)
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

maxrate = 0
for i in data:
    maxrate += data[i]['flow_rate']
bestvalue = 0
start_metadata = {
    'touchedvalves': set(['AA']),
    'openedvalves': ['AA'],
    'flowed': 0,
    'minutes': 26,
    'players_destination': [
        'AA',
        'AA'
    ],
    'players_source': [
        'AA',
        'AA'
    ],
    'players_minutes_to_destination': [
        0,
        0
    ]
}
compute(data,start_metadata)
print(bestvalue)