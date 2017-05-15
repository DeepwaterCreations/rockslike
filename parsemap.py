"""A module for generating map files from text input"""
import mapfeatures

__map_dict = {
        '.': mapfeatures.Floor,
        '#': mapfeatures.Wall,
        ' ': mapfeatures.Void
        }

def parse_file(map_file):
    """Divide file into map features section and entities section

    Sections are delimited by blank lines
    Map Features: An ASCII picture of the map
    Entities: A JSON list of objects with these fields:
            x_coord - the x coordinate of the entity's position
            y_coord - the y coordinate of the entity's position
            classname - the name of a subclass of Entity that describes this entity
            args - (optional) a list of arguments to pass to the entity's constructor
    """
    map_text = map_file.read()
    map_text = map_text.strip()
    map_text = map_text.splitlines()

    mapfeatures_end_index = map_text.index("\n") if "\n" in map_text else len(map_text)
    mapfeatures_text = map_text[:mapfeatures_end_index]
    entities_text = map_text[mapfeatures_end_index:]

    return __parse_map_features(mapfeatures_text)

def __parse_map_features(mapfeatures_text):
    """Read a description of a map from a file and generate a matrix of map features"""
    matrix = []
    for line in mapfeatures_text:
        parsed_line = [[__map_dict[feature]()] for feature in line.strip()]
        matrix.append(parsed_line)
    return matrix
