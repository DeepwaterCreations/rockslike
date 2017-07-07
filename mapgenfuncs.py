import parsemap
import entities
import mapfeatures

### MAP GENERATION FUNCTIONS ###
#Take a gameworld object plus other args, return world and map_entities,
#where "world" is a 2d list of map features,
#and "map_entities" is a list of Entity subclass objects, including
#exactly one Player object.

def load_from_file(gw, mapfile):
    """Parse mapfile and turn it into gameworld information"""
    world, entities_partials = parsemap.parse_file(mapfile)
    map_entities = [partial(get_gameworld_cell=gw.get) for partial in entities_partials]
    player = list(filter(lambda x: isinstance(x, entities.Player), map_entities))[0]
    player_spawn = (player.x, player.y)
    return world, map_entities, player_spawn

def empty_box(gw, width, height):
    """Generate a big, empty box of floor with walls around it and put the player in the middle"""
    world = [[[mapfeatures.Wall()] for x in range(width+2)]]
    floor_row = [[mapfeatures.Wall()]]
    floor_row += [[mapfeatures.Floor()] for x in range(width)]
    floor_row += [[mapfeatures.Wall()]]
    for y in range(height):
        world.append(floor_row.copy())
    world.append([[mapfeatures.Wall()] for x in range(width+2)])

    map_entities = []

    return world, map_entities, (width//2, height//2)

