#!/usr/bin/env python3

import sys
import curses
import argparse

import debugoutput
import keyinput
from gameworld import GameWorld

def draw_screen(stdscr, gameworld, show_debug_text=False):
    """Display the current game state on the screen"""
    view_width = curses.COLS-1
    view_height = curses.LINES-1
    view = gameworld.get_view(view_width=view_width, view_height=view_height, center_on_player=True)
    for y, row in enumerate(view):
        for x, tile in enumerate(row):
            stdscr.addstr(y, x, tile.char, tile.color)
    if show_debug_text:
        debugoutput.flush_debug_text()
    stdscr.refresh()

def main(stdscr):
    #SETUP
    args = get_args()
    curses.curs_set(False) #Turn off the cursor
    stdscr.clear() #Clear the screen

    show_debug_text = args.debugging_output
    debugoutput.init(stdscr)

    gameworld = GameWorld(args.mapfile)

    #GAME LOOP
    while True:
        try:
            draw_screen(stdscr, gameworld, show_debug_text=show_debug_text)
            keyinput.handle_key(stdscr.getkey())
            gameworld.update_world()
        except KeyboardInterrupt:
            #The user pressed Ctrl-C
            stdscr.refresh()
            sys.exit()
        except SystemExit:
            stdscr.refresh()
            sys.exit()

def get_args():
    """Parse the command line arguments and return a dictionary"""
    parser = argparse.ArgumentParser(description="""
        A curses-based roguelike something-or-other

        Movement:
        7 8 9      y k u
         \|/        \|/
        4-@-6  or  h-@-l
         /|\        /|\\
        1 2 3      b j n

        Maps to try are in the maps/ subfolder, or make your own.
            """, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mapfile",
            help="Path to a text file describing a game map",
            type=argparse.FileType('r'))
    parser.add_argument("-D", "--debugging-output", help="Print debugging messages", action="store_true")
    return parser.parse_args()

if __name__ == "__main__":
    #Parse the command line arguments before curses so that the help message can show
    get_args()

    #This will run the main function in a curses scope, and clean up
    #the terminal mode when the program ends.
    curses.wrapper(main)
