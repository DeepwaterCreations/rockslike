"""This module holds creatures and stuff that moves around"""
import curses

import events
from tile import Tile

class Entity():
    """A dynamic object on the map, such as a player or monster"""

    def __init__(self, tile, x, y):
        self.tile = tile
        self.x = x
        self.y = y

class Player(Entity):
    """A player character"""

    def __init__(self, x, y, width, height):
        tile = Tile('@', foreground=curses.COLOR_WHITE, background=curses.COLOR_CYAN)
        super(Player, self).__init__(tile, x, y)

        events.listen_to_event("player_move", self.move)

    def move(self, x_dir, y_dir, distance=1):
        """Move the player 'distance' cells in the given direction

        x_dir, y_dir: Values between -1 and 1 specifying the direction the player
        will move along that axis.
        """
        self.x += x_dir * distance
        self.y += y_dir * distance
