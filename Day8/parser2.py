fn = 'input.txt'

y = 0
grid = []
antennas = {}
with open(fn, 'r') as f:
    for line in f:
        vals = list(line.strip())
        for x, val in enumerate(vals):
            if val != '.':
                # Gather antenna positions
                if not val in antennas:
                    antennas[val] = []
                antennas[val].append((x, y))
        grid.append(list(line.strip()))

        y = y + 1

#print(antennas)

nodes = []
for antenna, locations in antennas.items():
    # Only check if we have 2+ antennas
    if len(locations) > 1:
        # For each antenna position
        for pos in locations:
            # For each other antenna position
            for other in locations:
                if other != pos:
                    diffX = other[0] - pos[0]
                    diffY = other[1] - pos[1]

                    # Start at 0 so we count the antenna position
                    count = 0
                    node1 = (pos[0] - (diffX * count), pos[1] - (diffY * count))
                    while (node1[0] >= 0 and node1[0] < len(grid) and
                           node1[1] >= 0 and node1[1] < len(grid[0])):

                        nodes.append(node1)
                        node1 = (pos[0] - (diffX * count), pos[1] - (diffY * count))
                        count = count + 1

                    count = 0
                    node2 = (other[0] + (diffX * count), other[1] + (diffY * count))
                    while (node2[0] >= 0 and node2[0] < len(grid) and
                        node2[1] >= 0 and node2[1] < len(grid[0])):

                        nodes.append(node2)
                        node2 = (other[0] + (diffX * count), other[1] + (diffY * count))
                        count = count + 1

nodes = list(set(nodes))
print(len(nodes))