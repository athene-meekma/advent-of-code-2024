import pprint
import curses
import time

fn = 'input.txt'

robots = []
with open(fn, 'r') as f:
    for line in f:
        parts = line.strip().split(' ')
        p = parts[0].replace('p=', '').split(',')
        v = parts[1].replace('v=', '').split(',')
        robot = {'p': list(map(int, p)), 'v': list(map(int, v))}
        robots.append(robot)

#pprint.pprint(robots)

maxX = 101
maxY = 103

halfY = int(maxY / 2)

seconds = 0

def main(stdscr):
    global seconds
    noMiddle = True

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, 94, curses.COLOR_BLACK)

    # Turning on attributes for title
    stdscr.attron(curses.color_pair(2))
    stdscr.attron(curses.A_BOLD)

    # Loop where k is the last character pressed
    while 1:
        if noMiddle:
            # Clear and refresh the screen for a blank canvas
            stdscr.clear()
            stdscr.refresh()

            seconds = seconds + 1
            points = []
            count = 0

            for robot in robots:
                newX = robot['p'][0] + robot['v'][0]
                if newX < 0:
                    newX = newX + maxX
                if newX >= maxX:
                    newX =newX - maxX
                robot['p'][0] = newX

                newY = robot['p'][1] + robot['v'][1]
                if newY < 0:
                    newY = newY + maxY
                if newY >= maxY:
                    newY = newY - maxY
                robot['p'][1] = newY

                points.append((newX, newY))

                if newY > halfY:
                    count = count + 1

                newY = newY - 10

                try:
                    if newY > 61:
                        stdscr.addstr(newY, robot['p'][0], 'X', curses.color_pair(2))
                    else:
                        stdscr.addstr(newY, robot['p'][0], 'X', curses.color_pair(1))
                except curses.error:
                    pass

                stdscr.addstr(0, 0, 'Iter '+str(seconds), curses.color_pair(1))
                # Refresh the screen
                stdscr.refresh()

            if (seconds == 7383):
                # Refresh the screen
                stdscr.refresh()
                noMiddle = False
                # Wait for next input
                k = stdscr.getch()

                if k == ord('c'):
                    noMiddle = True

curses.wrapper(main)