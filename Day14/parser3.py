import pprint
import sys,os
import curses
import time

fn = 'test.txt'

robots = []
with open(fn, 'r') as f:
    for line in f:
        parts = line.strip().split(' ')
        p = parts[0].replace('p=', '').split(',')
        v = parts[1].replace('v=', '').split(',')
        robot = {'p': list(map(int, p)), 'v': list(map(int, v))}
        robots.append(robot)

maxX = 101
maxX = 11
maxY = 103
maxY = 7

seconds = 0

def main(stdscr):
    global seconds
    noMiddle = True

    sc = curses.initscr()
    scr = curses.newpad(maxY, maxX)
    scr.scrollok

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, 94, curses.COLOR_BLACK)

    # Turning on attributes for title
    scr.attron(curses.color_pair(2))
    scr.attron(curses.A_BOLD)

    # Loop where k is the last character pressed
    while 1:
        if noMiddle:
            # Clear and refresh the screen for a blank canvas
            scr.clear()
            scr.refresh(0, 0, 0, 0, sc.getmaxyx()[0] - 1, sc.getmaxyx()[1] - 1)

            seconds = seconds + 1
            points = []

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


                try:
                    if newY > 70:
                        scr.addstr(robot['p'][1], robot['p'][0], 'X', curses.color_pair(2))
                    else:
                        scr.addstr(robot['p'][1], robot['p'][0], 'X', curses.color_pair(1))
                except curses.error:
                    pass

                scr.addstr(0, 0, 'Iter '+str(seconds), curses.color_pair(1))
                # Refresh the screen
                scr.refresh(0, 0, 0, 0, sc.getmaxyx()[0] - 1, sc.getmaxyx()[1] - 1)

            if seconds == 100:
                noMiddle = False

            if (
                (50, 0) in points and (49, 1) in points and (51, 1) in points
            ):
                noMiddle = False

curses.wrapper(main)