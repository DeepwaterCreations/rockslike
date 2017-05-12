class MapFeature():
    """A static element of the map, such as a floor or wall tile"""

    def __init__(self, char):
        self.char = char

    def get_char(self):
        return self.char

class Entity():
    """A dynamic object on the map, such as a player or monster"""

    def __init__(self, char, x, y):
        self.char = char
        self.x = x
        self.y = y

    def get_char(self):
        return self.char

class GameWorld():
    """A class to hold the current state of the game world"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map_features = {
                "empty": MapFeature(' '),
                "floor": MapFeature('.'),
                "wall": MapFeature('#')
                }
        #World is represented by a 2d matrix of lists
        #Each coordinate in the matrix is a tile
        #The list for that tile holds game objects
        #that are located in that tile.
        self._world = [[[self.map_features["floor"]] for x in range(self.width)] for y in range(self.height)]

        #add player to the map
        self._player = Entity('@', self.width//2, self.height//2)
        self._entities = [self._player]
        
    def _flatten_map(self):
        """Returns a matrix where each cell holds the char of the top game object at that location"""
        flattened = [['' for x in range(self.width)] for y in range(self.height)]
        for y, row in enumerate(self._world):
            for x, tile in enumerate(row):
                flattened[y][x] = tile[len(tile) - 1].char
        for entity in self._entities:
            flattened[entity.y][entity.x] = entity.char
        return flattened

    def get(self, x, y):
        """Returns the contents of the tile at x, y"""
        return self._world[y][x]

    def update_world(self, key):
        """Generate the results of a single turn"""
        #TODO: Break key handling into its own function, or maybe even class
        if key in ["y", "7"]:
            self._player.y -= 1
            self._player.x -= 1
        if key in ["KEY_UP", "k", "8"]:
            self._player.y -= 1
        if key in ["u", "9"]:
            self._player.y -= 1
            self._player.x += 1
        if key in ["KEY_LEFT", "h", "4"]:
            self._player.x -= 1
        if key in ["KEY_RIGHT", "l", "6"]:
            self._player.x += 1
        if key in ["b", "1"]:
            self._player.y += 1
            self._player.x -= 1
        if key in ["KEY_DOWN", "j", "2"]:
            self._player.y += 1
        if key in ["n", "3"]:
            self._player.y += 1
            self._player.x += 1

    def as_string(self):
        """Return the top-level tile characters for every tile"""
        #TODO: This won't really work if we want colors.
        worldstring = ""
        flattened = self._flatten_map()
        for row in flattened:
            rowstring = ""
            for char in row:
                rowstring += char
            worldstring += rowstring
            worldstring += '\n'
        return worldstring

