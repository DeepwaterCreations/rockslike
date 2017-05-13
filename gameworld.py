class Tile():
    """Holds char and color information for some game object's appearance"""

    def __init__(self, char, color):
        self.char = char
        self.color = color

class MapFeature():
    """A static element of the map, such as a floor or wall tile"""

    def __init__(self, tile):
        self.tile = tile

class Entity():
    """A dynamic object on the map, such as a player or monster"""

    def __init__(self, tile, x, y):
        self.tile = tile
        self.x = x
        self.y = y

class GameWorld():
    """A class to hold the current state of the game world"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map_features = {
                "empty": MapFeature(Tile(' ', None)),
                "floor": MapFeature(Tile('.', None)),
                "wall": MapFeature(Tile('#', None))
                }
        #World is represented by a 2d matrix of lists
        #Each coordinate in the matrix is a cell
        #The list for that cell holds game objects
        #that are located in that cell.
        self._world = [[[self.map_features["floor"]] for x in range(self.width)] for y in range(self.height)]

        #add player to the map
        self._player = Entity(Tile('@', None), self.width//2, self.height//2)
        self._entities = [self._player]
        
    def _flatten_map(self):
        """Returns a matrix where each cell holds the tile of the top game object at that location"""
        flattened = [['' for x in range(self.width)] for y in range(self.height)]
        for y, row in enumerate(self._world):
            for x, cell in enumerate(row):
                flattened[y][x] = cell[len(cell) - 1].tile
        for entity in self._entities:
            flattened[entity.y][entity.x] = entity.tile
        return flattened

    def get(self, x, y):
        """Returns the contents of the cell at x, y"""
        return self._world[y][x]

    def update_world(self, key):
        """Generate the results of a single turn"""
        #TODO: Break key handling into its own function, or maybe even class
        if key in ["y", "7"]:
            self._player.y = max(0, self._player.y - 1)
            self._player.x = max(0, self._player.x - 1)
        if key in ["KEY_UP", "k", "8"]:
            self._player.y = max(0, self._player.y - 1)
        if key in ["u", "9"]:
            self._player.y = max(0, self._player.y - 1)
            self._player.x = min(self.width-1, self._player.x + 1)
        if key in ["KEY_LEFT", "h", "4"]:
            self._player.x = max(0, self._player.x - 1)
        if key in ["KEY_RIGHT", "l", "6"]:
            self._player.x = min(self.width-1, self._player.x + 1)
        if key in ["b", "1"]:
            self._player.y = min(self.height-1, self._player.y + 1)
            self._player.x = max(0, self._player.x - 1)
        if key in ["KEY_DOWN", "j", "2"]:
            self._player.y = min(self.height-1, self._player.y + 1)
        if key in ["n", "3"]:
            self._player.y = min(self.height-1, self._player.y + 1)
            self._player.x = min(self.width-1, self._player.x + 1)

    def as_string(self):
        """Return the top-level tile characters for every cell"""
        #TODO: This won't really work if we want colors.
        worldstring = ""
        flattened = self._flatten_map()
        for row in flattened:
            rowstring = ""
            for tile in row:
                rowstring += tile.char
            worldstring += rowstring
            worldstring += '\n'
        return worldstring

