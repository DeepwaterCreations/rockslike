"""Quarry Depths: A relatively conventional roguelike."""
import curses
import random

import mapgenfuncs
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
        roomlist = bsp(mapgenfuncs.Room, self.width, self.height)
        for room in roomlist:
            mapfeatures = mapgenfuncs.union_mapfeatures(mapfeatures, room.mapfeatures, room.w_x, room.w_y)
            entities.extend(room.entities)
    
        return mapfeatures, entities, player_spawn

def bsp(roomclass, width, height, p_w_x=0, p_w_y=0, iteration=0):
    """Recursively divide a space into halves. When the halves are small enough, generate
    rooms in them, then link the rooms with their neighbor partitions' rooms until all the 
    partitions are linked. bsp = Binary Space Partition
    See http://roguecentral.org/doryen/articles/bsp-dungeon-generation/
    roomclass: The Room class to instantiate when a room is created
    width: The width of the current partition (Initially could be the entire game map)
    height: The height of the current partition
    p_w_x: The partition's x coordinate in world-space (the entire game map)
    p_w_y: The partition's y coordinate in world-space
    iteration: The depth of the recursive function
    """
    # debugoutput.add_debug_string("BSP iteration: {0}".format(iteration))
    max_iterations = 10
    min_room_width = 4
    min_room_height = 4
    width_margin = min_room_width+2 
    height_margin = min_room_height+2
    partition_width_threshold = width_margin*2
    partition_height_threshold = height_margin*2

    #0. Check if we're too small or randomly stop based on depth, and if so, build the room and return it.
    if width <= partition_width_threshold or height <= partition_height_threshold or \
            random.random() < iteration/max_iterations:
        room_p_x = random.randrange(0, width-min_room_width)
        room_p_y = random.randrange(0, height-min_room_height)
        max_room_width = width-room_p_x
        max_room_height = height-room_p_y
        room_w_x = p_w_x + room_p_x
        room_w_y = p_w_y + room_p_y
        return [roomclass((room_w_x, room_w_y), (min_room_width, max_room_width), (min_room_height, max_room_height))]

    #1. Divide the area in half randomly.
    v_split = iteration % 2 == 0
    splitbounds = (width_margin, width-width_margin) if v_split else (height_margin, height-height_margin)
    split = random.randrange(*splitbounds)

    #2. Call bsp on the two halves, collect their roomlists.
    width1 = split if v_split else width
    height1 = split if not v_split else height
    p_w_x1 = p_w_x
    p_w_y1 = p_w_y
    roomlist1 = bsp(roomclass, width1, height1, p_w_x1, p_w_y1, iteration+1)

    width2 = width-split if v_split else width
    height2 = height-split if not v_split else height
    p_w_x2 = p_w_x+split if v_split else p_w_x
    p_w_y2 = p_w_y+split if not v_split else p_w_y
    roomlist2 = bsp(roomclass, width2, height2, p_w_x2, p_w_y2, iteration+1)

    #3. Pick a point in each roomlist and connect them with a corridor.

    #A "corridor" is a room with width or length 0
    #I need to pick 4 points: 2 endpoints, 2 bend points. These points will specify the z-corridor.
    #Endpoints: Pick a random point along the parallel axis, then find where it intersects a room or corridor along
    #   the perpendicular axis,
    #Bendpoints: Pick a random place for the bend, just like picking a split.
    #Also check for intersection.
    #TODO: Implement this

    #4. Return all rooms and corridors.
    return roomlist1 + roomlist2
    # return (roomlist1 + roomlist2).append(corridor)


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

