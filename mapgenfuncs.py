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

def bsp(roomclass, width, height, p_w_x=0, p_w_y=0, iteration=0):
    """Recursively divide a space into halves. When the halves are small enough, generate
    rooms in them, then link the rooms with their neighbor partitions' rooms until all the 
    partitions are linked. bsp = Binary Space Partition
    See http://roguecentral.org/doryen/articles/bsp-dungeon-generation/
    roomclass: The Room class to instantiate when a room is created
    width: The width of the current partition (Initially could be the entire game map)
    height: The height of the current partition
    p_w_x: The partition's x coordinate in world-space (the entire game map)
    p_w_y: The partition's y coordinate in world-space
    iteration: The depth of the recursive function
    """
    # debugoutput.add_debug_string("BSP iteration: {0}".format(iteration))
    max_iterations = 10
    min_room_width = 4
    min_room_height = 4
    width_margin = min_room_width+2 
    height_margin = min_room_height+2
    partition_width_threshold = width_margin*2
    partition_height_threshold = height_margin*2

    #0. Check if we're too small or randomly stop based on depth, and if so, build the room and return it.
    if width <= partition_width_threshold or height <= partition_height_threshold or \
            random.random() < iteration/max_iterations:
        room_p_x = random.randrange(0, width-min_room_width)
        room_p_y = random.randrange(0, height-min_room_height)
        max_room_width = width-room_p_x
        max_room_height = height-room_p_y
        room_w_x = p_w_x + room_p_x
        room_w_y = p_w_y + room_p_y
        return [roomclass((room_w_x, room_w_y), (min_room_width, max_room_width), (min_room_height, max_room_height))]

    #1. Divide the area in half randomly.
    v_split = iteration % 2 == 0
    splitbounds = (width_margin, width-width_margin) if v_split else (height_margin, height-height_margin)
    split = random.randrange(*splitbounds)

    #2. Call bsp on the two halves, collect their roomlists.
    width1 = split if v_split else width
    height1 = split if not v_split else height
    p_w_x1 = p_w_x
    p_w_y1 = p_w_y
    roomlist1 = bsp(roomclass, width1, height1, p_w_x1, p_w_y1, iteration+1)

    width2 = width-split if v_split else width
    height2 = height-split if not v_split else height
    p_w_x2 = p_w_x+split if v_split else p_w_x
    p_w_y2 = p_w_y+split if not v_split else p_w_y
    roomlist2 = bsp(roomclass, width2, height2, p_w_x2, p_w_y2, iteration+1)

    #3. Pick a point in each roomlist and connect them with a corridor.

    #A "corridor" is a room with width or length 0
    #I need to pick 4 points: 2 endpoints, 2 bend points. These points will specify the z-corridor.
    #Endpoints: Pick a random point along the parallel axis, then find where it intersects a room or corridor along
    #   the perpendicular axis,
    #Bendpoints: Pick a random place for the bend, just like picking a split.
    #Also check for intersection.
    #TODO: Implement this

    #4. Return all rooms and corridors.
    return roomlist1 + roomlist2
    # return (roomlist1 + roomlist2).append(corridor)
