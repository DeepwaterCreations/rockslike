#!/usr/bin/env python3

import sys
import curses

def update_world():
    """Generate the results of a single turn"""
    pass

def draw_world():
    """Display the current game state on the screen"""
    pass

def main(stdscr):
    #SETUP
    curses.curs_set(False) #Turn off the cursor
    stdscr.clear() #Clear the screen

    #GAME LOOP
    while True:
        try:
            update_world()
            draw_world()
        except KeyboardInterrupt:
            #The user pressed Ctrl-C
            pass
        except SystemExit:
            stdscr.refresh()
            sys.exit()

if __name__ == "__main__":
    #This will run the main function in a curses scope, and clean up
    #the terminal mode when the program ends.
    curses.wrapper(main)
