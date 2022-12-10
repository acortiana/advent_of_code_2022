#!/usr/bin/python3
import fileinput
import sys
import re

def add_entry(data,parent):
    fileregex = re.compile('^([0-9]+) ([a-zA-Z0-9\.]+)$')
    dirregex = re.compile('^dir ([a-zA-Z0-9\.]+)$')
    fileresult = fileregex.match(data)
    dirresult = dirregex.match(data)
    if fileresult:
        size = int(fileresult[1])
        name = fileresult[2]
        mytype = 'file'
    elif dirresult:
        size = 0
        name = dirresult[1]
        mytype = 'dir'
    else:
        raise Exception("error")
    target = {
            'parent': parent,
            'children': [],
            'name': name,
            'type': mytype,
            'size': size
    }
    parent['children'].append(target)

def get_child_by_name(name,parent):
    for i in parent['children']:
        if i['name'] == name:
            return i
    return None

def find_child_directories(parent):
    mylist = []
    for i in parent['children']:
        if i['type'] == 'dir':
            mylist.append(i)
            mylist.extend(find_child_directories(i))
    return mylist

def find_dir_size(dir):
    total = 0
    for i in dir['children']:
        if i['type'] == 'dir':
            total += find_dir_size(i)
        else:
            total += i['size']
    return total

root = {
    'parent': None,
    'children': [],
    'name': '',
    'type': 'dir',
    'size': 0
}
cwd = root
cdregex = re.compile('^cd ([a-zA-Z0-9\.]+)$')
ls_data = []
for line in fileinput.input():
    line = line.rstrip('\n')
    if line == '$ cd ..':
        cwd = cwd['parent']
    elif line[0:4] == '$ cd':
        if line[5:] == "/":
            cwd = root
        else:
            cwd = get_child_by_name(line[5:],cwd)
        if cwd == None:
            Exception("error cwd")
    elif line == '$ ls':
        continue
    else:
        add_entry(line,cwd)


total_space = 70000000
total_used_space = find_dir_size(root)
total_free_space = total_space - total_used_space
space_needed_free = 30000000
bytes_to_delete = space_needed_free - total_free_space

curdirectory = None
curdiff = 9999999999999999
cursize = 0
for i in find_child_directories(root):
    mysize = find_dir_size(i)
    mydiff = mysize - bytes_to_delete
    if (mysize >= bytes_to_delete) and (mydiff < curdiff):
        curdirectory = i
        curdiff = mydiff
        cursize = mysize

print(cursize)