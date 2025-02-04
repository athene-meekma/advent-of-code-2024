import pprint

fn = 'input.txt'

robots = []
with open(fn, 'r') as f:
    for line in f:
        parts = line.strip().split(' ')
        p = parts[0].replace('p=', '').split(',')
        v = parts[1].replace('v=', '').split(',')
        robot = {'p': list(map(int, p)), 'v': list(map(int, v))}
        robots.append(robot)

pprint.pprint(robots)

maxX = 101
maxY = 103

seconds = 100
endSpots = []
for robot in robots:
    robot['v'][0] = robot['v'][0] * seconds
    robot['v'][1] = robot['v'][1] * seconds

    x = robot['v'][0] % maxX
    y = robot['v'][1] % maxY

    newX = robot['p'][0] + x
    newY = robot['p'][1] + y

    if newX < 0:
        newX = newX + maxX
    if newX >= maxX:
        newX = newX - maxX

    if newY < 0:
        newY = newY + maxY
    if newY >= maxY:
        newY = newY - maxY

    endSpots.append((newX, newY))

halfX = int(maxX / 2)
halfY = int(maxY / 2)
counts = {'quad1': 0, 'quad2': 0, 'quad3': 0, 'quad4': 0}
map = []
for y in range(maxY):
    map.append([])
    for x in range(maxX):
        map[y].append([])
        if (x, y) in endSpots:
            if x < halfX and y < halfY:
                counts['quad1'] = counts['quad1'] + endSpots.count((x,y))
            elif x < halfX and y > halfY:
                counts['quad2'] = counts['quad2'] + endSpots.count((x,y))
            elif x > halfX and y < halfY:
                counts['quad3'] = counts['quad3'] + endSpots.count((x,y))
            elif x > halfX and y > halfY:
                counts['quad4'] = counts['quad4'] + endSpots.count((x,y))

            print(x, y)
            map[y][x] = str(endSpots.count((x, y)))
        else:
            map[y][x] = '.'

pprint.pprint(map)

total = counts['quad1'] * counts['quad2'] * counts['quad3'] * counts['quad4']
print(total)