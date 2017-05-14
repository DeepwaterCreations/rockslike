"""This module holds dungeon features and generally immobile stuff"""
import curses
from tile import Tile

class MapFeature():
    """A static element of the map, such as a floor or wall tile"""

    def __init__(self, tile):
        self.tile = tile

    def player_collision(self, player):
        """Called when the player attempts to enter the same cell as this entity

        Return whether the player should complete the move or not.
        """
        return True

class Floor(MapFeature):
    """A tile the player can walk on"""

    def __init__(self):
        tile = Tile('.', foreground=curses.COLOR_GREEN, background=curses.COLOR_BLACK)
        super(Floor, self).__init__(tile)

class Wall(MapFeature):
    """A tile that blocks the player's movement"""
    #TODO: Block the player's movement

    def __init__(self):
        tile = Tile('#', foreground=curses.COLOR_MAGENTA, background=curses.COLOR_BLACK)
        super(Wall, self).__init__(tile)

class Void(MapFeature):
    """The un-tile. Represents the boundaries of the world map"""

    def __init__(self):
        super(Void, self).__init__(None)

    def player_collision(self, player):
        return False #Stop the player from falling off the edge of the world
