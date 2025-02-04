import pprint
import sys,os
import curses
import time

fn = 'input.txt'

directions = {
    '<': (-1,  0),
    '>': ( 1,  0),
    '^': ( 0, -1),
    'v': ( 0,  1)
}

def get_char_at_pos(stdscr, y, x):
    stdscr.move(y, x)  # Move the cursor to the desired position
    char_int = stdscr.inch()  # Get the character code at the cursor position
    return chr(char_int & 0xFF)  # Convert the character code to a string

def main(stdscr):
    onMap = True
    map = []
    moves = ''
    end = False

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # Process input and generate our map
    with open(fn, 'r') as f:
        for y, line in enumerate(f):
            line = line.strip()

            if onMap:
                if(line == ''):
                    onMap = False
                else:
                    map.append([])
                    for x, val in enumerate(line):
                        if val == '@':
                            robot = (x, y)
                            stdscr.addstr(y, x, val, curses.color_pair(2))
                        elif val == '#':
                            stdscr.addstr(y, x, val, curses.color_pair(3))
                        else:
                            stdscr.addstr(y, x, val, curses.color_pair(1))
                        map[y].append(val)
            else:
                moves = moves + line

     # Refresh the screen
    stdscr.refresh()

    maxX = len(map)
    maxY = len(map[0])

    moves = list(moves)
    while 1:
        if not end:
            # Clear and refresh the screen for a blank canvas
            stdscr.refresh()

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
                    stdscr.addstr(robotY, robotX, '.', curses.color_pair(1))
                    # Robot's new position
                    robot = (newX, newY)
                    stdscr.addstr(newY, newX, '@', curses.color_pair(2))
                    stdscr.addstr(maxY + 2, 0, '                     ', curses.color_pair(1))
                elif next == 'O':
                    # Attempt to push
                    boxY = newY
                    boxX = newX
                    while newY >= 0 and newY < maxY and newX >= 0 and newX < maxX:
                        nextChar = get_char_at_pos(stdscr, newY, newX)
                        if nextChar == '.':
                            # Move robot to new position
                            stdscr.addstr(robotY, robotX, '.', curses.color_pair(1))
                            stdscr.refresh()
                            # Which is where the box was
                            robot = (boxX, boxY)
                            stdscr.addstr(boxY, boxX, '@', curses.color_pair(2))

                            # Move box to next open position
                            stdscr.addstr(newY, newX, 'O', curses.color_pair(1))
                            break
                        elif nextChar == '#':
                            # Hit a wall, we're done
                            break
                        newY = newY + modY
                        newX = newX + modX
                stdscr.refresh()

            sum = 0
            for y in range(maxY):
                for x in range(maxX):
                    val = get_char_at_pos(stdscr, y, x)
                    if val == 'O':
                        sum = sum + (y * 100) + x
            stdscr.addstr(maxY + 2, 0, 'GPS Coordinate: '+str(sum), curses.color_pair(3))
            stdscr.refresh()
            end = True

curses.wrapper(main)