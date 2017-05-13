"""This module holds creatures and stuff that moves around"""
import curses
from tile import Tile

class Entity():
    """A dynamic object on the map, such as a player or monster"""

    def __init__(self, tile, x, y):
        self.tile = tile
        self.x = x
        self.y = y

class Player(Entity):
    """A player character"""

    def __init__(self, x, y):
        tile = Tile('@', foreground=curses.COLOR_WHITE, background=curses.COLOR_CYAN)
        super(Player, self).__init__(tile, x, y)
