import curses
import time
import heapq
import functools

test = 0
if test:
    fn = 'test.txt'
    s  = 50
    cheatLength = 2
else:
    fn = 'input.txt'
    s  = 100
    cheatLength = 20

directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]

cheat = None
cheats = []
firstTime = 1
lines = open(fn, 'r').readlines()
maxX = 0
maxY = 0

class Node:
    def __init__(self):
        self.parentY       = 0            # Parent cell's row index
        self.parentX       = 0            # Parent cell's column index
        self.cost          = float('inf') # Total cost of the cell (distFromStart + distToGoal)
        self.distFromStart = float('inf') # Cost from start to this cell
        self.distToGoal    = 0            # Heuristic cost from this cell to destination

def isValid(map, y, x):
    return y >= 0 and y < maxY and x >= 0 and x < maxX and map[y][x] in ['.', 'S', 'E']

@functools.cache
def getDist(y, x, newY, newX):
    return abs(y - newY) + abs(x - newX)

pathNodes = []
def showPath(stdscr, nodes, endNode):
    global pathNodes
    global cheats
    global cheat

    y = endNode[0]
    x = endNode[1]

    dist = nodes[y][x].distFromStart
    printScr(stdscr, 0, 0, 'Standard steps: '+str(dist), curses.color_pair(1))
    if len(pathNodes) == 0:
        count = 0
        while not (nodes[y][x].parentY == y and nodes[y][x].parentX == x):
            pathNodes.append((y, x))
            count = count + 1
            tempY = nodes[y][x].parentY
            tempX = nodes[y][x].parentX
            y = tempY
            x = tempX
        pathNodes.append((y, x))

        for pathNode in pathNodes:
            y = pathNode[0]
            x = pathNode[1]
            # Find all possible valid locations within cheatLength steps
            for newY in range(y-cheatLength-1, y+cheatLength+1):
                for newX in range(x-cheatLength-1, x+cheatLength+1):
                    d = getDist(y, x, newY, newX)
                    if d <= cheatLength:
                        # (dist - pathNodes.index((y, x))) = distance from start
                        # pathNodes.index((newY, newX))    = distance to end
                        # d = distance traveled during jump
                        # s = picoseconds saved
                        if isValid(map, newY, newX) and (dist - pathNodes.index((y, x))) + pathNodes.index((newY, newX)) + d <= dist - s:
                            cheats.append({
                                'start': (y, x),
                                'end': (newY, newX)
                            })
            printScr(stdscr, 1, 0, 'Processing path nodes '+str(y) +', '+str(x), curses.color_pair(2))
            printScr(stdscr, 2, 0, 'Found cheats '+str(len(cheats)), curses.color_pair(3))

    return dist

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

        distMod = 1
        isCheat = False
        if cheat != None and (y, x) == cheat['start']:
            # Add the cheat distance
            distMod = getDist(cheat['end'][0], cheat['end'][1], y, x)
            newY = cheat['end'][0]
            newX = cheat['end'][1]
            isCheat = True

        for dir in directions:
            if not isCheat:
                newY = y + dir[0]
                newX = x + dir[1]

            # If the neighbor is valid and not visited
            if isValid(map, newY, newX) and not closedNodes[newY][newX]:
                # Calculate new costs/distances
                newDistFromStart = nodes[y][x].distFromStart + distMod
                if (newY, newX) == endNode:
                    # Reached our destination
                    nodes[newY][newX].parentY = y
                    nodes[newY][newX].parentX = x
                    nodes[newY][newX].distFromStart = newDistFromStart
                    return showPath(stdscr, nodes, endNode)
                else:
                    newDistToGoal    = getDist(newY, newX, endNode[0], endNode[1])
                    newCost          = newDistFromStart + newDistToGoal
                    if nodes[newY][newX].cost == float('inf') or nodes[newY][newX].cost > newCost or isCheat:
                        # Add the node to the open list
                        heapq.heappush(openNodes, (newCost, newY, newX))
                        nodes[newY][newX].distFromStart = newDistFromStart
                        nodes[newY][newX].cost = newCost
                        nodes[newY][newX].distToGoal = newDistToGoal
                        nodes[newY][newX].parentY = y
                        nodes[newY][newX].parentX = x

    # If the destination is not found after visiting all cells
    if not foundEnd:
        return float('inf')

def printScr(stdscr, y, x, val, color):
    try:
        stdscr.addstr(y, x, val, color)
    except curses.error:
        pass
    stdscr.refresh()

def generateMap(stdscr):
    global maxX
    global maxY
    global map
    global startNode
    global endNode

    map = []
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
                map[y].append(val)
    maxY = len(map)
    maxX = len(map[0])


def main(stdscr):
    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)

    generateMap(stdscr)
    done = False
    while 1:
        if not done:
            findShortestPath(stdscr, map, startNode, endNode)
            done = True

curses.wrapper(main)