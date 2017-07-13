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
