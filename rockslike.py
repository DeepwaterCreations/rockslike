#!/usr/bin/env python3

import sys
import curses
import argparse

import debugoutput
import keyinput
import mapgenfuncs
from gameworld import GameWorld
from screenpanels import MessagePanel, ListMenu

def draw_screen(stdscr, gameworld, gamewindow, panellist, show_debug_text=False):
    """Display the current game state on the screen"""

    #Update non-game panels
    for panel in panellist:
        panel.display()

    #Draw the gameworld to its window
    window_height, window_width = gamewindow.getmaxyx()
    view = gameworld.get_view(view_width=window_width, view_height=window_height, center_on_player=True)
    for y, row in enumerate(view):
        for x, tile in enumerate(row):
            gamewindow.addstr(y, x, tile.char, tile.color)
    gamewindow.refresh()

    #Flush debug text
    if show_debug_text:
        debugoutput.flush_debug_text()

def layout_panels(stdscr):
    """Build panel layout and create sub-windows of stdscr

    Return: A tuple with the game window and a list of other panels
    """
    screen_width = curses.COLS-1
    screen_height = curses.LINES-1
    messagepanel_height = 5
    gamewindow_width = 3 * (screen_width // 4)
    #Arguments for creating sub-windows are height, width, y coord of top, x coord of left
    #0,0 is top left corner of the screen
    messagepanel = MessagePanel(stdscr.subwin(messagepanel_height, gamewindow_width, 0, 0))
    gamewindow = stdscr.subwin(screen_height-messagepanel_height, gamewindow_width, messagepanel_height+1, 0)
    menupanel = ListMenu(stdscr.subwin(screen_height, (screen_width // 4), 0, gamewindow_width+1))
    return (gamewindow, [messagepanel, menupanel])

def main(stdscr):
    #SETUP
    args = get_args()
    curses.curs_set(False) #Turn off the cursor
    stdscr.clear() #Clear the screen

    show_debug_text = args.debugging_output
    debugoutput.init(stdscr)

    gamewindow, panellist = layout_panels(stdscr)
    if args.mapfile:
        gameworld = GameWorld(genfunc=mapgenfuncs.load_from_file, mapfile=args.mapfile)
    else:
        gameworld = GameWorld(genfunc=mapgenfuncs.empty_box, width=20, height=20)

    #GAME LOOP
    while True:
        try:
            draw_screen(stdscr, gameworld, gamewindow, panellist, show_debug_text=show_debug_text)
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
            nargs='?',
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
