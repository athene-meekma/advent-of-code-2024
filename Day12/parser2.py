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

def getSurrounding(x, y):
    up    = grid[y-1][x] if y - 1 >= 0           else None
    down  = grid[y+1][x] if y + 1 < len(grid)    else None
    left  = grid[y][x-1] if x - 1 >= 0           else None
    right = grid[y][x+1] if x + 1 < len(grid[0]) else None

    return up, down, left, right

def findTouching(region, point, matches):
    x = point[0]
    y = point[1]

    processed.append((x,y))

    if not bool(matches):
        matches['points'] = []
        matches['edges']  = {}
        matches['fences'] = 0

    # Gather surrounding values
    up, down, left, right = getSurrounding(x, y)

    if (x, y) not in matches['points']:
        matches['points'].append((x, y))

        fences = (up != region) + (down != region) + (left != region) + (right != region)

        if fences > 0:
            matches['edges'][(x,y)] = {}
            matches['edges'][(x,y)]['top']    = up != region
            matches['edges'][(x,y)]['bottom'] = down != region
            matches['edges'][(x,y)]['left']   = left != region
            matches['edges'][(x,y)]['right']  = right != region
            #matches['edges'].append((x,y))

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
        discount = 0
        for edge, borders in set['edges'].items():
            x = edge[0]
            y = edge[1]

            if (x+1, y) in set['edges']:
                if borders['top'] and set['edges'][(x+1,y)]['top']:
                    # Top edge continues
                    discount = discount + 1
                if borders['bottom'] and set['edges'][(x+1,y)]['bottom']:
                    # Bottom edge continues
                    discount = discount + 1

            if (x, y+1) in set['edges']:
                if borders['left'] and set['edges'][(x,y+1)]['left']:
                    # Left edge continues
                    discount = discount + 1
                if borders['right'] and set['edges'][(x,y+1)]['right']:
                    # Right edge continues
                    discount = discount + 1

        area = len(set['points'])
        newFences = set['fences'] - discount
        total = total + (area * newFences)

print('total '+str(total))