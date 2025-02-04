import re

fn = 'input.txt'

grid = []
trailHeads = []
with open(fn, 'r') as f:
    for y, line in enumerate(f):
        row = line.strip()
        for m in re.finditer('0', row):
            trailHeads.append((m.start(), y))
        grid.append(list(row))

def followTrail(trailEnds, x, y, height):
    if height == 9:
        trailEnds.append((x, y))
        return trailEnds

    # Up
    if y - 1 >= 0:
        newHeight = grid[y - 1][x]
        if newHeight != '.' and int(newHeight) == height + 1:
            trailEnds = followTrail(trailEnds, x, y-1, int(newHeight))
    # Down
    if y + 1 < len(grid):
        newHeight = grid[y + 1][x]
        if newHeight != '.' and int(newHeight) == height + 1:
            trailEnds = followTrail(trailEnds, x, y + 1, int(newHeight))
    # Left
    if x - 1 >= 0:
        newHeight = grid[y][x - 1]
        if newHeight != '.' and int(newHeight) == height + 1:
            trailEnds = followTrail(trailEnds, x - 1, y, int(newHeight))
    # Right
    if x + 1 < len(grid[0]):
        newHeight = grid[y][x + 1]
        if newHeight != '.' and int(newHeight) == height + 1:
            trailEnds = followTrail(trailEnds, x + 1, y, int(newHeight))

    return trailEnds

trailEnds = []
for trailHead in trailHeads:
    x = trailHead[0]
    y = trailHead[1]

    trailEnds.append(followTrail([], x, y, 0))

sum = 0
for end in trailEnds:
    sum = sum + len(set(end))

print(sum)