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
        #TEMP:
        self.width = width
        self.height = height

        events.listen_to_event("player_move_n", self.move_n)
        events.listen_to_event("player_move_ne", self.move_ne)
        events.listen_to_event("player_move_e", self.move_e)
        events.listen_to_event("player_move_se", self.move_se)
        events.listen_to_event("player_move_s", self.move_s)
        events.listen_to_event("player_move_sw", self.move_sw)
        events.listen_to_event("player_move_w", self.move_w)
        events.listen_to_event("player_move_nw", self.move_nw)

    def move_n(self, distance=1):
        self.y = max(0, self.y - distance)
    def move_ne(self, distance=1):
        self.y = max(0, self.y - distance)
        self.x = min(self.width-1, self.x + distance)
    def move_e(self, distance=1):
        self.x = min(self.width-1, self.x + distance)
    def move_se(self, distance=1):
        self.y = min(self.height-1, self.y + distance)
        self.x = min(self.width-1, self.x + distance)
    def move_s(self, distance=1):
        self.y = min(self.height-1, self.y + distance)
    def move_sw(self, distance=1):
        self.y = min(self.height-1, self.y + distance)
        self.x = max(0, self.x - distance)
    def move_w(self, distance=1):
        self.x = max(0, self.x - distance)
    def move_nw(self, distance=1):
        self.y = max(0, self.y - distance)
        self.x = max(0, self.x - distance)
