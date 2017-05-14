#!/usr/bin/env python3

import sys
import curses

import parsemap
import debugoutput
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
    curses.curs_set(False) #Turn off the cursor
    stdscr.clear() #Clear the screen

    show_debug_text = True
    debugoutput.init(stdscr)

    if len(sys.argv) > 1:
        map_filename = sys.argv[1]
    else:
        map_filename = "/home/Quarry/src/rockslike/maps/testmap.map"
    with open(map_filename) as map_file:
        gamemap = parsemap.parse_map_features(map_file)

    gameworld = GameWorld(gamemap)

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
