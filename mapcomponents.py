"""A module for sets of tiles that make up a component of a map, such as a room or corridor"""
import random

import mapfeatures

class MapComponent():

    def __init__(self, world_coordinates, width, height):
        self.w_x, self.w_y = world_coordinates
        self.width = width
        self.height = height

        self.mapfeatures = [[None for x in range(self.width)] for y in range(self.height)]
        self.entities = []

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
        new_component = MapComponent((new_x, new_y), new_width, new_height)

        #Set the new mapfeatures to the union of both rooms' mapfeatures
        new_component.mapfeatures = union_mapfeatures(self.mapfeatures, other.mapfeatures, x_offset, y_offset)

        #Set the new entities to the union of both rooms' entities lists, and change the location
        #of the entities in other to match the offset
        new_entities = other.entities
        for e in new_entities:
            e.x += x_offset
            e.y += y_offset
        new_entities.extend(self.entities)

        return new_component

class Room(MapComponent):

    def __init__(self, world_coordinates, width_range, height_range, *args, **kwargs):
        self.width = random.randrange(*width_range)
        self.height = random.randrange(*height_range)
        super(Room, self).__init__(world_coordinates, self.width, self.height, *args, **kwargs)

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

class Corridor(MapComponent):

    def __init__(self, start_coords, end_coords):
        width = abs(start_coords[0] - end_coords[0])
        height = abs(start_coords[1] - end_coords[1])
        world_coords = (min(start_coords[0], end_coords[0]), min(start_coords[1], end_coords[1]))
        super(Corridor, self).__init__(world_coords, width, height)

        self.mapfeatures = self.generate_corridor_mapfeatures()
        self.entities = self.generate_corridor_entities()

    def generate_corridor_mapfeatures(self):
        pass
    
    def generate_corridor_entities(self):
        return []
