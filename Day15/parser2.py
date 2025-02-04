import pprint
import curses
import time

fn = 'input.txt'

directions = {
    '<': (-1,  0),
    '>': ( 1,  0),
    '^': ( 0, -1),
    'v': ( 0,  1)
}

modX = None
modY = None

def get_char_at_pos(stdscr, y, x):
    stdscr.move(y, x)  # Move the cursor to the desired position
    char_int = stdscr.inch()  # Get the character code at the cursor position
    return chr(char_int & 0xFF)  # Convert the character code to a string

def boxCanMove(stdscr, boxLeft, boxRight, y, canMove):
    global modY
    newY = y + modY
    nextLeft = get_char_at_pos(stdscr, newY, boxLeft)
    nextRight = get_char_at_pos(stdscr, newY, boxRight)

    if canMove:
        if nextLeft == '.' and nextRight == '.':
            canMove = True
        elif nextLeft == '#' or nextRight == '#':
            canMove = False
        else:
            if nextLeft == '[':
                canMove = boxCanMove(stdscr, boxLeft, boxRight, newY, canMove)
            elif nextLeft == ']':
                canMove = boxCanMove(stdscr, boxLeft - 1, boxLeft, newY, canMove)

            if nextRight == '[':
                canMove = boxCanMove(stdscr, boxRight, boxRight + 1, newY, canMove)
            elif nextRight == ']':
                canMove = boxCanMove(stdscr, boxLeft, boxRight, newY, canMove)

    return canMove

def moveBoxes(stdscr, boxLeft, boxRight, y):
    global modY
    newY = y + modY
    nextLeft = get_char_at_pos(stdscr, newY, boxLeft)
    nextRight = get_char_at_pos(stdscr, newY, boxRight)

    if nextLeft == '.' and nextRight == '.':
        stdscr.addstr(newY, boxLeft, '[', curses.color_pair(1))
        stdscr.addstr(newY, boxRight, ']', curses.color_pair(1))

        stdscr.addstr(newY - modY, boxLeft, '.', curses.color_pair(4))
        stdscr.addstr(newY - modY, boxRight, '.', curses.color_pair(4))
        #stdscr.refresh()
        #time.sleep(1)
    else:
        # Move next box(es)
        if nextLeft == '[':
            moveBoxes(stdscr, boxLeft, boxRight, newY)
        if nextLeft == ']':
            moveBoxes(stdscr, boxLeft - 1, boxLeft, newY)
        if nextRight == '[':
            moveBoxes(stdscr, boxRight, boxRight + 1, newY)
        # Try moving this one again
        moveBoxes(stdscr, boxLeft, boxRight, y)
    return

def moveRobot(stdscr, robot, next):
    global modX
    global modY

    # Clear previous spot
    stdscr.addstr(robot[1], robot[0], '.', curses.color_pair(4))

    # Set new position
    robot = (robot[0] + modX, robot[1] + modY)

    # Move the robot
    stdscr.addstr(robot[1], robot[0], '@', curses.color_pair(2))


    return robot

def main(stdscr):
    global modX
    global modY

    onMap = True
    map = []
    moves = ''
    end = False

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK)

    # Process input and generate our map
    with open(fn, 'r') as f:
        for y, line in enumerate(f):
            line = line.strip()
            mod = 0

            if onMap:
                if(line == ''):
                    onMap = False
                else:
                    map.append([])
                    for x, val in enumerate(line):
                        if val == '@':
                            robot = (mod + x, y)
                            stdscr.addstr(y, mod + x, '@', curses.color_pair(2))
                            stdscr.addstr(y, mod + x + 1, '.', curses.color_pair(4))
                        elif val == '#':
                            stdscr.addstr(y, mod + x, '#', curses.color_pair(3))
                            stdscr.addstr(y, mod + x + 1, '#', curses.color_pair(3))
                        elif val == 'O':
                            stdscr.addstr(y, mod + x, '[', curses.color_pair(1))
                            stdscr.addstr(y, mod + x + 1, ']', curses.color_pair(1))
                        else:
                            stdscr.addstr(y, mod + x, '.', curses.color_pair(4))
                            stdscr.addstr(y, mod + x + 1, '.', curses.color_pair(4))
                        map[y].append('.')
                        map[y].append('.')
                        mod = mod + 1
            else:
                moves = moves + line

    # Refresh the screen
    stdscr.refresh()

    maxX = len(map[0])
    maxY = len(map)

    moves = list(moves)
    while 1:
        if not end:
            for count, move in enumerate(moves):
                stdscr.addstr(maxY + 1, 0, 'Move '+str(count)+': ' + move, curses.color_pair(1))
                stdscr.refresh()
                time.sleep(0.1)
                modX, modY = directions[move]
                robotY = robot[1]
                robotX = robot[0]

                newY = robotY + modY
                newX = robotX + modX
                # Value at next position
                next = get_char_at_pos(stdscr, newY, newX)

                if next == '#':
                    # Hit a wall, continue
                    continue
                elif next == '.':
                    # We're moving, robot no longer at this position
                    stdscr.addstr(robotY, robotX, '.', curses.color_pair(4))
                    # Robot's new position
                    robot = (newX, newY)
                    stdscr.addstr(newY, newX, '@', curses.color_pair(2))
                elif next == '[' or next == ']':
                    # Attempt to push
                    boxY = newY
                    if next == '[':
                        boxLeft = newX
                        boxRight = newX + 1
                    else:
                        boxLeft = newX - 1
                        boxRight = newX

                    if move in ['<', '>']:
                        # Left/right movement
                        while newX >= 0 and newX + 1 < maxX:
                            nextChar = get_char_at_pos(stdscr, newY, newX)
                            if nextChar == '.':
                                # Shift all the boxes
                                r = range(robotX + (2 * modX), newX + modX, modX)
                                for count, i in enumerate(r):
                                    c = ']' if count % 2 == (1 if move == '>' else 0) else '['
                                    stdscr.addstr(newY, i, c, curses.color_pair(1))

                                # Move robot to new position
                                robot = moveRobot(stdscr, robot, next)

                                break
                            elif nextChar == '#':
                                # Hit a wall, we're done
                                break
                            newY = newY + modY
                            newX = newX + modX
                    else:
                        # Up/down movement
                        canMove = boxCanMove(stdscr, boxLeft, boxRight, newY, True)
                        if canMove:
                            moveBoxes(stdscr, boxLeft, boxRight, newY)

                            # Move robot to new position
                            robot = moveRobot(stdscr, robot, next)

                stdscr.refresh()

            sum = 0
            for y in range(maxY):
                for x in range(maxX):
                    val = get_char_at_pos(stdscr, y, x)
                    if val == '[':
                        sum = sum + (y * 100) + x
            stdscr.addstr(maxY + 2, 0, 'GPS Coordinate: '+str(sum), curses.color_pair(3))
            stdscr.refresh()
            end = True

curses.wrapper(main)