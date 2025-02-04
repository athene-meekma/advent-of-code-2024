import curses
import time
from collections import OrderedDict
import heapq

fn = 'input.txt'

# g = the movement cost to move from the starting point to a given square on the grid, following the path generated to get there (distance)
# h = the estimated movement cost to move from that given square on the grid to the final destination (distanceToGoal ish)

class Node:
    def __init__(self):
        self.parentY       = 0            # Parent cell's row index
        self.parentX       = 0            # Parent cell's column index
        self.cost          = float('inf') # Total cost of the cell (distFromStart + distToGoal)
        self.distFromStart = float('inf') # Cost from start to this cell
        self.distToGoal    = 0            # Heuristic cost from this cell to destination
        self.direction     = None         # Direction reindeer is facing at this node

directions = OrderedDict()
directions['<'] = ( 0, -1)
directions['^'] = (-1,  0)
directions['>'] = ( 0,  1)
directions['v'] = ( 1,  0)

def printScr(stdscr, y, x, val, color):
    try:
        stdscr.addstr(y, x, val, color)
    except curses.error:
        pass
    stdscr.refresh()

def getDistance(dir, facing):
    iDir = list(directions.keys()).index(dir)
    iFacing = list(directions.keys()).index(facing)

    if iDir == iFacing:
        # Same direction
        points = 1
    else:
        # Turning
        points = 1001

    return points

def getDistToGoal(y, x, endNode):
    return abs(endNode[0] - y) + abs(endNode[1] - x)

def isValid(map, y, x):
    return y >= 0 and y < maxY and x >= 0 and x < maxX and map[y][x] in ['.', 'E']

def showPath(stdscr, nodes, endNode):
    y = endNode[0]
    x = endNode[1]

    printScr(stdscr, 0, maxX + 1, 'Cost: '+ str(nodes[y][x].distFromStart), curses.color_pair(2))
    count = 0
    while not (nodes[y][x].parentY == y and nodes[y][x].parentX == x):
        count = count + 1
        dir = nodes[y][x].direction
        if dir == None:
            dir = 'E'
        printScr(stdscr, y, x, dir, curses.color_pair(2))
        tempY = nodes[y][x].parentY
        tempX = nodes[y][x].parentX
        y = tempY
        x = tempX
    return

def findShortestPath(stdscr, map, startNode, endNode):
    # Initialize the closed node list (visited nodes)
    closedNodes = [[False for _ in range(maxX)] for _ in range(maxY)]
    # Initialize the details of each node
    nodes = [[Node() for _ in range(maxX)] for _ in range(maxY)]

    y = startNode[0]
    x = startNode[1]

    nodes[y][x].parentY       = y
    nodes[y][x].parentX       = x
    nodes[y][x].cost          = 0
    nodes[y][x].distFromStart = 0
    nodes[y][x].distToGoal    = 0
    nodes[y][x].direction     = '>'

    # Initialize the open node list (cells to be visited) with the start cell
    openNodes = []
    heapq.heappush(openNodes, (0.0, y, x))

    foundEnd = False

    while len(openNodes) > 0:
        # Pop the cell with the smallest f value from the open list
        curNode = heapq.heappop(openNodes)

        # Mark the node as visited
        y = curNode[1]
        x = curNode[2]
        closedNodes[y][x] = True

        for direction, dir in directions.items():
            newY = y + dir[0]
            newX = x + dir[1]

            # If the neighbor is valid and not visited
            if isValid(map, newY, newX) and not closedNodes[newY][newX]:
                # Calculate new costs/distances
                dist = getDistance(direction, nodes[y][x].direction)
                newDistFromStart = nodes[y][x].distFromStart + dist

                if (newY, newX) == endNode:
                    # Reached our destination
                    nodes[newY][newX].parentY = y
                    nodes[newY][newX].parentX = x

                    nodes[newY][newX].distFromStart = newDistFromStart
                    nodes[newY][newX].direction = 'E'

                    printScr(stdscr, maxY, 0, 'Reached destination!', curses.color_pair(1))

                    showPath(stdscr, nodes, endNode)
                    foundEnd = True
                    return foundEnd
                else:
                    newDistToGoal    = getDistToGoal(newY, newX, endNode)
                    newCost          = newDistFromStart + newDistToGoal

                    if nodes[newY][newX].cost == float('inf') or nodes[newY][newX].cost > newCost:
                        # Add the node to the open list
                        heapq.heappush(openNodes, (newCost, newY, newX))
                        nodes[newY][newX].distFromStart = newDistFromStart
                        nodes[newY][newX].cost = newCost
                        nodes[newY][newX].distToGoal = newDistToGoal
                        nodes[newY][newX].parentY = y
                        nodes[newY][newX].parentX = x
                        nodes[newY][newX].direction = direction

    # If the destination is not found after visiting all cells
    if not foundEnd:
        printScr(stdscr, maxY + 2, 0, 'Couldn\'t find destination', curses.color_pair(1))

maxY = 0
maxX = 0
def main(stdscr):
    global maxX
    global maxY

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    map = []
    # Process input and generate our map
    with open(fn, 'r') as f:
        for y, line in enumerate(f):
            line = line.strip()

            map.append([])
            for x, val in enumerate(line):
                if val in ['S', 'E']:
                    if val == 'S':
                        startNode = (y, x)
                    if val == 'E':
                        endNode = (y, x)
                    color = curses.color_pair(2)
                elif val == '#':
                    color = curses.color_pair(3)
                else:
                    color = curses.color_pair(1)
                printScr(stdscr, y, x, val, color)
                map[y].append(val)

    maxY = len(map)
    maxX = len(map[0])
    foundEnd = False

    while 1:
        if not foundEnd:
            foundEnd = findShortestPath(stdscr, map, startNode, endNode)

curses.wrapper(main)