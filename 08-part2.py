#!/usr/bin/python3
import fileinput

def count_visible_left(x,y):
    global data
    counter = 0
    for i in range(x-1,-1,-1):
        counter += 1
        if data[y][i] >= data[y][x]:
            break
    return counter

def count_visible_right(x,y):
    global data
    global x_len
    counter = 0
    for i in range(x+1,x_len,+1):
        counter += 1
        if data[y][i] >= data[y][x]:
            break
    return counter

def count_visible_up(x,y):
    global data
    counter = 0
    for i in range(y-1,-1,-1):
        counter += 1
        if data[i][x] >= data[y][x]:
            break
    return counter

def count_visible_down(x,y):
    global data
    global y_len
    counter = 0
    for i in range(y+1,y_len,+1):
        counter += 1
        if data[i][x] >= data[y][x]:
            break
    return counter

def get_scenic_score(x,y):
    a = count_visible_left(x,y)
    b = count_visible_right(x,y)
    c = count_visible_down(x,y)
    d = count_visible_up(x,y)
    return a*b*c*d

data = []
for line in fileinput.input():
    data.append(line.rstrip('\n'))

y_len = len(data)
x_len = len(data[0])

best_scenic_score = 0
for y in range(0,y_len):
    for x in range(0,x_len):
        scenic_score = get_scenic_score(x,y)
        if best_scenic_score < scenic_score:
            best_scenic_score = scenic_score


print(best_scenic_score)
