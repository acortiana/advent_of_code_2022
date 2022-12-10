#!/usr/bin/python3
import fileinput

def check_visible_left(x,y):
    global data
    for i in range(x-1,-1,-1):
        if data[y][i] >= data[y][x]:
            return False
    return True

def check_visible_right(x,y):
    global data
    global x_len
    for i in range(x+1,x_len,+1):
        if data[y][i] >= data[y][x]:
            return False
    return True

def check_visible_up(x,y):
    global data
    for i in range(y-1,-1,-1):
        if data[i][x] >= data[y][x]:
            return False
    return True

def check_visible_down(x,y):
    global data
    global y_len
    for i in range(y+1,y_len,+1):
        if data[i][x] >= data[y][x]:
            return False
    return True

def check_visible(x,y):
    if check_visible_left(x,y):
        return True
    if check_visible_right(x,y):
        return True
    if check_visible_down(x,y):
        return True
    if check_visible_up(x,y):
        return True
    return False

data = []
for line in fileinput.input():
    data.append(line.rstrip('\n'))

y_len = len(data)
x_len = len(data[0])

total_visible = 0
for y in range(0,y_len):
    for x in range(0,x_len):
        if check_visible(x,y):
            total_visible +=1

print(total_visible)
