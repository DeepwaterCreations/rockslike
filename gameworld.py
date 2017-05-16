import parsemap
import entities
import mapfeatures
import keyinput

class GameWorld():
    """A class to hold the current state of the game world"""

    def __init__(self, mapfile):
        #World is represented by a 2d matrix of lists
        #Each coordinate in the matrix is a cell
        #The list for that cell holds game objects
        #that are located in that cell.
        self._world, entities_partials = parsemap.parse_file(mapfile)

        self.width = len(self._world[0])
        self.height = len(self._world)

        #Entities are game objects that can see the map and that might move around.
        self._entities = [partial(get_gameworld_cell=self.get) for partial in entities_partials]
        self._player = list(filter(lambda x: isinstance(x, entities.Player), self._entities))[0]

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
        for y, row in enumerate(self._world[o_y:max_y]):
            for x, cell in enumerate(row[o_x:max_x]):
                flattened[y][x] = cell[len(cell) - 1].tile
        #add entity tiles
        for entity in self._entities:
            if o_x <= entity.x < max_x and o_y <= entity.y < max_y:
                e_x = entity.x - o_x
                e_y = entity.y - o_y
                flattened[e_y][e_x] = entity.tile
        return flattened

    def get(self, x, y):
        """Returns the contents of the cell at x, y"""
        if (x < 0 or x > self.width-1) or (y < 0 or y > self.height-1):
            return [mapfeatures.Void()]
        return self._world[y][x]

    def update_world(self, key):
        """Generate the results of a single turn"""
        keyinput.handle_key(key)
