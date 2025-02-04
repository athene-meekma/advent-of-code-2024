import curses
import time
import heapq

fn = 'input.txt'

maxX = 71
maxY = 71

grid = [['.' for _ in range(maxX)] for _ in range(maxY)]
coordinates = []

directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]

count = 0
max = 1024
with open(fn, 'r') as f:
    for line in f:
        count = count + 1
        if count > max:
            break
        line = line.strip()
        (x,y) = list(map(int, line.split(',')))
        coordinates.append((x, y))
        grid[y][x] = '#'

class Node:
    def __init__(self):
        self.parentY       = 0            # Parent cell's row index
        self.parentX       = 0            # Parent cell's column index
        self.cost          = float('inf') # Total cost of the cell (distFromStart + distToGoal)
        self.distFromStart = float('inf') # Cost from start to this cell
        self.distToGoal    = 0            # Heuristic cost from this cell to destination

def getDistToGoal(y, x, endNode):
    return abs(endNode[0] - y) + abs(endNode[1] - x)

def isValid(grid, y, x):
    return y >= 0 and y < maxY and x >= 0 and x < maxX and grid[y][x] in ['.']

def showPath(stdscr, nodes, endNode):
    y = endNode[0]
    x = endNode[1]

    dist = str(nodes[y][x].distFromStart)
    count = 0
    while not (nodes[y][x].parentY == y and nodes[y][x].parentX == x):
        count = count + 1
        printScr(stdscr, y, x, 'O', curses.color_pair(3))
        tempY = nodes[y][x].parentY
        tempX = nodes[y][x].parentX
        y = tempY
        x = tempX
    printScr(stdscr, y, x, 'O', curses.color_pair(3))

    printScr(stdscr, 0, maxX + 1, 'Steps: '+ dist, curses.color_pair(2))
    return

def findShortestPath(stdscr, grid, startNode, endNode):
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

        for dir in directions:
            newY = y + dir[0]
            newX = x + dir[1]

            # If the neighbor is valid and not visited
            if isValid(grid, newY, newX) and not closedNodes[newY][newX]:
                # Calculate new costs/distances
                newDistFromStart = nodes[y][x].distFromStart + 1

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

    # If the destination is not found after visiting all cells
    if not foundEnd:
        printScr(stdscr, maxY + 2, 0, 'Couldn\'t find destination', curses.color_pair(1))

def printScr(stdscr, y, x, val, color):
    try:
        stdscr.addstr(y, x, val, color)
    except curses.error:
        pass
    stdscr.refresh()

def main(stdscr):
    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val == '.':
                printScr(stdscr, y, x, val, curses.color_pair(1))
            else:
                printScr(stdscr, y, x, val, curses.color_pair(2))

    foundEnd = False
    while 1:
        if not foundEnd:
            foundEnd = findShortestPath(stdscr, grid, (0, 0), (maxY-1, maxX-1))

curses.wrapper(main)