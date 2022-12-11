#!/usr/bin/python3
import fileinput
import sys

def do_one_round():
    global monkeys
    for monkey_id in range(0,len(monkeys)):
        for item in monkeys[monkey_id]['items']:
            monkeys[monkey_id]['inspection_counter'] += 1
            new_item = exec_operation(item,monkeys[monkey_id]['operation'])
            if (new_item[monkey_id] % monkeys[monkey_id]['test']) == 0:
                target_monkey_id = monkeys[monkey_id]['test_true']
            else:
                target_monkey_id = monkeys[monkey_id]['test_false']
            monkeys[target_monkey_id]['items'].append(new_item)
        monkeys[monkey_id]['items'] = []

def exec_operation(item,operation):
    global monkeys
    new_item = []
    for item_part_id in range(0,len(item)):
        old = item[item_part_id]
        new = eval(operation) % monkeys[item_part_id]['test']
        new_item.insert(item_part_id,new)
    new_item = tuple(new_item)
    return new_item

def get_item_from_number(number):
    global monkeys
    result = []
    for monkey in monkeys:
        result.append(number % monkey['test'])
    result = tuple(result)
    return result

def get_monkey_business():
    global monkeys
    counters = []
    for i in monkeys:
        counters.append(i['inspection_counter'])
    counters.sort()
    return counters[-1] * counters[-2]

# Loading
monkeys = []
for line in fileinput.input():
    line = (line.rstrip().lstrip())
    if line[0:6] == "Monkey":
        monkey_id = int(line[7:8])
        monkeys.insert(monkey_id,{})
    elif line[0:6] == "Starti":
        monkeys[monkey_id]['items'] = [ int(x) for x in line[16:].split(', ') ]
    elif line[0:6] == "Operat":
        monkeys[monkey_id]['operation'] = line[17:]
    elif line[0:4] == "Test":
        monkeys[monkey_id]['test'] = int(line[19:])
    elif line[0:7] == "If true":
        monkeys[monkey_id]['test_true'] = int(line[-1])
    elif line[0:7] == "If fals":
        monkeys[monkey_id]['test_false'] = int(line[-1])
    monkeys[monkey_id]['inspection_counter'] = 0

# Transform items
for monkey in monkeys:
    new_items = []
    for item in monkey['items']:
        new_items.append(get_item_from_number(item))
    monkey['items'] = new_items

print("please wait, calculations can take a couple of minutes...", file=sys.stderr)
for i in range(0,10000):
    do_one_round()

print(get_monkey_business())