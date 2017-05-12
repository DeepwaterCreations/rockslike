#!/usr/bin/env python3

import sys
import curses

def game_loop():
    pass

def main(stdscr):
    #SETUP
    curses.curs_set(False) #Turn off the cursor
    stdscr.clear() #Clear the screen

    #GAME LOOP
    try:
        game_loop()
    except KeyboardInterrupt:
        pass
    except SystemExit:
        stdscr.refresh()
        sys.exit()

if __name__ == "__main__":
    #This will run the main function in a curses scope, and clean up
    #the terminal mode when the program ends.
    curses.wrapper(main)
