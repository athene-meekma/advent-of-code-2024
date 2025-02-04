import re
import copy

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

def runRoute(obstacle, guardY, guardX):
    loop = False
    turns = {}

    yMod = -1
    xMod = 0

    newY = guardY
    newX = guardX

    while newY >= 0 and newY < len(obstacle) and newX >= 0 and newX < len(obstacle[0]):
        if obstacle[guardY][guardX] != '^':
            if abs(yMod) == 1:
                if obstacle[guardY][guardX] == '-':
                     obstacle[guardY][guardX] = '+'
                else:
                    obstacle[guardY][guardX] = '|'
            elif abs(xMod) == 1:
                if obstacle[guardY][guardX] == '|':
                     obstacle[guardY][guardX] = '+'
                else:
                    obstacle[guardY][guardX] = '-'

        newY = guardY + yMod
        newX = guardX + xMod

        if newY < 0 or newY >= len(obstacle) or newX < 0 or newX >= len(obstacle[0]):
            # New spot is out of bounds
            break

        if obstacle[newY][newX] == '#' or obstacle[newY][newX] == 'O':
            if obstacle[guardY][guardX] != '^':
                obstacle[guardY][guardX] = '+'

            if guardY in turns and guardX in turns[guardY] and [yMod, xMod] in turns[guardY][guardX]:
                loop = True
                break
            else:
                # Add the turn location and direction
                if not guardY in turns:
                    turns[guardY] = {}

                if not guardX in turns[guardY]:
                    turns[guardY][guardX] = []

                turns[guardY][guardX].append([yMod, xMod])

            if abs(yMod) == 1:
                xMod = -yMod
                yMod = 0
            elif abs(xMod) == 1:
                yMod = xMod
                xMod = 0

            newY = guardY + yMod
            newX = guardX + xMod

        if obstacle[newY][newX] != '#' and obstacle[newY][newX] != 'O':
            guardY = newY
            guardX = newX

    #if loop or not loop:
    #    new = []
    #    for o in obstacle:
    #        new.append(''.join(o))
    #    print(*new, sep='\n')
    #    print()
    return loop

count = 0

for y in range(0, len(map)):
    for x in range(0, len(map[0])):
        #print(y, x)
        if not (y == guardY and x == guardX) and not map[y][x] == '#':
            obstacle = copy.deepcopy(map)
            obstacle[y][x] = 'O'

            loop = runRoute(obstacle, guardY, guardX)

            if loop:
                print([y, x])
                count = count + 1

print(count)