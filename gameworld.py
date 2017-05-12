class MapFeature():
    """A static element of the map, such as a floor or wall tile"""

    def __init__(self, char):
        self.char = char

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

    def get(self, x, y):
        """Returns the contents of the tile at x, y"""
        return self._world[y][x]

    def update_world(self):
        """Generate the results of a single turn"""
        pass

    def as_string(self):
        """Return the top-level tile characters for every tile"""
        #TODO: This won't really work if we want colors.
        worldstring = ""
        for row in self._world:
            rowstring = ""
            for tile in row:
                char = tile[len(tile)-1].get_char()
                rowstring += char
            worldstring += rowstring
            worldstring += '\n'
        return worldstring

