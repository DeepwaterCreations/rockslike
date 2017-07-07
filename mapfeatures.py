"""This module holds dungeon features and generally immobile stuff"""
import events
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

class StairsDown(MapFeature):
    """A tile from which the player can travel to the level below the current one"""
    def __init__(self, dest_coords=None,
                tilechar='>', fgcolor="WHITE", bgcolor="BLACK", bold=True, *args, **kwargs):
        super(StairsDown, self).__init__(tilechar, fgcolor, bgcolor, bold, *args, **kwargs)
        self.dest_coords = dest_coords
    
    def activate_portal(self, target_entity):
        """Change the map and move target_entity (probably the player) to the next map"""
        events.trigger_event("change_map_down")
        if self.dest_coords is not None:
            target_entity.x, target_entity.y = dest_coords

class StairsUp(MapFeature):
    """A tile from which the player can travel to the level above the current one"""
    def __init__(self, dest_coords=None,
                tilechar='<', fgcolor="WHITE", bgcolor="BLACK", bold=True, *args, **kwargs):
        super(StairsDown, self).__init__(tilechar, fgcolor, bgcolor, bold, *args, **kwargs)
        self.dest_coords = dest_coords
    
    def activate_portal(self, target_entity):
        """Change the map and move target_entity (probably the player) to the next map"""
        events.trigger_event("change_map_up")
        if self.dest_coords is not None:
            target_entity.x, target_entity.y = dest_coords

# class MapPortal(MapFeature):
#     """A tile from which the player can travel to other maps"""

#     def __init__(self, dest_map, dest_x, dest_y, 
#             tilechar='>', fgcolor="WHITE", bgcolor="BLACK", bold=True, *args, **kwargs):
#         super(MapPortal, self).__init__(tilechar, fgcolor, bgcolor, bold, *args, **kwargs)
#         self.dest_map = dest_map
#         self.dest_coords = (dest_x, dest_y)

#     def activate_portal(self, target_entity):
#         """Change the map and move target_entity (probably the player) to the portal's
#         destination
#         """
#         self.dest_map.entities.append(target_entity)
#         target_entity.x = self.dest_x
#         target_entity.y = self.dest_y
#         events.trigger_event("change_map", self.dest_map)


        
