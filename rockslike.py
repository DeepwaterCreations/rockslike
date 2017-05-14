#!/usr/bin/env python3

import sys
import curses

import debugoutput
from gameworld import GameWorld

def draw_screen(stdscr, gameworld, show_debug_text=False):
    """Display the current game state on the screen"""
    for y, row in enumerate(gameworld.flatten_map()):
        for x, tile in enumerate(row):
            stdscr.addstr(y, x, tile.char, tile.color)
    if show_debug_text:
        debugoutput.flush_debug_text()
    stdscr.refresh()

def main(stdscr):
    #SETUP
    show_debug_text = True
    debugoutput.init(stdscr)

    curses.curs_set(False) #Turn off the cursor
    stdscr.clear() #Clear the screen

    gameworld = GameWorld(curses.COLS-1, curses.LINES-1)

    #GAME LOOP
    while True:
        try:
            draw_screen(stdscr, gameworld, show_debug_text=show_debug_text)
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
