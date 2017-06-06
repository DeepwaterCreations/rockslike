"""A module for generating map files from text input"""
import sys
import json
import functools

import mapfeatures
import entities
from tile import Tile

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
            classname - the name of a subclass of Entity that describes this entity
            x_coord - the x coordinate of the entity's position
            y_coord - the y coordinate of the entity's position
            tilechar - the character to display for the object
            fgcolor, bgcolor - strings describing the foreground and backgrounc color
                of the tile
            args - (optional) a list of arguments to pass to the entity's constructor
            ksargs - (optional) a dict of keyword arguments to pass to the entity's constructor
    """
    map_text = map_file.read()
    map_text = map_text.strip()
    map_text = map_text.splitlines()

    mapfeatures_end_index = map_text.index("") if "" in map_text else len(map_text)
    mapfeatures_text = map_text[:mapfeatures_end_index]
    entities_text = map_text[mapfeatures_end_index:]

    matrix = __parse_map_features(mapfeatures_text)
    map_entities = __parse_entities(entities_text)
    return (matrix, map_entities)

def __parse_map_features(mapfeatures_text):
    """Read a description of a map from a file and generate a matrix of map features"""
    matrix = []
    for line in mapfeatures_text:
        parsed_line = [[__map_dict[feature]()] for feature in line.strip()]
        matrix.append(parsed_line)
    return matrix

def __parse_entities(entities_text):
    """Build a list of callable game entity constructors from a list of JSON objects"""
    entities_text = "".join(entities_text)
    json_entities = json.loads(entities_text)

    map_entities = []
    for obj in json_entities:
        x_coord = int(obj['x_coord'])
        y_coord = int(obj['y_coord'])
        fgcolor = obj['fgcolor'] if 'fgcolor' in obj else "WHITE"
        bgcolor = obj['bgcolor'] if 'bgcolor' in obj else "BLACK"
        tile = Tile(obj['tilechar'], fgcolor, bgcolor) if 'tilechar' in obj else None
        args = obj['args'] if 'args' in obj else []
        if tile is not None:
            args.append(tile)
        args.append(x_coord)
        args.append(y_coord)
        kwargs = obj['kwargs'] if 'kwargs' in obj else {}
        entity_class = getattr(sys.modules["entities"], obj['classname'])
        entity_partial = functools.partial(entity_class, *args, **kwargs)
        map_entities.append(entity_partial)
    return map_entities
