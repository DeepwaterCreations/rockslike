import parsemap

### MAP GENERATION FUNCTIONS ###
#Take a gameworld object plus other args, return world and map_entities,
#where "world" is a 2d list of map features,
#and "map_entities" is a list of Entity subclass objects, including
#exactly one Player object.

def load_from_file(gw, mapfile):
    """Parse mapfile and turn it into gameworld information"""
    world, entities_partials = parsemap.parse_file(mapfile)
    map_entities = [partial(get_gameworld_cell=gw.get) for partial in entities_partials]
    return world, map_entities
