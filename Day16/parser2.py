import curses
import sys
from collections import OrderedDict

fn = 'test.txt'

directions = OrderedDict()
directions['<'] = ( 0, -1)
directions['^'] = (-1,  0)
directions['>'] = ( 0,  1)
directions['v'] = ( 1,  0)

class Deer:
    def __init__(self, visited, points, direction):
        self.visited   = visited
        self.points    = points
        self.direction = direction

def printScr(stdscr, y, x, val, color):
    try:
        stdscr.addstr(y, x, val, color)
    except curses.error:
        pass
    stdscr.refresh()

def isValid(map, y, x):
    return y >= 0 and y < maxY and x >= 0 and x < maxX and map[y][x] in ['.', 'E']

def goDeer(stdscr, map, y, x, deer):
    dead = False

    modY = directions[facing][0]
    modX = directions[facing][1]

    foundEnd = False
    turns = []
    while isValid(map, y, x):
        if map[y][x] == 'E':
            foundEnd = True

        left =
        for direction, dir in directions.items():
            turnY = y + dir[0]
            turnX = x + dir[1]
            if isValid(map, turnY, turnX):
                goDeer(stdscr, map, turnY, turnX, Deer([], deer.points + 1000, direction))
                turns.append((turnY, turnX))

        y = y + modY
        x = x + modX

    if not isValid(map, y, x) and not foundEnd:
        dead = True
    return dead

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

    deerCount = 1
    firstDeer = Deer([], 0, '>')

    while 1:
        if deerCount > 0:
            goDeer(stdscr, map, y, x, firstDeer)

curses.wrapper(main)