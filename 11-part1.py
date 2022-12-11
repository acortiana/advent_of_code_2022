#!/usr/bin/python3
import fileinput

def do_one_round():
    global monkeys
    for monkey in monkeys:
        for item in monkey['items']:
            monkey['inspection_counter'] += 1
            old = item
            new = eval(monkey['operation'])
            new = int(new / 3)
            if (new % monkey['test']) == 0:
                target_monkey_id = monkey['test_true']
            else:
                target_monkey_id = monkey['test_false']
            monkeys[target_monkey_id]['items'].append(new)
        monkey['items'] = []

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


for i in range(0,20):
    do_one_round()

print(get_monkey_business())