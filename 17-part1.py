#!/usr/bin/python3
import fileinput
import sys

obj_template = [
    [(0,0),(1,0),(2,0),(3,0)],
    [(1,0),(0,1),(1,1),(2,1),(1,2)],
    [(0,0),(1,0),(2,0),(2,1),(2,2)],
    [(0,0),(0,1),(0,2),(0,3)],
    [(0,0),(1,0),(0,1),(1,1)],
]

def get_height(data):
    height = -1
    for i in data:
        if i[1] > height:
            height = i[1]
    return height

def spawn_object(number,height):
    objid = number % 5
    myobj = []
    for i in obj_template[objid]:
        myobj.append((i[0]+2,i[1]+4+height))
    return myobj

def move_object(data,obj,direction):
    if direction == "<":
        mydirection = (-1,0)
    elif direction == ">":
        mydirection = (1,0)
    elif direction == "down":
        mydirection = (0,-1)
    newobj = []
    for i in obj:
        newobj.append((i[0]+mydirection[0],i[1]+mydirection[1]))
    return newobj

def collision(data,obj):
    for i in obj:
        if not (0 <= i[0] <= 6):
            return True
        if i[1] < 0:
            return True
        if i in data:
            return True
    return False


# Main
for line in fileinput.input():
    break

data = set()
obj_count = 0
myobj = None
while True:
    for direction in line:
        if myobj == None:
            myobj = spawn_object(obj_count,get_height(data))
        tmp = move_object(data,myobj,direction)
        if not collision(data,tmp):
            myobj = tmp
        tmp = move_object(data,myobj,'down')
        if collision(data,tmp):
            for i in myobj:
                data.add(i)
            myobj = None
            obj_count += 1
        else:
            myobj = tmp
        if obj_count == 2022:
            print(get_height(data)+1)
            sys.exit(0)