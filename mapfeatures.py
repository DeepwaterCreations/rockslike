"""This module holds dungeon features and generally immobile stuff"""
from tile import Tile

class MapFeature():
    """A static element of the map, such as a floor or wall tile"""

    def __init__(self, tilechar='?', fgcolor="BLACK", bgcolor="RED", bold=False):
        self.tile = Tile(tilechar, fgcolor, bgcolor, bold)

    def player_collision(self, player):
        """Called when the player attempts to enter the same cell as this entity

        Return whether the player should complete the move or not.
        """
        return True

class Floor(MapFeature):
    """A tile the player can walk on"""

    def __init__(self, tilechar='.', fgcolor="WHITE", bgcolor="BLACK", *args, **kwargs):
        super(Floor, self).__init__(tilechar, fgcolor, bgcolor, *args, **kwargs)

class Wall(MapFeature):
    """A tile that blocks the player's movement"""

    def __init__(self, tilechar='#', fgcolor="WHITE", bgcolor="BLACK", *args, **kwargs):
        super(Wall, self).__init__(tilechar, fgcolor, bgcolor, *args, **kwargs)

    def player_collision(self, player):
        return False #Stop the player from falling off the edge of the world

class Void(MapFeature):
    """The un-tile. Represents the boundaries of the world map"""

    def __init__(self, tilechar=' ', fgcolor="BLACK", bgcolor="BLACK", *args, **kwargs):
        super(Void, self).__init__(tilechar, fgcolor, bgcolor, *args, **kwargs)

    def player_collision(self, player):
        return False #Stop the player from falling off the edge of the world
