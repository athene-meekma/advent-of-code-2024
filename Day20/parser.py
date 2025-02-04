import curses
import time
import heapq

test = 0
if test:
    fn = 'test.txt'
else:
    fn = 'input.txt'

directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]

cheats = []
firstTime = 1
lines = open(fn, 'r').readlines()
maxX = 0
maxY = 0
def refresh(stdscr):
    global maxX
    global maxY
    global firstTime
    global map
    global startNode
    global endNode
    global cheats
    global cheatY
    global cheatX

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
                    color = curses.color_pair(2)
                elif val == '#':
                    #if firstTime:
                    #    cheats.append((y, x))
                    color = curses.color_pair(3)
                else:
                    color = curses.color_pair(1)
                printScr(stdscr, y, x, val, color)

                map[y].append(val)
    maxY = len(map)
    maxX = len(map[0])

    if firstTime:
        for y, row in enumerate(map):
            for x, val in enumerate(row):
                if val == '#':
                    validCount = 0
                    for dir in directions:
                        newY = y + dir[0]
                        newX = x + dir[1]
                        validCount = validCount + isValid(map, newY, newX)
                    if validCount > 0:
                        cheats.append((y, x))
        printScr(stdscr, 7, maxX+1, 'Total cheats: '+str(len(cheats)), curses.color_pair(2))

    else:
        (cheatY, cheatX) = cheats.pop()
        map[cheatY][cheatX] = '.'
        printScr(stdscr, cheatY, cheatX, '.', curses.color_pair(1))
        printScr(stdscr, maxY, 0, 'Cheat: '+str(cheatY)+', '+str(cheatX), curses.color_pair(1))
    firstTime = 0

class Node:
    def __init__(self):
        self.parentY       = 0            # Parent cell's row index
        self.parentX       = 0            # Parent cell's column index
        self.cost          = float('inf') # Total cost of the cell (distFromStart + distToGoal)
        self.distFromStart = float('inf') # Cost from start to this cell
        self.distToGoal    = 0            # Heuristic cost from this cell to destination

def getDistToGoal(y, x, endNode):
    return abs(endNode[0] - y) + abs(endNode[1] - x)

def isValid(map, y, x):
    return y >= 0 and y < maxY and x >= 0 and x < maxX and map[y][x] in ['.', 'S', 'E']

def showPath(stdscr, nodes, endNode):
    y = endNode[0]
    x = endNode[1]

    dist = str(nodes[y][x].distFromStart)
    count = 0
    while not (nodes[y][x].parentY == y and nodes[y][x].parentX == x):
        #time.sleep(0.002)
        count = count + 1
        printScr(stdscr, y, x, 'O', curses.color_pair(2))
        tempY = nodes[y][x].parentY
        tempX = nodes[y][x].parentX
        y = tempY
        x = tempX
    printScr(stdscr, y, x, 'O', curses.color_pair(2))

    printScr(stdscr, 0, maxX + 1, 'Steps: '+ dist, curses.color_pair(2))
    return int(dist)

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

        for dir in directions:
            newY = y + dir[0]
            newX = x + dir[1]

            # If the neighbor is valid and not visited
            if isValid(map, newY, newX) and not closedNodes[newY][newX]:
                # Calculate new costs/distances
                newDistFromStart = nodes[y][x].distFromStart + 1

                if (newY, newX) == endNode:
                    # Reached our destination
                    nodes[newY][newX].parentY = y
                    nodes[newY][newX].parentX = x

                    nodes[newY][newX].distFromStart = newDistFromStart

                    printScr(stdscr, 9, maxX + 1, 'Reached destination!', curses.color_pair(1))

                    return showPath(stdscr, nodes, endNode)
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
        printScr(stdscr, 9, maxX + 1, 'Couldn\'t find destination', curses.color_pair(1))

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
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)

    refresh(stdscr)
    doneFirst = False
    saves = {}
    while 1:
        if len(cheats) > 0:
            steps = findShortestPath(stdscr, map, startNode, endNode)
            count = 2
            if not doneFirst:
                standardSteps = steps
                printScr(stdscr, 2, maxX+1, 'Standard steps: '+str(standardSteps), curses.color_pair(1))
            elif steps <= standardSteps - 100:
                saved = standardSteps - steps
                if saved in saves:
                    saves[saved] = saves[saved] + 1
                else:
                    saves[saved] = 1

                total = 0
                for i, saved in saves.items():
                    total = total + saved
                printScr(stdscr, count + 1, maxX+1, 'Total routes: '+str(total), curses.color_pair(1))

            printScr(stdscr, count + 3, maxX+1, 'Remaining cheats: '+str(len(cheats)).ljust(4, ' '), curses.color_pair(2))

            refresh(stdscr)
            doneFirst = True

curses.wrapper(main)