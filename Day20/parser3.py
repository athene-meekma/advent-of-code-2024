import curses
import time
import heapq
import functools

'''
Total cheats: 3455268
Total routes: 1015122

1015122 is too low
'''

test = 3
if test == 1:
    fn = 'test.txt'
    s  = 12
    cheatLength = 2
elif test == 2:
    fn = 'input.txt'
    s  = 100
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
    if len(pathNodes) == 0:
        count = 0
        while not (nodes[y][x].parentY == y and nodes[y][x].parentX == x):
            pathNodes.append((y, x))
            count = count + 1
            printScr(stdscr, y, x, 'O', curses.color_pair(2))
            tempY = nodes[y][x].parentY
            tempX = nodes[y][x].parentX
            y = tempY
            x = tempX
        printScr(stdscr, y, x, 'O', curses.color_pair(2))
        pathNodes.append((y, x))

        testCount = 0
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
                            if True:
                                show = str(y) +','+str(x)
                                show = show + ' '+ str(newY) +','+str(newX)
                                show = show + ' '+str(d)
                                show = show + ' indexStart: '+str(pathNodes.index((y, x))) + ' indexEnd: '+str(pathNodes.index((newY, newX)))
                                show = show + ' addDist: '+str(d)
                                t = ((dist - pathNodes.index((y, x))) + pathNodes.index((newY, newX)) + d)
                                show = show + ' '+str(t)
                                testCount = testCount + 1
                                printScr(stdscr, 8+testCount, maxX+1, show, curses.color_pair(2))
                            cheats.append({
                                'start': (y, x),
                                'end': (newY, newX)
                            })
            printScr(stdscr, 0, maxX+1, 'Processing path nodes '+str(y) +', '+str(x), curses.color_pair(2))
            printScr(stdscr, 1, maxX+1, 'Found cheats '+str(len(cheats)), curses.color_pair(2))
        #printScr(stdscr, y, maxX, 'Processing path nodes', curses.color_pair(2))

    #printScr(stdscr, 0, maxX + 1, 'Steps: '+ dist, curses.color_pair(2))
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
                    #printScr(stdscr, 9, maxX + 1, 'Reached destination!', curses.color_pair(1))
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
        #printScr(stdscr, 9, maxX + 1, 'Couldn\'t find destination', curses.color_pair(1))
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
    global firstTime
    global map
    global startNode
    global endNode
    global cheats
    global cheat

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
                    color = curses.color_pair(3)
                else:
                    color = curses.color_pair(1)
                printScr(stdscr, y, x, val, color)
                map[y].append(val)
    maxY = len(map)
    maxX = len(map[0])
    #for y, row in enumerate(map):
    #    for x, val in enumerate(row):
    #        if val in ['.', 'E', 'S']:
    #            # Find all possible valid locations within 20 steps
    #            for newY in range(y-20, y+20):
    #                for newX in range(x-20, x+20):
    #                    if (abs(y - newY) + abs(x - newX)) <= 20:
    #                        if isValid(map, newY, newX):
    #                            validCount = 0
    #                            for dir in directions:
    #                                tempY = newY + dir[0]
    #                                tempX = newX + dir[1]
    #                                validCount = validCount + isValid(map, tempY, tempX)
    #                            if validCount > 0:
    #                                cheats.append({
    #                                    'start': (y, x),
    #                                    'end': (newY, newX)
    #                                })
    #printScr(stdscr, 4, maxX+1, 'Total cheats: '+str(len(cheats)), curses.color_pair(2))


def main(stdscr):
    global cheats
    global cheat

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)

    generateMap(stdscr)
    doneFirst = False
    saves = {}
    done = False
    total = 0
    while 1:
        if not done:
            steps = findShortestPath(stdscr, map, startNode, endNode)
            count = 2
            if not doneFirst:
                standardSteps = steps
                printScr(stdscr, 2, maxX+1, 'Standard steps: '+str(standardSteps), curses.color_pair(1))
            elif steps <= standardSteps - s:
                saved = standardSteps - steps
                if saved in saves:
                    saves[saved] = saves[saved] + 1
                else:
                    saves[saved] = 1

                total = total + 1

                #total = 0
                #for i, saved in sorted(saves.items(), key=lambda item: item[0]):
                #    printScr(stdscr, count + 5, maxX + 1, str(saved)+' cheats saving '+str(i), curses.color_pair(1))
                #    total = total + saved
                #    count = count + 1
                printScr(stdscr, count + 5, maxX+1, 'Total routes: '+str(total), curses.color_pair(1))

            printScr(stdscr, 5, maxX+1, 'Remaining cheats: '+str(len(cheats)).ljust(7, ' '), curses.color_pair(2))

            if len(cheats) > 0:
                cheat = cheats.pop()
            else:
                done = True
            doneFirst = True

curses.wrapper(main)