import random

import parsemap
import entities
import mapfeatures

### MAP GENERATION FUNCTIONS ###
#Take a gameworld object plus other args, return mapfeatures, entities, and player_spawn,
#where "mapfeatures" is a 2d list of map features,
#"entities" is a list of Entity subclass objects,
#and "player_spawn" is a set of x, y coordinates for the player's spawn location, presented
#as a tuple.

def load_from_file(gw, mapfile):
    """Parse mapfile and turn it into gameworld information"""
    world, entities_partials, player_spawn = parsemap.parse_file(mapfile)
    map_entities = [partial(get_gameworld_cell=gw.get) for partial in entities_partials]
    # player = list(filter(lambda x: isinstance(x, entities.Player), map_entities))[0]
    # player_spawn = (player.x, player.y)
    return world, map_entities, player_spawn

def empty_box(gw, width, height):
    """Generate a big, empty box of floor with walls around it and put the player in the middle"""
    world = [[mapfeatures.Wall() for x in range(width)]]
    floor_row = [mapfeatures.Wall()]
    floor_row += [mapfeatures.Floor() for x in range(width-2)]
    floor_row += [mapfeatures.Wall()]
    for y in range(height):
        world.append(floor_row.copy())
    world.append([mapfeatures.Wall() for x in range(width)])

    map_entities = []

    return world, map_entities, (width//2, height//2)

class Room():

    def __init__(self, world_coordinates, width_range, height_range):
        self.w_x, self.w_y = world_coordinates
        self.width = random.randrange(*width_range)
        self.height = random.randrange(*height_range)

        self.mapfeatures = self.generate_room_mapfeatures()
        self.entities = self.generate_room_entities()

    def generate_room_mapfeatures(self):
        wall_row = [mapfeatures.Wall() for x in range(self.width)]
        floor_row = [mapfeatures.Wall()]
        floor_row += [mapfeatures.Floor() for x in range(self.width-2)]
        floor_row += [mapfeatures.Wall()]

        roomfeatures = []
        roomfeatures.append(wall_row.copy())
        for y in range(self.height-1):
            roomfeatures.append(floor_row.copy())
        roomfeatures.append(wall_row.copy())

        return roomfeatures

    def generate_room_entities(self):
        return []

    def do_tiles_overlap(self, other):
        """Return true if any tiles in other occupy the same world space as the tiles 
        in this room.
        """
        if not self.do_bounds_overlap(other):
            return False

        #Iterate over the bounding box intersection of both rooms and
        #return True as soon as both contain a tile that is not None
        self_left = max(self.x, other.x) - self.x
        other_left = max(self.x, other.x) - other.x
        self_top = max(self.y, other.y) - self.y
        other_top = max(self.y, other.y) - other.y
        intersect_width = min(self.x+self.width, other.x+other.width) - \
                        max(self.x, other.x)
        intersect_height = min(self.y+self.height, other.y+other.height) - \
                        max(self.y, other.y)
        for y in range(intersect_height):
            for x in range(intersect_width):
                if self.mapfeatures[y+self_top][x+self_left] is not None and \
                        other.mapfeatures[y+other_top][x+other_left] is not None:
                            return True
        return False

    def do_bounds_overlap(self, other):
        """Return True if the bounding box of other overlaps with the bounding 
        box of this room in world space. (The tiles may or may not overlap.
        """
        #v_overlap is true if you can draw a vertical line that passes through
        #   both bounding boxes.
        v_overlap = not (self.x >= (other.x + other.width) or (self.x + self.width) <= other.x)
        #h_overlap, ditto but horizontally.
        h_overlap = not (self.y >= (other.y + other.height) or (self.y + self.height) <= other.y)
        return v_overlap and h_overlap

    def append(self, other, x_offset, y_offset):
        """Return a room containing the tiles in self with the tiles in other mapped onto
        them. Tiles from other overwrite tiles in self when they overlap.
        x_offset: The number of tiles to the right that the tiles from other should start
        y_offset: The number of tiles down that the tiles from other should start
        """
        #First, get the new width, height, w_x, and w_y
        new_width = max((self.x+self.width), (other.x+other.width)) - min(self.x, other.x)
        new_height = max((self.y+self.height), (other.y+other.height)) - min(self.y, other.y)
        new_x = min(self.x, other.x)
        new_y = min(self.y, other.y)
        new_room = Room((new_x, new_y), (new_width, new_width+1), (new_height, new_height+1))

        #Set the new mapfeatures to the union of both rooms' mapfeatures
        new_room.mapfeatures = union_mapfeatures(self.mapfeatures, other.mapfeatures, x_offset, y_offset)

        #Set the new entities to the union of both rooms' entities lists, and change the location
        #of the entities in other to match the offset
        new_entities = other.entities
        for e in new_entities:
            e.x += x_offset
            e.y += y_offset
        new_entities.extend(self.entities)

        return new_room

def union_mapfeatures(a, b, x_offset, y_offset):
    """Return a 2d list of mapfeatures from a and b, where b is offset by x_offset 
    to the left, and by y_offset downward. All empty tiles are None.
    """
    a_width = len(a[0])
    a_height = len(a)
    b_width = len(b[0])
    b_height = len(b)
    new_mapfeatures = []
    for y in range(min(0, y_offset), max(a_height, b_height+y_offset)):
        row = []
        for x in range(min(0, x_offset), max(a_width, b_width+x_offset)):
            new_tile = None
            if y < a_height and x < a_width:
                new_tile = a[y][x]
            if y_offset <= y < b_height+y_offset and x_offset <= x < b_width+x_offset:
                b_x = x - x_offset
                b_y = y - y_offset
                new_tile = b[b_y][b_x]
            row.append(new_tile)
        new_mapfeatures.append(row)
    return new_mapfeatures
