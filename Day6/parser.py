import re

fn = 'input.txt'

map = []
guardX = guardY = 0
with open(fn, 'r') as f:
    for y, line in enumerate(f):
        line = line.strip()
        map.append(list(line))
        for x, s in enumerate(line):
            if s == '^':
                guardX = x
                guardY = y

yMod = -1
xMod = 0

newY = guardY
newX = guardX

count = 0
while newY >= 0 and newY < len(map) and newX >= 0 and newX < len(map[0]):
    # If guard hasn't been here already
    if(map[guardY][guardX] != 'X'):
        count = count + 1

    map[guardY][guardX] = 'X'
    #print(*map, sep='\n')

    newY = guardY + yMod
    newX = guardX + xMod

    if newY < 0 or newY >= len(map) or newX < 0 or newX >= len(map[0]):
        break

    if map[newY][newX] == '#':
        # Do turn
        if abs(yMod) == 1:
            xMod = -yMod
            yMod = 0
        elif abs(xMod) == 1:
            yMod = xMod
            xMod = 0

        newY = guardY + yMod
        newX = guardX + xMod
        print('post turn')
        print('yMod: '+str(yMod))
        print('xMod: '+str(xMod))
        print('newY: '+str(newY))
        print('newX: '+str(newX))

    guardY = newY
    guardX = newX

print(*map, sep='\n')
print(count)