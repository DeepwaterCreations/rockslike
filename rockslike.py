#!/usr/bin/env python3

import sys
import curses

from gameworld import GameWorld

def draw_screen(stdscr, gameworld):
    """Display the current game state on the screen"""
    stdscr.addstr(0, 0, gameworld.as_string())
    stdscr.refresh()

def main(stdscr):
    #SETUP
    curses.curs_set(False) #Turn off the cursor
    stdscr.clear() #Clear the screen

    gameworld = GameWorld(curses.COLS-1, curses.LINES-1)

    #GAME LOOP
    while True:
        try:
            draw_screen(stdscr, gameworld)
            key = stdscr.getkey()
            gameworld.update_world(key)
        except KeyboardInterrupt:
            #The user pressed Ctrl-C
            stdscr.refresh()
            sys.exit()
        except SystemExit:
            stdscr.refresh()
            sys.exit()

if __name__ == "__main__":
    #This will run the main function in a curses scope, and clean up
    #the terminal mode when the program ends.
    curses.wrapper(main)
