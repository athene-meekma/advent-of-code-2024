import pprint

fn = 'input.txt'

regions = {}
grid = []
with open(fn, 'r') as f:
    for y, line in enumerate(f):
        vals = list(line.strip())
        for x, val in enumerate(vals):
            if not val in regions:
                regions[val] = []
            regions[val].append((x,y))
        grid.append(list(line.strip()))

processed = []
def findTouching(region, point, matches):
    x = point[0]
    y = point[1]

    processed.append((x,y))

    if not bool(matches):
        matches['points'] = []
        matches['fences'] = 0

    # Gather surrounding values
    up    = grid[y-1][x] if y - 1 >= 0           else None
    down  = grid[y+1][x] if y + 1 < len(grid)    else None
    left  = grid[y][x-1] if x - 1 >= 0           else None
    right = grid[y][x+1] if x + 1 < len(grid[0]) else None
    if (x, y) not in matches['points']:
        matches['points'].append((x, y))
        fences = (up != region) + (down != region) + (left != region) + (right != region)
        matches['fences'] = matches['fences'] + fences
    else:
        # We've already processed this point
        return matches

    if up == region and (x, y-1) not in matches['points']:
        # check up
        matches = findTouching(region, (x, y-1), matches)

    if down == region and (x, y+1) not in matches['points']:
        # check down
        matches = findTouching(region, (x, y+1), matches)

    if left == region and (x-1, y) not in matches['points']:
        # check left
        matches = findTouching(region, (x-1, y), matches)

    if right == region and (x+1, y) not in matches['points']:
        # check right
        matches = findTouching(region, (x+1, y), matches)

    return matches

total = 0
sets = {}
for region, points in regions.items():
    sets[region] = []
    for point in points:
        if not point in processed:
            i = len(sets[region])
            sets[region].append({})
            sets[region][i] = findTouching(region, point, {})

    for set in sets[region]:
        area = len(set['points'])
        fences = set['fences']
        total = total + (area * fences)

print('total '+str(total))