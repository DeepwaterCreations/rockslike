"""Quarry Depths: A relatively conventional roguelike."""
import curses
import random

import mapgenfuncs
import mapcomponents
import debugoutput
from gameworld import GameWorld, GameMap

class QuarryDepthsGameWorld(GameWorld):

    def __init__(self, *args, **kwargs):
        super(QuarryDepthsGameWorld, self).__init__(*args, **kwargs)

    def create_new_map(self):
        return QuarryDepthsGameMap(self)

class QuarryDepthsGameMap(GameMap):

    def __init__(self, gameworld, *args, **kwargs):
        self.width = 75
        self.height = 50
        super(QuarryDepthsGameMap, self).__init__(gameworld=gameworld, genfunc=self.generate, *args, **kwargs)

    def generate(self, *args, **kwargs):
        mapfeatures = [[]]
        entities = []
        player_spawn = (0,0)

        #First, build rooms and corridors.
        #Then, copy the rooms and corridors into mapfeatures and entities.
        roomlist = mapgenfuncs.bsp(mapcomponents.Room, self.width, self.height)
        for room in roomlist:
            mapfeatures = mapgenfuncs.union_mapfeatures(mapfeatures, room.mapfeatures, room.w_x, room.w_y)
            entities.extend(room.entities)
    
        return mapfeatures, entities, player_spawn



#---
"""Test the gameworld by printing maps to the screen"""
def test_print(stdscr):
    import sys
    curses.curs_set(False) #Turn off the cursor
    debugoutput.init(stdscr)
    gw = QuarryDepthsGameWorld(genfunc=mapgenfuncs.load_from_file, mapfile=open("maps/testmap.map"))
    window_height, window_width = stdscr.getmaxyx()
    while True:
        view = gw.get_view(view_width=window_width, view_height=window_height)
        stdscr.clear()
        for y, row in enumerate(view):
            for x, tile in enumerate(row):
                stdscr.addstr(y, x, tile.char, tile.color)
        debugoutput.flush_debug_text()
        stdscr.refresh()
        key = stdscr.getkey()
        if key == '>':
            gw.change_map_down()
        elif key == '<':
            gw.change_map_up()
        elif key == 'q':
            sys.exit()


if __name__ == "__main__":
    curses.wrapper(test_print)

