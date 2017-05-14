import entities
import mapfeatures
import keyinput

class GameWorld():
    """A class to hold the current state of the game world"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        #World is represented by a 2d matrix of lists
        #Each coordinate in the matrix is a cell
        #The list for that cell holds game objects
        #that are located in that cell.
        self._world = [[[mapfeatures.Floor()] for x in range(self.width)] for y in range(self.height)]

        #add player to the map
        self._player = entities.Player(self.width//2, self.height//2, self.get)
        self._entities = [self._player]
        
    def flatten_map(self):
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
        keyinput.handle_key(key)
