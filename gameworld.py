import entities
import mapfeatures
import keyinput
import events
import mapgenfuncs

class GameWorld():
    """A class to hold the current state of the game world"""

    def __init__(self, *args, **kwargs):
        #self._mapfeatures is a 2d list that holds things like floors and walls
        #self._entities is a list of dynamic objects, which store their own coordinates

        self.current_map_idx = 0
        self.maplist = [GameMap(self, *args, **kwargs)]
        self._player = entities.Player(*self.maplist[self.current_map_idx].player_spawn, self.get)
        self.load_map(self.maplist[self.current_map_idx])

        events.listen_to_event("on_entity_death", lambda e: self._entities.remove(e))
        events.listen_to_event("world_remove_entity", lambda e: self._entities.remove(e))
        events.listen_to_event("world_add_entity", lambda e: self._entities.append(e))
        events.listen_to_event("change_map", self.change_map)
        events.listen_to_event("change_map_down", self.change_map_down)
        events.listen_to_event("change_map_up", self.change_map_up)

    def get_view(self, view_width=None, view_height=None, origin=(None, None), center_on_player=False):
        """Returns a 2d matrix of the top tiles of a subset of the board"""
        #Set defaults
        if view_width is None:
            view_width = self.width
        if view_height is None:
            view_height = self.height
        o_x, o_y = origin
        if o_x is None:
            o_x = 0
        if o_y is None:
            o_y = 0

        #Constrain view to map size
        view_width = min(view_width, self.width)
        view_height = min(view_height, self.height)
        o_x = min(o_x, self.width-1)
        o_y = min(o_y, self.height-1)

        #center on player
        if center_on_player:
            o_x = min(max(self._player.x - view_width//2, 0), self.width - view_width)
            o_y = min(max(self._player.y - view_height//2, 0), self.height - view_height)

        #Flatten map
        max_x = o_x + view_width
        max_y = o_y + view_height
        flattened = [['' for x in range(view_width)] for y in range(view_height)]
        #Add map feature tiles
        for y, row in enumerate(self._mapfeatures[o_y:max_y]):
            for x, cell in enumerate(row[o_x:max_x]):
                flattened[y][x] = cell.tile
        #add entity tiles
        for entity in self._entities:
            if o_x <= entity.x < max_x and o_y <= entity.y < max_y:
                e_x = entity.x - o_x
                e_y = entity.y - o_y
                flattened[e_y][e_x] = entity.tile
        return flattened

    def get(self, x, y):
        """Returns the contents of the cell at x, y as a (mapfeatures, entities) tuple"""
        if (x < 0 or x > self.width-1) or (y < 0 or y > self.height-1):
            return (mapfeatures.Void(), [])
        cell_entities = list(filter(lambda e: e.x == x and e.y == y, self._entities))
        return (self._mapfeatures[y][x], cell_entities)

    def update_world(self):
        """Generate the results of a single turn"""
        pass

    def change_map_down(self):
        """Set the current map to the next map down. Generate
        a new one if necessary.
        """
        self.change_map(self.current_map_idx + 1)

    def change_map_up(self):
        """Set the current map to the next map up, if we're not at the surface.  """
        if self.current_map_idx > 0:
            self.change_map(self.current_map_idx + 1)

    def change_map(self, depth, *args, **kwargs):
        """Unload the current map and load a new one"""
        #Unload
        self.maplist[self.current_map_idx].on_unload()
        self.maplist[self.current_map_idx]._entities.remove(self._player)

        #Generate new maps if necessary
        while depth >= len(self.maplist):
            new_map = GameMap(self, mapgenfuncs.empty_box, width=self.width, height=self.height)
            self.maplist.append(new_map)

        #Switch to the new map
        self.current_map_idx = depth
        self.load_map(self.maplist[self.current_map_idx])


    def load_map(self, new_map):
        """Set up a new map that the player has just entered"""
        new_map.on_load()

        self._entities = new_map._entities
        self._entities.append(self._player)
        self._player.x = new_map.player_spawn[0]
        self._player.y = new_map.player_spawn[1]

        self._mapfeatures = new_map._mapfeatures
        self.width = len(self._mapfeatures[0])
        self.height = len(self._mapfeatures)


class GameMap():
    """A class for a single map, a collection of which makes up a gameworld"""
    def __init__(self, gameworld, genfunc, *args, **kwargs):
        self.generate = genfunc
        self._mapfeatures, self._entities, self.player_spawn = self.generate(gameworld, *args, **kwargs)

    def generate(self, gameworld):
        """Create the mapfeatures and entities for this map"""
        raise NotImplementedError

    def on_load(self):
        """Called when this map becomes the current map"""
        pass

    def on_unload(self):
        """Called when the player leaves the map"""
        pass
