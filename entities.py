"""This module holds creatures and stuff that moves around"""
import curses

import events
from tile import Tile

class Entity():
    """A dynamic object on the map, such as a player or monster"""

    def __init__(self, tile, x, y, get_gameworld_cell):
        self.tile = tile
        self.x = x
        self.y = y
        self.get_gameworld_cell = get_gameworld_cell

        self.inventory = []

    def player_collision(self, player):
        """Called when the player attempts to enter the same cell as this entity

        Return whether the player should complete the move or not.
        """
        return True

    def die(self):
        """Remove this entity from the world"""
        events.trigger_event("on_entity_death", self)

class Player(Entity):
    """A player character"""

    def __init__(self, *args, **kwargs):
        tile = Tile('@', foreground=curses.COLOR_WHITE, background=curses.COLOR_CYAN)
        super(Player, self).__init__(tile, *args, **kwargs)

        #A flag that might temporarily be set to false during the move step if something
        #prevents the player from moving
        self.should_move = True 

        events.listen_to_event("player_move", self.move)
        events.listen_to_event("player_should_stop", self.cancel_move)

    def move(self, x_dir, y_dir):
        """Check the map and move the player in the given direction

        x_dir, y_dir: Values between -1 and 1 specifying the direction the player
        will move along that axis.
        """
        self.should_move = True
        next_coords = (self.x + x_dir, self.y + y_dir)

        #First we directly inform the contents of the next cell that a player is trying
        #to enter it - this way we can minimize the use of the event
        next_cell = self.get_gameworld_cell(*next_coords)
        for thingy in next_cell:
            self.should_move = thingy.player_collision(self)

        #Then we trigger an event for anyone not in the next cell who might care
        #If they stop us from moving, they should trigger "player_should_stop"
        events.trigger_event("player_enter_space", self, *next_coords)

        if self.should_move:
            self.x, self.y = next_coords

    def cancel_move(self):
        """Stop an in-progress movement
        
        Triggered by the 'player_should_stop' event.
        """
        self.should_move = False

    def receive_item(self, item):
        """Add item to the player's inventory"""
        self.inventory.append(item)
        events.trigger_event("print_message", "Picked up {0}".format(item))

class ItemPickup(Entity):
    """An item's presence in the world

    When the player walks over it, they pick it up, which puts its inventory items
    in their inventory and destroys this object.
    """

    def __init__(self, items, *args, **kwargs):
        tile = Tile('%', foreground=curses.COLOR_YELLOW, background=curses.COLOR_BLACK)
        super(ItemPickup, self).__init__(tile, *args, **kwargs)

        self.inventory.extend(items)

    def player_collision(self, player):
        """On player collision, the player gets the contained items"""
        for item in self.inventory:
            player.receive_item(item)
        self.die()
        return True
